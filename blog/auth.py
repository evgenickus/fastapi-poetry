# from fastapi.security import OAuth2PasswordBearer#, OAuth2PasswordRequestForm
# from fastapi import Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from jose import JWTError, jwt
# from datetime import datetime, timedelta, timezone
# from . import crud, schemas, database
# from .database import SessionLocal, engine


# def get_db():
#   db = database.SessionLocal()
#   try:
#     yield db
#   finally:
#     db.close()


# SECRET_KEY = "069d25e094faa6ca2556c8189d25e094faa6ca2556c818116b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# def authenticate_user(db: Session, username: str, password: str):
#   user = crud.get_username(db, username)
#   if not user:
#     return False
#   if not crud.verify_password(password, user.hashed_password):
#     return False
  
#   return user

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#   to_encode = data.copy()
#   if expires_delta:
#     expire = datetime.now(timezone.utc) + expires_delta
#   else:
#     expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#   to_encode.update({"exp": expire})
#   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#   return encoded_jwt

# async def get_current_user(db: Session, token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = crud.get_username(db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user