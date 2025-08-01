# JupyterHub with DockerSpawner and PostgreSQL

[![JupyterHub](https://img.shields.io/badge/Powered%20by-JupyterHub-orange.svg)](https://jupyter.org/hub)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue.svg)](https://www.postgresql.org/)

This project provides a robust, containerized JupyterHub environment that allows multiple users to work in isolated environments. It uses DockerSpawner to launch separate notebook environments for each user in their own Docker containers, and a PostgreSQL database for persistent storage of user and Hub data.

## 🚀 Key Features

- **Isolated Environments**: Each user gets their own Docker container, ensuring security and reproducible environments
- **Persistent Storage**: User notebooks and data are stored in named Docker volumes, persisting even after a container is stopped or removed
- **Centralized Authentication**: Uses `NativeAuthenticator` for a simple, database-backed user management system
- **Scalable**: This setup provides a solid foundation for running JupyterHub for small to medium-sized teams

## 📋 Prerequisites

- Docker
- Docker Compose

## 🛠️ Setup

### 1. Create Docker Network

This setup requires a manually created Docker network to ensure all services can reliably communicate. Run this command **once**:

```shell script
docker network create jupyterhub-network
```

### 2. Configure Environment Variables

1. Copy the `.env.dummy` file to a new file named `.env`:
```shell script
cp .env.dummy .env
```

2. Edit the `.env` file and adjust the following values:
```
JUPYTERHUB_PORT=8000                     # Port for JupyterHub to run on
   DOCKER_JUPYTER_IMAGE=jupyter/minimal-notebook:latest # Docker image for user notebooks
   JUPYTERHUB_ADMIN_USERS=admin             # Comma-separated list of admin users
   JUPYTERHUB_NETWORK=jupyterhub-network    # Name of Docker network
   
   DB_NAME=jupyterhub                       # PostgreSQL database name
   DB_HOST=postgres                         # PostgreSQL server hostname
   DB_PORT=5432                             # PostgreSQL port
   DB_ROOT_PASSWORD=rootpassword            # Root password for PostgreSQL
   DB_USER=jupyterhub                       # PostgreSQL user
   DB_PASSWORD=jupyterhubpass               # PostgreSQL password
```

### 3. Build and Start Containers

```shell script
docker-compose up -d --build
```

## 🖥️ Usage

1. Access JupyterHub in your browser at `http://localhost:8000` (or the port configured in `.env`)
2. Log in with a username and password of your choice
3. Users listed in `JUPYTERHUB_ADMIN_USERS` will have administrator privileges
4. After logging in, you will be redirected to your personal Jupyter notebook server

## ⚙️ Configuration

- **JupyterHub**: The main configuration is in `jupyterhub_config.py`. You can customize authentication, user roles, and other settings here.
- **Notebook Environment**: The `Dockerfile` defines the Docker image for user notebook servers. You can add new libraries and dependencies to this file.
- **Docker Compose**: The `docker-compose.yml` file defines the services and their relationships.

## 🔧 Troubleshooting

- **Containers won't start**: Check if the Docker network was created correctly and if environment variables are set properly.
- **Access issues**: Ensure the correct permissions are in place for the Docker socket.
- **Database connection problems**: Verify the DB settings in the `.env` file.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).