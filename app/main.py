from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router
from app.routes_refresh import router as refresh_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task O'Auth 2 Do")
app.include_router(router)
app.include_router(refresh_router)