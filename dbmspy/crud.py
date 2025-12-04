from .database import sessionlocal, Password
from sqlalchemy import select
from .models import User, CodeConfirm
from sqlalchemy.exc import NoResultFound
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
        print(f"DEBUG: Starting delete_user for {email}")
        
        # ВАРИАНТ 1: Удаление через execute (рекомендуется для async)
        try:
            async with sessionlocal() as session:
                from sqlalchemy import delete
                
                # Создаем DELETE запрос
                stmt = delete(User).where(
                    User.email == email
                )
                
                # Выполняем запрос
                result = await session.execute(stmt)
                
                # Получаем количество удаленных строк
                rows_deleted = result.rowcount
                print(f"DEBUG: Rows deleted: {rows_deleted}")
                
                # Коммитим изменения
                await session.commit()
                
                if rows_deleted > 0:
                    return {"success": True, "msg": "user deleted", "rows": rows_deleted}
                else:
                    return {"success": False, "msg": "User not found or credentials incorrect"}
                    
        except Exception as e:
            print(f"DEBUG: Error: {str(e)}")
            return {"success": False, "msg": f"Error: {str(e)}"}
        
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
                            