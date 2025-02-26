from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from bot.services.core.config.config import options

BASE_URL = options.DB_BOT_LINK

engine = create_async_engine(
    url=BASE_URL,
    echo=True,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
