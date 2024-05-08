from pydantic import BaseModel, EmailStr

class ArticleBase(BaseModel):
  title: str
  content: str

class ArticleCreate(ArticleBase):
  author_id: int

class Article(ArticleBase):
  id: int

  class Config:
    from_attributes = True

class UserBase(BaseModel):
  email: EmailStr

class UserCreate(UserBase):
  password: str

class User(UserBase):
  id: int
  is_active: bool
  
  class Config:
    from_attributes = True


class CommentBase(BaseModel):
  content: str

class CommentCreate(CommentBase):
  article_id: int
  owner_id: int

class Comment(CommentBase):
  id: int

  class Config:
    from_attributes = True