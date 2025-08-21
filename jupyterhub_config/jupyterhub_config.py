# type: ignore
import os, re

from user_mgmt import configure_users_and_roles
from hub_setup import get_db_env
from auth_setup import apply_auth
from spawner_setup import apply_spawner

c = get_config()  # type: ignore

users_file = os.getenv("USERS_FILE", "/srv/jupyterhub/users.json")
sync_interval = int(os.getenv("USERSYNC_INTERVAL", "10"))
prune = os.getenv("USERSYNC_PRUNE", "false")

c.JupyterHub.services = [
    {
        "name": "usersync",
        "admin": True,  
        "command": ["python", "/srv/jupyterhub/usersync.py"],
        "environment": {
            "USERS_FILE": users_file,
            "USERSYNC_INTERVAL": str(sync_interval),
            "USERSYNC_PRUNE": prune,
        },
    }
]

apply_auth(c, users_file=users_file)

# --- URLs Hub ---
c.JupyterHub.bind_url = "http://:8000"
c.JupyterHub.hub_bind_url = "http://0.0.0.0:8081"
c.JupyterHub.hub_connect_url = "http://jupyterhub:8081"

# --- Config users & rols ---
configure_users_and_roles(c)

# --- DB configuration ----
db_name, db_host, db_port, db_user, db_pass = get_db_env()
c.JupyterHub.db_url = f'postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

# --- Spawner configuration ---
apply_spawner(c)

c.JupyterHub.log_level = "INFO"
c.JupyterHub.tornado_settings = {"slow_spawn_timeout": 60} 

c.JupyterHub.cookie_secret_file = "/srv/jupyterhub/secret/jupyterhub_cookie_secret"



