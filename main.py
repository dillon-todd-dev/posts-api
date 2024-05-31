import os
import time
import psycopg2
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor


app = FastAPI()


load_dotenv()

db_params = {
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": os.getenv("POSTGRES_PORT"),
    "host": os.getenv("POSTGRES_HOST"),
    "cursor_factory": RealDictCursor
}

while True:
    try:
        conn = psycopg2.connect(**db_params)
        print('successfully connected to db')
        cursor = conn.cursor()
        break
    except (Exception, psycopg2.Error) as error:
        print(f'failed to connect to db: {error}')
        time.sleep(5)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get('/')
def root():
    return {'message': 'hello, world!'}


@app.get('/posts')
def get_posts():
    select_query = "SELECT * FROM posts;"
    cursor.execute(select_query)
    posts = cursor.fetchall()
    return {'data': posts}


@app.post('/posts')
def create_post(post: Post):
    insert_query = "INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *;"
    cursor.execute(insert_query, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}
