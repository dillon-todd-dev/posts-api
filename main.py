from fastapi import FastAPI
from dotenv import load_dotenv
import os
import psycopg2


app = FastAPI()


load_dotenv()

db_params = {
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": os.getenv("POSTGRES_PORT"),
    "host": os.getenv("POSTGRES_HOST")
}

try:
    conn = psycopg2.connect(**db_params)
    print('successfully connected to db')
    cursor = conn.cursor()
except (Exception, psycopg2.Error) as error:
    print(f'failed to connect to db: {error}')


@app.get('/')
def root():
    return {'message': 'hello, world!'}
