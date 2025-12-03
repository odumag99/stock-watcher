import json
import asyncio
import os
from pathlib import Path
from fcntl import flock, LOCK_EX, LOCK_UN

FILE_PATH = Path(os.getcwd()).parent / "notification_records.json"

class NotificationRecordStore:
    # 싱글톤 패턴
    _instance = None
    _instance_lock = asyncio.Lock()
    
    @classmethod
    async def get_instance(cls):    
        if cls._instance is not None:
            return cls._instance
        
        async with cls._instance_lock:
            if cls._instance is None:
                cls._instance = cls()
                await cls._instance._ainit()
        return cls._instance

    def __init__(self):
        pass

    async def _ainit(self):
        self._records = None
        self._records_lock = asyncio.Lock()
        self._file_path = FILE_PATH
        self._file_lock = asyncio.Lock()

        async with self._file_lock:
            with self._file_path.open("r+") as f:
                self._records = json.load(f)

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._write_records_to_file()
        if exc_type is not None:
            raise exc_value

    async def get_last_notification_datetime(self, stock_symbol: str):


    async def update_notification_datetime(self, stock_symbol: str, notified_datetime: datetime):
        self.records[stock_symbol] = {
            "last_notified_datetime": notified_datetime.isoformat()
        }
        with self.FILE_PATH.open("r+") as f:
            flock(f, LOCK_EX)
            try:
                f.seek(0)
                f.write(json.dumps(self.records, indent=4))
                f.truncate()
            finally:
                flock(f, LOCK_UN)