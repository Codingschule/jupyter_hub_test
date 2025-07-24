# type: ignore
import os
from dockerspawner import DockerSpawner  # type: ignore
from jupyterhub.auth import DummyAuthenticator  # type: ignore

c = get_config()  # type: ignore

c.JupyterHub.bind_url = 'http://:8000'
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_connect_ip = 'jupyterhub'

c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_IMAGE']
c.DockerSpawner.cmd = ["start-notebook.sh"]
c.Spawner.start_timeout = 120
c.DockerSpawner.network_name = os.environ['JUPYTERHUB_NETWORK']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.remove = True
c.DockerSpawner.name_template = "jupyter-{username}"

c.Authenticator.admin_users = { os.environ['JUPYTERHUB_ADMIN_USERS'] }
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = "1234"
