ARG JUPYTERHUB_VERSION=5.1.0
FROM jupyterhub/jupyterhub:${JUPYTERHUB_VERSION}

ARG JUPYTERLAB_VERSION=4.2.5
ARG NATIVEAUTH_VERSION=1.3.0
ARG DOCKERSPAWNER_VERSION=14.0.0
ARG PG_PKG="psycopg[binary]==3.1.18"
# driver python to Postgree
# binari : evita instalar librerías del sistema (más simple y estable en contenedores).



RUN python3 -m pip install --no-cache-dir --upgrade pip \
 && python3 -m pip install --no-cache-dir \
      jupyterlab==${JUPYTERLAB_VERSION} \
      jupyterhub-nativeauthenticator==${NATIVEAUTH_VERSION} \
      dockerspawner==${DOCKERSPAWNER_VERSION} \
      "${PG_PKG}" \
  && python3 -m pip check \
 && rm -rf /root/.cache/pip ~/.cache/pip /tmp/*

 # psycopg2-binary>=2.9,<3.0 \ 
 # psycopg2-binary==${PSYCOPG2_VERSION} \