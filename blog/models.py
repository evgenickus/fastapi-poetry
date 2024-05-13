from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  hashed_password = Column(String)
  is_active = Column(Boolean, default=True)

  articles = relationship("Article", back_populates="author")
  comments = relationship("Comment", back_populates="owner")


class Article(Base):
  __tablename__ = "articles"
  
  id = Column(Integer, primary_key=True)
  title = Column(String, index=True)
  content = Column(Text)
  author_id = Column(Integer, ForeignKey("users.id"))

  author = relationship("User", back_populates="articles")

class Comment(Base):
  __tablename__ = "comments"

  id = Column(Integer, primary_key=True)
  content = Column(Text)
  article_id = Column(Integer, ForeignKey("articles.id"))
  owner_id = Column(Integer, ForeignKey("users.id"))

  owner = relationship("User",  back_populates="comments")



