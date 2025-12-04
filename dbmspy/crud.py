from .database import sessionlocal, Password
from sqlalchemy import select
from .models import User, CodeConfirm

pwdacts = Password()

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
                .where(User.email==email)
            )
            
            user=result.scalar_one_or_none()
            if user and pwdacts.verify_password(password, user.password):
                return {"msg":"user found", "user_id":user.id}
            return {"msg":"user not found", "user_id":None}
     
    @staticmethod
    async def add_user(email:str, password:str):
        new_user=User(
            email=email,
            password=pwdacts.get_password_hash(password)
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
        
        if UserActions.find_user(email, password)["user_id"] is not None:
            async with sessionlocal() as session:
                session.delete(deletable_user)
                await session.commit()
                return {"msg":"user deleted"}
        return {"msg":"user not found"}
            

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
                            