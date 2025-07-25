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
c.Authenticator.allowed_users = {"admin"}
c.Authenticator.admin_users = {"admin"}

c.NativeAuthenticator.auto_approve = True
c.Authenticator.admin_users = { os.environ['JUPYTERHUB_ADMIN_USERS'] }
#c.JupyterHub.authenticator_class = DummyAuthenticator

# db
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_host = os.environ['MYSQL_HOST']
db_port = os.environ['MYSQL_PORT']
db_name = os.environ['MYSQL_DB']

c.JupyterHub.db_url = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

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


#c.DummyAuthenticator.password = "1234"

c.Spawner.start_timeout = 120
c.Spawner.http_timeout = 120
