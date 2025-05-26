from pydantic import BaseModel
from typing import Optional, List

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"