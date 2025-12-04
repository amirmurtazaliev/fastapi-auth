from fastapi import FastAPI
from .crud import UserActions, CodeActions
from .schemes import User, UserEmail, CodeConfirm
import uvicorn 

app = FastAPI()

useracts = UserActions()
codeacts = CodeActions()

@app.post("/database/add_user")
async def add_user(user: User): 
    result = await useracts.add_user(
        email = user.email,
        password = user.password
    )
    return result

@app.delete("/database/delete_user")
async def delete_user(user: User):
    result = await useracts.delete_user(
        email = user.email,
        password = user.password
    )
    return result

@app.post("/database/check_user")
async def check_user(user:User):
    result = await useracts.find_user(
        email = user.email,
        password = user.password
    )
    return result

@app.post("/database/check_email")
async def check_email(user_email: UserEmail):
    result = await useracts.email_is_busy(user_email.email)
    return result 

@app.post("/database/add_confirm_code")
async def add_code(params: CodeConfirm):
    result = await codeacts.add_conf_code(
        email = params.email,
        code = params.code
    )
    return result

@app.post("/database/find_confirm_code")
async def find_code(user_email: UserEmail):
    result = await codeacts.find_conf_code(user_email.email)
    return result 
