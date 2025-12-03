import os
import asyncio
from pathlib import Path
from datetime import datetime
from sqlalchemy import TIMESTAMP, VARCHAR, inspect, Inspector
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


DB_FILE_NAME = "stock_watcher.db"
DB_FILE_PATH = Path(os.getcwd()) / DB_FILE_NAME
DB_FILE_PATH.touch(exist_ok=True)

CONNECTION_STRING = f"sqlite+aiosqlite:///{DB_FILE_PATH}"


class ORMBase(DeclarativeBase):
    def __repr__(self) -> str:
        cls = type(self)
        cls_name = cls.__name__
        mapper = cls.__mapper__
        attrs = mapper.column_attrs
        attr_strings = []
        for attr in attrs:
            name = attr.key
            value = getattr(self, name)
            attr_strings.append(f"{name}={value!r}")
        attr_str = ", ".join(attr_strings)
        return f"<{cls_name}({attr_str})>"
    
class NotificationRecord(ORMBase):
    __tablename__ = "notification_records"

    stock_symbol: Mapped[str] = mapped_column(VARCHAR(10), primary_key=True)
    last_notified_datetime: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

engine = create_async_engine(
    CONNECTION_STRING,
    echo=True,
)
make_session = async_sessionmaker(bind=engine)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(ORMBase.metadata.create_all)

try:
    loop = asyncio.get_running_loop()
    loop.create_task(init_db())
except RuntimeError:
    asyncio.run(init_db())

async def get_db_session():
    async with make_session() as session:
        yield session
