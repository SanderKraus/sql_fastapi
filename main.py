from fastapi import Depends, FastAPI, HTTPException, responses, encoders, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

import requests, asyncio
import httpx

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)

#     # print(f'db_user {db_user}')
#     # print(f'user_id {user_id}')
#     '''
#     Getting the response-body with python.requests
#     '''
#     # url_string = "http://127.0.0.1:8000/users/"
#     # print(url_string + str(user_id))
#     # r = requests.get(url_string + str(user_id))
#     # print(r.content)

#     if db_user is None:
#         raise HTTPException(status_code=404, detail="Dieser User wurde nicht in der Datenbank gefunden!")
#     return db_user


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    # print(f'db_user {db_user}')
    # print(f'user_id {user_id}')

    if db_user is None:
        raise HTTPException(status_code=404, detail="Dieser User wurde nicht in der Datenbank gefunden!")
    return db_user

print('-------')
print(read_user(1))

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
