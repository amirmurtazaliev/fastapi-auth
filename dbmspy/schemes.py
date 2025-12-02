from pydantic import BaseModel,EmailStr,Field

class Base(BaseModel):
    pass 

class User(Base):
    email:EmailStr = Field(max_length=50)
    password:str = Field(min_length=5,max_length=30)
    
class UserEmail(Base):
    email:EmailStr = Field(max_length=50)
    
class CodeConfirm(Base):
    email:EmailStr = Field(max_length=50)
    code:str
    