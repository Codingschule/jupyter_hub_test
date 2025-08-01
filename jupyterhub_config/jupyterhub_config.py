# type: ignore
import os
from nativeauthenticator import NativeAuthenticator
from dockerspawner import DockerSpawner  # type: ignore
#from jupyterhub.auth import DummyAuthenticator  # type: ignore

c = get_config()  # type: ignore

c.JupyterHub.bind_url = 'http://:8000'
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_connect_ip = 'jupyterhub'

c.JupyterHub.authenticator_class = NativeAuthenticator
c.NativeAuthenticator.open_signup = True

c.NativeAuthenticator.auto_approve = True
admin_users = os.environ['JUPYTERHUB_ADMIN_USERS'].split(",")
c.Authenticator.admin_users = set(admin_users)
c.Authenticator.allowed_users = set(admin_users)

# db
db_name = os.environ['DB_NAME']
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASSWORD']

c.JupyterHub.db_url = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_IMAGE']
c.DockerSpawner.cmd = ["start-notebook.sh"]
c.DockerSpawner.network_name = os.environ['JUPYTERHUB_NETWORK']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.remove = True
c.DockerSpawner.name_template = 'jupyter-{username}'
c.DockerSpawner.notebook_dir = '/home/jovyan/work'
c.DockerSpawner.volumes = {
    'jupyterhub-user-{username}': '/home/jovyan/work'
}


c.Spawner.start_timeout = 120
c.Spawner.http_timeout = 120
