from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from .models import Base,User,CodeConfirm
from sqlalchemy import select
import config
import asyncio

engine=create_async_engine(
    url=config.settings.database_url
)

sessionlocal=async_sessionmaker(bind=engine)

async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

class UserActions:
    @staticmethod
    async def email_is_busy(email:str):
        async with sessionlocal() as session:
            result = await session.execute(
                select(User)
                .where(User.email==email)
                .limit(1)
            )
            user = result.scalar_one_or_none()
            if user:
                return {"msg":"email is busy", "employment":True}
            return {"msg":"email is not busy", "employment":False}
        
    @staticmethod
    async def find_user(email:str, password:str):
        async with sessionlocal() as session:
            result= await session.execute(
                select(User)
                .where(User.email==email, User.password==password)
            )
            user=result.scalar_one_or_none()
            if user:
                return {"msg":"user found", "user_id":user.id}
            return {"msg":"user not found", "user_id":None}
     
    @staticmethod
    async def add_user(email:str, password:str):
        new_user=User(
            email=email,
            password=password
        )
        
        async with sessionlocal() as session:
            session.add(new_user)  
            await session.commit()
        return {"msg":"user added"}
    
    @staticmethod
    async def delete_user(email: str, password: str):
        deletable_user = User(
            email=email,
            password=password
        )
        
        async with sessionlocal() as session:
            session.delete(deletable_user)
            await session.commit()
        return {"msg":"user deleted"}
            

class CodeActions:
    @staticmethod
    async def add_conf_code(email:str, code:str):
        new_conf_code = CodeConfirm(
            email = email,
            code = code
        )
        
        async with sessionlocal() as session:
            session.add(new_conf_code)
            await session.commit()
        return {"msg":"ok"}
    
    @staticmethod
    async def find_conf_code(email:str):
        async with sessionlocal() as session:
            result = await session.execute(
                select(CodeConfirm)
                .where(CodeConfirm.email==email)
                .order_by(CodeConfirm.id.desc())
                .limit(1)
            )
            
            code = result.scalar_one_or_none()
            return {"msg":"code found", "conf_code":code.code}
        
    