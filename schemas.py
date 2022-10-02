from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str
    rating: int | None = None
    top_percentage: float | None = None

    class Config:
        orm_mode = True

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    rating: int
    top_percentage: float
