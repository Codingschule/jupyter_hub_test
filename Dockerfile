FROM jupyterhub/jupyterhub:latest

RUN pip install  jupyterhub jupyterlab jupyterhub-nativeauthenticator pymysql dockerspawner

