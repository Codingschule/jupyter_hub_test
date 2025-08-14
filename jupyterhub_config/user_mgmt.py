import os

def split_csv(env, default=""):
    return [x.strip() for x in os.environ.get(env, default).split(",") if x.strip()]


# --- Roles y scopes ---
def scopes_for_role(role_name: str):
    r = (role_name or "").lower()
    if r == "admin":
        return ["admin-ui","admin:users","admin:servers","admin:groups","admin:services","read:hub","read:metrics"]
    if r == "user-admin":
        return ["admin-ui","admin:users","admin:groups","read:roles","read:hub","list:users","read:users","read:groups","servers","access:servers"]
    return ["self"]


def configure_users_and_roles(c):
    # Define los usuarios administradores y subadministradores
    admin_users = split_csv("JUPYTERHUB_ADMIN_USERS")
    subadmin_users = split_csv("JUPYTERHUB_SUBADMIN_USERS")
    allowed_users_env = split_csv("JUPYTERHUB_ALLOWED_USERS")

    # Define el flag de bootstrap
    BOOTSTRAP_FLAG = os.environ.get(
        "JUPYTERHUB_SIGNUP_BOOTSTRAP_FLAG",
        "/srv/jupyterhub/.signup_bootstrap_done"
    )

    first_bootstrap = not os.path.exists(BOOTSTRAP_FLAG)
    if first_bootstrap:
        try:
            with open(BOOTSTRAP_FLAG, "w", encoding="utf-8") as f:
                f.write("signup opened on first boot\n")
            print(f"[bootstrap] Signup ABIERTO solo esta ejecución. Flag creados: {BOOTSTRAP_FLAG}")
        except Exception as e:
            print(f"[bootstrap] No pude crear flag {BOOTSTRAP_FLAG}: {e}")

    env_open = os.environ.get("JUPYTERHUB_OPEN_SIGNUP", "false").lower() == "true"
    # env_auto = os.environ.get("JUPYTERHUB_AUTO_APPROVE", "false").lower() == "true"

    c.NativeAuthenticator.open_signup  = env_open or first_bootstrap
    # c.NativeAuthenticator.auto_approve = env_auto or first_bootstrap


    # Allowed users and roles
    c.Authenticator.admin_users = set(admin_users)
    base_allowed = set(allowed_users_env) if allowed_users_env else set(admin_users + subadmin_users)
    c.Authenticator.allowed_users = base_allowed | set(admin_users)

    # Define los roles
    roles = []
    if subadmin_users:
        roles.append({
            "name": "user-admin",
            "description": "Rol limit to management users and groups",
            "scopes": scopes_for_role("user-admin"),
            "users": subadmin_users,
        })
    c.JupyterHub.load_roles = roles

    # Grupos de conveniencia (formato NUEVO requerido)
    c.JupyterHub.load_groups = {
        "admins": {"users": admin_users},
        "subadmins": {"users": subadmin_users},
    }


