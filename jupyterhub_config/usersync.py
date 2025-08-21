#!/usr/bin/env python3
import os, time, json, urllib.request, urllib.error, urllib.parse, hashlib, sys

API_URL = os.environ["JUPYTERHUB_API_URL"].rstrip("/")   # CDI for JupyterHub
API_TOKEN = os.environ["JUPYTERHUB_API_TOKEN"]           # CDI for JupyterHub
USERS_FILE = os.getenv("USERS_FILE", "/srv/jupyterhub/users.json")
INTERVAL = int(os.getenv("USERSYNC_INTERVAL", "10"))
PRUNE = os.getenv("USERSYNC_PRUNE", "false").lower() == "true"

HDRS = {"Authorization": f"token {API_TOKEN}", "Content-Type": "application/json"}

def api(method, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_URL + path, data=data, method=method, headers=HDRS)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read()
            return r.getcode(), json.loads(body) if body else None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return e.code, body
    except Exception as e:
        return None, str(e)

def load_desired():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    desired_users = {}  
    desired_groups = {} 


    if isinstance(raw, list):
        for u in raw:
            desired_users[str(u)] = {"admin": False, "groups": set()}
    elif isinstance(raw, dict):
        if "users" in raw and isinstance(raw["users"], list):
            for u in raw["users"]:
                name = str(u.get("name") or u.get("username"))
                if not name:
                    continue
                admin = bool(u.get("admin", False))
                groups = set(u.get("groups", []))
                desired_users[name] = {"admin": admin, "groups": groups}

        for name in raw.get("admins", []) or []:
            name = str(name)
            desired_users.setdefault(name, {"admin": False, "groups": set()})
            desired_users[name]["admin"] = True
        for name in raw.get("allowed", []) or []:
            name = str(name)
            desired_users.setdefault(name, {"admin": False, "groups": set()})
        for g, members in (raw.get("groups") or {}).items():
            desired_groups.setdefault(g, set()).update(map(str, members))
            for m in members:
                m = str(m)
                desired_users.setdefault(m, {"admin": False, "groups": set()})
                desired_users[m]["groups"].add(g)
    else:
        raise ValueError("Format of users.json not recognized")

    return desired_users, desired_groups

def get_current():
    code, users = api("GET", "/users")
    if code != 200 or not isinstance(users, list):
        raise RuntimeError(f"GET /users error: {code} {users}")
    cur_users = {u["name"]: {"admin": bool(u.get("admin")), "groups": set(u.get("groups", []))} for u in users}

    code, groups = api("GET", "/groups")
    if code != 200 or not isinstance(groups, list):
        raise RuntimeError(f"GET /groups error: {code} {groups}")
    cur_groups = {g["name"]: set(g.get("users", [])) for g in groups}
    return cur_users, cur_groups


def ensure_user(name: str, admin: bool):

    uname = name.strip()
    path = f"/users/{urllib.parse.quote(uname, safe='')}"


    post_body = {"admin": True} if admin else None
    code, _ = api("POST", path, post_body)
    if code not in (201, 409):  # 201 created, 409 already exists
        raise RuntimeError(f"POST {path} -> {code}")

    code, data = api("GET", path, None)
    if code == 200 and isinstance(data, dict):
        cur_admin = bool(data.get("admin", False))
        if cur_admin != bool(admin):
            code2, _ = api("PATCH", path, {"admin": bool(admin)})
            if code2 not in (200, 204):
                raise RuntimeError(f"PATCH {path} -> {code2}")
    else:
        code2, _ = api("PATCH", path, {"admin": bool(admin)})
        if code2 not in (200, 204, 404):
            raise RuntimeError(f"PATCH {path} -> {code2}")

def ensure_group(name):
    code, _ = api("POST", "/groups", {"groups": [name]})
    if code not in (201, 409):
        raise RuntimeError(f"POST /groups {name} -> {code}")        


def add_members(group, users):
    if not users:
        return
    code, _ = api("POST", f"/groups/{urllib.parse.quote(group)}/users", {"users": list(users)})
    if code not in (200, 201, 204):
        raise RuntimeError(f"POST /groups/{group}/users -> {code}")

def remove_members(group, users):
    for u in users:
        code, _ = api("DELETE", f"/groups/{urllib.parse.quote(group)}/users/{urllib.parse.quote(u)}")
        if code not in (200, 204):
            pass  

def reconcile():
    desired_users, desired_groups = load_desired()
    cur_users, cur_groups = get_current()

    for name, meta in desired_users.items():
        ensure_user(name, meta["admin"])

    for g in desired_groups.keys():
        ensure_group(g)

    cur_users, cur_groups = get_current()

    for g, want_members in desired_groups.items():
        have = cur_groups.get(g, set())
        missing = want_members - have
        add_members(g, missing)
        if PRUNE:
            extra = have - want_members
            remove_members(g, extra)

def watch():
    last_sig = None
    while True:
        try:
            with open(USERS_FILE, "rb") as f:
                b = f.read()
            sig = hashlib.sha1(b).hexdigest()
            if sig != last_sig:
                reconcile()
                last_sig = sig
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"[usersync] error: {e}", flush=True)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    if "--once" in sys.argv:
        reconcile()
    else:
        print(f"[usersync] watching {USERS_FILE} every {INTERVAL}s (prune={PRUNE})", flush=True)
        watch()
