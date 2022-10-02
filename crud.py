import bcrypt
from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import desc

def get_user(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()

def password_hasher(raw_password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(raw_password.encode(), salt)

def check_password(raw_password: str, hashed_password: str):
    return bcrypt.checkpw(raw_password.encode(), hashed_password.encode())

def save_user(db: Session, user_in: schemas.UserIn):
    hashed_password = password_hasher(user_in.password)
    db_user = models.User(username=user_in.username, hashed_password=hashed_password.decode())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user        

def update_user(db: Session, username: str, new_rating: int, new_top_percentage: float):
    user: models.User = db.query(models.User).filter(models.User.username == username).first()
    user.rating = new_rating
    user.top_percentage = new_top_percentage
    db.add(user)
    return {'ok': True}

def get_users(db: Session):
    return db.query(models.User).order_by(desc(models.User.rating)).all()

def get_usernames(db: Session):
    return list(map(lambda user: user.username, get_users(db)))

def remove_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()
    return True
