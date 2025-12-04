from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from .models import Base
from passlib.context import CryptContext
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
        
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Password:
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)