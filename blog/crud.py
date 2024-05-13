from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException


# def verify_password(password, hashed_password):
#   return pwd_context.verify(
#     password, hashed_password)


def get_username(db: Session, username: str):
  return db.query(models.User).filter(models.User.username == username).first()
  
def get_users(db: Session):
  users = db.query(models.User).all()
  return users

def get_articles(db: Session):
  articles = db.query(models.Article).all()
  return articles

def get_articles_by_username(db: Session, username: str):
  author_id = db.query(models.User).filter(models.User.username == username).first()
  if author_id is None:
    raise HTTPException(status_code=404, detail="Username not found")
  articles = db.query(models.Article).filter(models.Article.author_id == author_id.id)
  return articles

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
  db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

def add_article(db: Session, article: schemas.ArticleCreate):

  author_id = db.query(models.User).filter(models.User.username == article.username).first()
  if author_id is None:
    raise HTTPException(status_code=404, detail="Username not found")
  db_article = models.Article(title=article.title, content=article.content, author_id=author_id.id)
  db.add(db_article)
  db.commit()
  db.refresh(db_article)
  return db_article