from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from typing import List
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
  users = crud.get_users(db)
  return users

# if __name__ == "__main__":
#   uvicorn.run(app, host="0.0.0.0", port=8000)

