
# JupyterHub with DockerSpawner and PostgreSQL

This project provides a robust, containerized JupyterHub setup. It uses DockerSpawner to launch isolated notebook environments for each user in their own Docker containers, and a PostgreSQL database for persistent storage of user and Hub data.

## Key Features

-   **Isolated Environments:** Each user gets their own Docker container, ensuring security and reproducible environments.
-   **Persistent Storage:** User notebooks and data are stored in named Docker volumes, persisting even after a container is stopped or removed.
-   **Centralized Authentication:** Uses `NativeAuthenticator` for a simple, database-backed user management system.
-   **Scalable:** This setup provides a solid foundation for running JupyterHub for small to medium-sized teams.

## Prerequisites

-   Docker
-   Docker Compose

## Setup Instructions

Follow these steps to configure and launch the environment.

### 1. Create the External Docker Network

This setup requires a manually created Docker network to ensure all services can reliably communicate. Run this command **once**:

```bash
docker network create jupyterhub-network
```

### 2. Create a `.env` file

Create a `.env` file in the root of the project and add the following environment variables:

```
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_USER=your_postgres_user
POSTGRES_DB=your_postgres_db
```

### 3. Build and Run the Containers

```bash
docker-compose up -d --build
```

## Usage

1.  Access JupyterHub in your browser at `http://localhost:8000`.
2.  The first user to log in will become an administrator.
3.  Log in with a username and password of your choice.
4.  You will be redirected to your personal Jupyter notebook server.

## Configuration

-   **JupyterHub:** The main configuration is in `jupyterhub_config.py`. You can customize authentication, user roles, and more.
-   **Notebook Environment:** The `Dockerfile` defines the Docker image for user notebook servers. You can add new libraries and dependencies to this file.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
