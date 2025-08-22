import os

def split_csv(env, default=""):
    return [x.strip() for x in os.environ.get(env, default).split(",") if x.strip()]


# Define scopes for roles
def scopes_for_role(role_name: str):
    r = (role_name or "").lower()
    if r == "admin":
        return ["admin-ui","admin:users","admin:servers","admin:groups","admin:services","read:hub","read:metrics"]
    if r == "user-admin":
        return ["admin-ui","admin:users","admin:groups","read:roles","read:hub","list:users","read:users","read:groups","servers","access:servers"]
    return ["self"]


def configure_users_and_roles(c):
    admin_users = split_csv("JUPYTERHUB_ADMIN_USERS")
    subadmin_users = split_csv("JUPYTERHUB_SUBADMIN_USERS")
    allowed_users_env = split_csv("JUPYTERHUB_ALLOWED_USERS")

    BOOTSTRAP_FLAG = os.environ.get(
        "JUPYTERHUB_SIGNUP_BOOTSTRAP_FLAG",
        "/srv/jupyterhub/.signup_bootstrap_done"
    )

    first_bootstrap = not os.path.exists(BOOTSTRAP_FLAG)
    if first_bootstrap:
        try:
            with open(BOOTSTRAP_FLAG, "w", encoding="utf-8") as f:
                f.write("signup opened on first boot\n")
            print(f"[bootstrap] Signup OPEN only this execution. Flags created: {BOOTSTRAP_FLAG}")
        except Exception as e:
            print(f"[bootstrap] can't create flag {BOOTSTRAP_FLAG}: {e}")

    env_open = os.environ.get("JUPYTERHUB_OPEN_SIGNUP", "false").lower() == "true"

    c.NativeAuthenticator.open_signup  = env_open or first_bootstrap
    # for the users security: only allow signup on first boot unless explicitly enabled
    c.Authenticator.admin_users = set(admin_users)
    base_allowed = set(allowed_users_env) #  if allowed_users_env else set(admin_users + subadmin_users)

    if base_allowed:
      c.Authenticator.allowed_users = base_allowed | set(admin_users)

    roles = []
    if subadmin_users:
        roles.append({
            "name": "user-admin",
            "description": "Role limit to management users and groups",
            "scopes": scopes_for_role("user-admin"),
            "users": subadmin_users,
        })

    c.JupyterHub.load_roles = roles
    
    c.JupyterHub.load_groups = {
        "admins": {"users": admin_users},
        "subadmins": {"users": subadmin_users},
    }


