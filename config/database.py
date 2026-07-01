from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection

DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/board";
#DATABASE_URL = "mysql+aiomysql://root:123456@localhost:5000/board";

# Engine 설정
engine = create_async_engine(DATABASE_URL, echo=True, pool_pre_ping=True);

# db 커넥션 의전송 주입 함수
async def get_db() -> AsyncGenerator[AsyncConnection, None]:
    async with engine.begin() as conn:
        yield conn

