from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, engine
from typing import List
from fastapi.middleware.cors import CORSMiddleware
# from . import models, schemas # TODO: why doesn't this work?
import models, schemas
from sqlalchemy.orm import Session
from crud import save_user, update_user, get_user, get_users, get_usernames, remove_user, check_password
from leetcode import get_data_from_leetcode

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return True

@app.post('/user', response_model=schemas.UserOut)
def create_user(user_in: schemas.UserIn, db: Session = Depends(get_db)):
    user = get_user(db, user_in.username)
    if user:
        raise HTTPException(status_code=400, detail='Username exists')
    user_saved = save_user(db, user_in)
    return user_saved

@app.delete('/user')
def delete_user(user_in: schemas.UserIn, db: Session = Depends(get_db)):
    user = get_user(db, user_in.username)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not check_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail='Invalid password')
    remove_user(db, user)
    return {'ok': True}

@app.post('/rating')
def update_ratings(db: Session = Depends(get_db)):
    usernames = get_usernames(db)
    for username in usernames:
        try:
            data = get_data_from_leetcode(username)
            update_user(db, username, data['rating'], data['top_percentage'])
        except Exception as e:
            print(f'error while updating username={username}', e)
    return {'ok': True}

@app.get('/rating', response_model=List[schemas.UserOut])
def get_rating(db: Session = Depends(get_db)):
    return get_users(db)
