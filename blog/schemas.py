from pydantic import BaseModel, EmailStr

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: str | None = None

class ArticleBase(BaseModel):
  title: str
  content: str

class ArticleCreate(ArticleBase):
  username: str

class Article(ArticleBase):
  id: int

  class Config:
    from_attributes = True

class UserBase(BaseModel):
  username: str
  email: EmailStr

class UserLogin(BaseModel):
  username: str
  password: str

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
