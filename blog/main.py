from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, models, crud, database
import uvicorn
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from .database import SessionLocal, engine
from passlib.context import CryptContext
from enum import Enum
from typing import Union
models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()


#Sequrty
SECRET_KEY = "verylongsecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_schemas = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


def verify_password(password, hashed_password):
  return pwd_context.verify(
    password, hashed_password)


def authenticate_user(db, username: str, password: str):
  user = crud.get_username(db, username=username)
  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc)+ expires_delta
    print(expire)
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    print(expire)

  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  print(encoded_jwt)
  return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_schemas), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    token_data = schemas.TokenData(username=username)
  except JWTError:
    raise credentials_exception
  user = crud.get_username(db, username=token_data.username)
  
  if user is None:
    raise credentials_exception
  return user


#Routs
@app.post("/login", include_in_schema=False)
def login_for_get_salary(
  db: Session = Depends(get_db),
  form_data: OAuth2PasswordRequestForm = Depends()
):
  user = authenticate_user(db, form_data.username, form_data.password)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"}
    )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    data={"sub": user.username}, expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}



@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  hashed_password = pwd_context.hash(user.password)
  return crud.create_user(db=db, user=user, hashed_password=hashed_password)


@app.get("/users/", response_model=list[schemas.User])
def read_users(user: schemas.UserLogin = Depends(get_current_user), db: Session = Depends(get_db)):
  users = crud.get_users(db)
  return users

@app.get("/articles/", response_model=list[schemas.Article])
def read_articles(user: schemas.UserLogin = Depends(get_current_user), db: Session = Depends(get_db)):

  articles = crud.get_articles_by_username(db, user.username)
  return articles

# class Color(Enum):
#   def __init__(self, db: Session = Depends(get_db)) -> list:
#     articles = crud.get_articles(db)
#     res = [a.title for a in articles]
#     return res

  # def get_titles():
  #   return articles
  # art = get_titles
  # print(art)

Color = Enum('Color', ['RED', 'GREEN', 'BLUE'])


@app.patch("/article/{title}")
def edit_article(
  title: Union[str],
  user: schemas.UserLogin = Depends(get_current_user),
  db: Session = Depends(get_db),
):

  articles = crud.get_articles_by_username(db, user.username)

  return articles




@app.post("/articles/", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
  return crud.add_article(db=db, article=article)


# @app.post("/login", response_model=schemas.UserBase)
# def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
#   db_user = crud.get_username(db, username = user.username)
#   if db_user is None:
#     raise HTTPException(status_code=401, detail="wrong username or password")
#   if not crud.verify_password(user.password, db_user.hashed_password):
#     raise HTTPException(status_code=401, detail="wrong username or password")

#   return schemas.UserBase(username=db_user.username, email=db_user.email)












# if __name__ == "__main__":
#   uvicorn.run(app, host="0.0.0.0", port=8000)
