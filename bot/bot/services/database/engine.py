from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


BASE_URL = ""

engine = create_async_engine(
    url=BASE_URL,
    max_overflow=5,
)



async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
