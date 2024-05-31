import os
import time
import psycopg2
from fastapi import FastAPI, status, HTTPException
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


@app.get('/posts/{post_id}')
def get_post_by_id(post_id: int):
    select_query = "SELECT * FROM posts WHERE id = %s;"
    cursor.execute(select_query, (str(post_id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"can't find post with id: {post_id}")
    return {'data': post}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    insert_query = "INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *;"
    cursor.execute(insert_query, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}


@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    delete_query = "DELETE FROM posts WHERE id = %s RETURNING *;"
    cursor.execute(delete_query, (str(post_id)))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"can't find post with id: {post_id}")
    conn.commit()
