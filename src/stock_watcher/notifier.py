from datetime import datetime, timedelta, timezone
import os

from dotenv import load_dotenv

from .watch_result import WatchResult
from .stock_mapper import STOCK_MAPPER
from .logger import logger

load_dotenv()

NOTIFICATION_MIN_INTERVAL = timedelta(hours=23, minutes=59)
NOTIFICATION_TO_EMAIL_ADDRESS = os.getenv("NOTIFICATION_TO_EMAIL_ADDRESS") # pyright: ignore[reportAssignmentType]
assert NOTIFICATION_TO_EMAIL_ADDRESS is not None, "환경 변수 NOTIFICATION_TO_EMAIL_ADDRESS가 설정되어 있지 않습니다."
NOTIFICATION_TO_EMAIL_ADDRESS: str

class Notifier:
    def __init__(self, watch_result):
        self.watch_result: WatchResult = watch_result

    async def execute(self):
        if not self.watch_result.should_notify:
            logger.info(f"{self.watch_result.korean_name} 기준에 미치지 못해 알림을 보내지 않습니다.")
            return
        
        if not await self._should_send_notification():
            logger.info(f"{self.watch_result.korean_name} 최근 알림 이후 최소 알림 간격 이내로 알림을 보내지 않습니다.")
            return
        
        await self._send_notification()
        logger.info(f"{self.watch_result.korean_name} 알림을 보냈습니다.")

    async def _should_send_notification(self) -> bool:
        from .notification_record_store import NotificationRecordNotFoundException
        try:
            last_notified_datetime = await self._get_last_notified_datetime()
        except NotificationRecordNotFoundException:
            return True
        
        now = datetime.now()

        if now - last_notified_datetime < NOTIFICATION_MIN_INTERVAL:
            return False
        return True
    
    async def _get_last_notified_datetime(self) -> datetime:
        from .notification_record_store import NotificationRecordStore
        return await NotificationRecordStore().get_last_notification_datetime(
            self.watch_result.stock_symbol
        )

    async def _send_notification(self):
        from .mail_sender import MailSender
        from .notification_record_store import NotificationRecordStore

        stock_korean_name = self.watch_result.korean_name
        subject = f"[Stock Watcher] {stock_korean_name} 주가 알림"

        kst = timezone(timedelta(hours=9))
        now = datetime.now(tz=kst)
        body = f"""현재 시각: {now.strftime('%Y-%m-%d %H:%M:%S')}
{self.watch_result.message}
"""
        to = NOTIFICATION_TO_EMAIL_ADDRESS

        mail_sender = MailSender()
        await mail_sender.send_mail(
            subject=subject,
            body=body,
            to=to,
        )

        await NotificationRecordStore().update_notification_record(
            stock_symbol=self.watch_result.stock_symbol
        )

        


