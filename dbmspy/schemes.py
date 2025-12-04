from pydantic import BaseModel,EmailStr,Field

class Base(BaseModel):
    pass 

class User(Base):
    email:EmailStr = Field(max_length=50)
    password:str
    
class UserEmail(Base):
    email:EmailStr = Field(max_length=50)
    
class CodeConfirm(Base):
    email:EmailStr = Field(max_length=50)
    code:str
    