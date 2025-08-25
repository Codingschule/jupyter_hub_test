import os

def get_db_env():
    return (
        os.environ['POSTGRES_DB'],
        os.environ['DB_HOST'],
        os.environ['DB_PORT'],
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
    )