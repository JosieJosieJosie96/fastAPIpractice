# main.py

from typing import Optional, List
from auth import authenticate
from fastapi import FastAPI, HTTPException, Depends


import secrets
from models import Item, User




items: List[Item] = []
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items/")
async def create_item(item: Item):
    item.id = len(items)
    items.append(item)
    return item

@app.post("/items_tax/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


@app.get("/items/", response_model=List[Item])
async def get_items():
    return items

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        return {"error": "Item not found"}
    deleted_item = items.pop(item_id)
    return {"deleted": deleted_item}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/secure-data/")
def read_secure_data(username: str = Depends(authenticate)):
    return {"message": f"Hello, {username}. You are authenticated!"}