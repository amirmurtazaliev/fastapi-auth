from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

class Base(DeclarativeBase):
    pass
 
class User(Base):
    __tablename__="users"
    
    id:Mapped[int]=mapped_column(primary_key=True)
    email:Mapped[str]
    password:Mapped[str]
    
class CodeConfirm(Base):
    __tablename__ = "codes"
    
    id:Mapped[int] = mapped_column(primary_key = True)
    email:Mapped[str]
    code:Mapped[str]
    
