from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

my_posts=[]

class Post(BaseModel):
    title : str
    content : str
    published: bool = True
    rating: Optional[int] = 0

@app.get("/posts")
def get_posts():
    return my_posts

@app.get("/posts/{id}")
def get_post_by_id(id : int, response : Response):
    post = find_post(id)

    if not post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} was not found")

    return post

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_post(post : Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return post_dict

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_for_post(id)
    if index == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} was not found")

    my_posts.pop(index)

@app.put("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def update_post(id: int, post: Post):
    index = find_index_for_post(id)

    if index == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} was not found")

    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict

def find_index_for_post(id: int) -> int:
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

def find_post(id : int):
    for post in my_posts:
        print(post)
        print(id)
        if post["id"] == id:
            return post