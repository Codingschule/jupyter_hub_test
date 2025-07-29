FROM jupyterhub/jupyterhub:latest

RUN pip install \
 jupyterhub \
 jupyterlab \
 jupyterhub-nativeauthenticator \
 dockerspawner \
 psycopg2-binary==2.9.9

