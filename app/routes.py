from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, models, crud
from app.auth import get_db, get_current_user, create_tokens, get_user_by_username
from app.utils import get_password_hash, verify_password

router = APIRouter()

@router.post("/register", response_model=schemas.UserRead)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = get_password_hash(user.password)
    return crud.create_user(db, user, hashed)

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token, refresh_token = create_tokens(user.username)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.get("/tasks", response_model=list[schemas.TaskRead])
def read_tasks(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_tasks(db, current_user.id)

@router.post("/tasks", response_model=schemas.TaskRead)
def create_task(task: schemas.TaskCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_task(db, task, current_user.id)

@router.put("/tasks/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, task: schemas.TaskCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    updated = crud.update_task(db, task_id, task, current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not crud.delete_task(db, task_id, current_user.id):
        raise HTTPException(status_code=404, detail="Task not found")