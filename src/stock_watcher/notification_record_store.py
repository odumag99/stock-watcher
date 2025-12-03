import json
import asyncio
from datetime import datetime, timezone, timedelta
import os
from pathlib import Path

from .db import get_db_session, AsyncSession, NotificationRecord
from sqlalchemy import select

FILE_PATH = Path(os.getcwd()).parent / "notification_records.json"
KST = timezone(timedelta(hours=9))

class NotificationRecordNotFoundException(Exception):
    pass

class NotificationRecordStore:
    @classmethod
    async def get_last_notification_datetime(cls, stock_symbol: str) -> datetime:
        session_gen = get_db_session()
        
        session: AsyncSession = await anext(session_gen)
        
        record = await session.scalar(
            select(NotificationRecord)
            .where(NotificationRecord.stock_symbol == stock_symbol)
        )

        if record is None:
            raise NotificationRecordNotFoundException(f"{stock_symbol}에 대해 저장된 알림 기록이 없습니다.")
        
        try:
            await anext(session_gen)
        except StopAsyncIteration:
            pass
        
        return record.last_notified_datetime
    
    @classmethod
    async def update_notification_record(cls, stock_symbol: str):
        session_gen = get_db_session()
        
        session: AsyncSession = await anext(session_gen)
        
        record = await session.scalar(
            select(NotificationRecord)
            .where(NotificationRecord.stock_symbol == stock_symbol)
        )

        if record is None:
            record = NotificationRecord(
                stock_symbol=stock_symbol,
            )
            session.add(record)
        
        record.last_notified_datetime = datetime.now(tz=KST)

        await session.commit()
        try:
            await anext(session_gen)
        except StopAsyncIteration:
            pass