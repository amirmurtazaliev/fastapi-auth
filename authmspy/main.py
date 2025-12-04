import uvicorn
import aiohttp
import random
from fastapi import FastAPI,Response,HTTPException
from .schemes import User,UserEmail,UserWithCode
from .auth import security, authconfig
from fastapi.middleware.cors import CORSMiddleware
from .verif import send_confirmation_code

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/check_email")
async def check_email(user_email:UserEmail):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://127.0.0.1:8000/database/check_email",
            json = {
                "email": user_email.email
            }
        ) as response:
            data = await response.json()
        if data["employment"] is False:
            code = str(random.randint(1000,9999))
            send_confirmation_code(user_email.email,code)
            async with session.post(
                "http://127.0.0.1:8000/database/add_confirm_code",
                json = {
                    "email": user_email.email,
                    "code": code
                } 
            ) as response:
                return await response.json()
        else:
            return {"msg":"this email is busy"}

@app.post("/auth/register")
async def register(user:UserWithCode):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://127.0.0.1:8000/database/find_confirm_code",
            json = {
                "email": user.email
            }
        ) as response:
            data = await response.json()
        if data["conf_code"] != user.code:
                return {"msg":"неверный код"}
            
        async with session.post(
            "http://127.0.0.1:8000/database/add_user",
            json = {
                "email": user.email,
                "password": user.password
            }
        ) as response:
            return await response.json()

@app.post("/auth/login")
async def login(user:User, createcookie:Response):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://127.0.0.1:8000/database/check_user",
            json = {
                "email": user.email,
                "password": user.password
            }
        ) as response:
            data = await response.json()
        print(data)
        if data["user_id"] is not None:
            token=security.create_access_token(uid=str(data["user_id"]))
            createcookie.set_cookie(authconfig.JWT_ACCESS_COOKIE_NAME,token)
            return data
        raise HTTPException(status_code=401,detail="incorrect email or password")

@app.post("/auth/delete_user")
async def delete_user(user: User):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://127.0.0.1:8000/database/delete_user",
            json = {
                "email": user.email,
                "password": user.password
            }
        ) as response:
            data = await response.json()
        return data