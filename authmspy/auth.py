from authx import AuthX, AuthXConfig
from passlib.context import CryptContext
import config

authconfig = AuthXConfig()
authconfig.JWT_SECRET_KEY = config.settings.jwt_secret_key
authconfig.JWT_ACCESS_COOKIE_NAME = "my_access_token"
authconfig.JWT_TOKEN_LOCATION = ["cookies"]
authconfig.JWT_COOKIE_CSRF_PROTECT = False

security=AuthX(config=authconfig)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(self,password: str) -> str:
    return pwd_context.hash(password)