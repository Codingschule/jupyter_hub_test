# type: ignore
import os, re, json
from nativeauthenticator import NativeAuthenticator
from dockerspawner import DockerSpawner  # type: ignore

from user_mgmt import configure_users_and_roles
from hub_setup import get_db_env

c = get_config()  # type: ignore

# --------------- config user sync ----------------
users_file = os.getenv("USERS_FILE", "/srv/jupyterhub/users.json")
sync_interval = int(os.getenv("USERSYNC_INTERVAL", "10"))
prune = os.getenv("USERSYNC_PRUNE", "false")

c.JupyterHub.services = [
    {
        "name": "usersync",
        "admin": True,  # Authorize to create users/groups
        "command": ["python", "/srv/jupyterhub/usersync.py"],
        "environment": {
            "USERS_FILE": users_file,
            "USERSYNC_INTERVAL": str(sync_interval),
            "USERSYNC_PRUNE": prune,
        },
    }
]





# Auto-approve users if they are listed in the users.json file
class AutoApproveAuthenticator(NativeAuthenticator):
    def add_user(self, username, *args, **kwargs):
        try:
            with open(users_file) as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}
        if username in users:
            kwargs["approved"] = True
        return super().add_user(username, *args, **kwargs)

c.JupyterHub.authenticator_class = AutoApproveAuthenticator
c.NativeAuthenticator.admin_approval = False
c.NativeAuthenticator.open_signup = False  # Not signup opened default





# --- URLs del Hub ---
c.JupyterHub.bind_url = "http://:8000"
c.JupyterHub.hub_bind_url = "http://0.0.0.0:8081"
c.JupyterHub.hub_connect_url = "http://jupyterhub:8081"

# c.JupyterHub.authenticator_class = NativeAuthenticator    #modified to function AutoAprovved....

c.NativeAuthenticator.minimum_password_length = 3
# todo : c.NativeAuthenticator.password_config = 20

# --- Configuración de usuarios y roles ---
configure_users_and_roles(c)


# --- db configuration ----
db_name, db_host, db_port, db_user, db_pass = get_db_env()
c.JupyterHub.db_url = f'postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'






# Spawner configuration
c.JupyterHub.spawner_class = DockerSpawner
#-----------------------------new
#c.JupyterHub.hub_ip = "jupyterhub"
""" jupyterhub: es el nombre del servicio en docker-compose. Dentro de las redes de Docker, ese nombre resuelve por DNS a la IP del contenedor del Hub.
8081: es el puerto interno donde el proceso del Hub escucha sus APIs internas (no es el puerto público del proxy). """
#-----------------------------
c.DockerSpawner.image =  os.environ.get("DOCKER_JUPYTER_IMAGE", "jupyter/datascience-notebook:latest")
# os.environ['DOCKER_JUPYTER_IMAGE']
c.DockerSpawner.cmd =  ["start-singleuser.py"] # ["jupyterhub-singleuser"] #or image   ["start-singleuser.py"] #
#["start-notebook.sh"] image has
c.DockerSpawner.network_name = os.environ['JUPYTERHUB_NETWORK']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.remove = False        
c.DockerSpawner.name_template = 'jupyter-{username}'
c.Spawner.args = ["--ServerApp.root_dir=/home/jovyan/work"]
#c.DockerSpawner.notebook_dir = '/home/jovyan/work'
c.DockerSpawner.volumes = {'jupyterhub-user-{username}': '/home/jovyan/work'}
c.DockerSpawner.extra_host_config = {   
    "shm_size": "1g"          # important for pandas/plotly (memory shared)
}
# c.DockerSpawner.extra_create_kwargs = {'user': 'root'} # root permission Volumens
c.DockerSpawner.environment = {
    'CHOWN_HOME': 'yes',
    'CHOWN_HOME_OPTS': '-R',
    'NB_UID': '1000',   # jovyan
    'NB_GID': '100',    # group 'users'
}
c.Spawner.default_url = '/lab'   # UX defaults

c.Spawner.start_timeout = 600
c.Spawner.http_timeout = 600

c.DockerSpawner.debug = False
c.JupyterHub.log_level = "INFO"

c.JupyterHub.tornado_settings = {"slow_spawn_timeout": 60} 
# silenciar ese aviso temprano de 10 s:
c.Authenticator.username_pattern = r'^[a-zA-Z0-9._%+\-@]+$'


