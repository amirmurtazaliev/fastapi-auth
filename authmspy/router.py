import random 
from fastapi import Depends, APIRouter, Response, HTTPException
from .schemes import User, UserEmail, UserWithCode
from .auth import security, authconfig
from .verif import send_confirmation_code
from .http_client import DBHTTPClient

router = APIRouter(prefix="/auth", tags=["auth"])

db_client = DBHTTPClient("http://127.0.0.1:8000/database/")

@router.post("/auth/check_email")
async def check_email(user_email:UserEmail):
    params = {
        "email": user_email.email
        }
    
    data = await db_client.send_post_request(
        endpoint_url = "check_email",
        json = params
        )
    
    if data["employment"] is False:
        code = random.randint(1000,9999)
        send_confirmation_code(user_email.email,code)
        params_with_code = {
            "email": user_email.email,
            "code": str(code)
        }
        await db_client.send_post_request(
            endpoint_url = "add_confirm_code",
            json = params_with_code
            )
        
    else:
        return {"msg":"this email is busy"}

@router.post("/auth/register")
async def register(user:UserWithCode):
    params = {
        "email": user.email,
        "password": user.password
        }
    
    data = await db_client.send_post_request(
        endpoint_url = "find_confirm_code",
        json = params
        )
    
    if data["conf_code"] != user.code:
        return {"msg":"неверный код"}
        
    await db_client.send_post_request(
        endpoint_url = "add_user",
        json = params
        )

@router.post("/auth/login")
async def login(user:User, createcookie:Response):
    params = {
        "email": user.email,
        "password": user.password
        }
    
    data = await db_client.send_post_request(
        endpoint_url = "check_user",
        json = params
        )
    
    if data["user_id"] is not None:
        token=security.create_access_token(uid=str(data["user_id"]))
        createcookie.set_cookie(authconfig.JWT_ACCESS_COOKIE_NAME,token)
        return data
    
    raise HTTPException(
        status_code=401,
        detail="incorrect email or password"
        )

@router.post("/auth/logout",
             dependencies = [Depends(
                 security.access_token_required)])
async def logout(response: Response):
    response.delete_cookie(key="my_access_token")
    return {'msg': 'Пользователь успешно вышел из системы'}

@router.delete("/auth/delete_user")
async def delete_user(user: User):
    params = {
        "email": user.email,
        "password": user.password
        }
    await db_client.send_delete_request(
        endpoint_url = "delete_user",
        json = params
    )