from authx import AuthX, AuthXConfig
import config

authconfig = AuthXConfig()
authconfig.JWT_SECRET_KEY = config.settings.jwt_secret_key
authconfig.JWT_ACCESS_COOKIE_NAME = "my_access_token"
authconfig.JWT_TOKEN_LOCATION = ["cookies"]
authconfig.JWT_COOKIE_CSRF_PROTECT = False

security=AuthX(config=authconfig)

