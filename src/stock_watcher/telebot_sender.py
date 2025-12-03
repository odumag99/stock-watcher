from dotenv import load_dotenv
import os

from .logger import logger

load_dotenv()

TELEBOT_RETRY_MAX_COUNT = 5

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # pyright: ignore[reportAssignmentType]
assert TELEGRAM_BOT_TOKEN is not None, "환경 변수 TELEGRAM_BOT_TOKEN가 설정되어 있지 않습니다."

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # pyright: ignore[reportAssignmentType]
assert TELEGRAM_CHAT_ID is not None, "환경 변수 TELEGRAM_CHAT_ID가 설정되어 있지 않습니다."

class TelebotSender:
    async def send_message(self, message: str):
        from httpx import AsyncClient
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = dict(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )
        retry = 0
        while True:
            try:
                async with AsyncClient() as client:
                    response = await client.post(url, data=payload)
                    response.raise_for_status()
                logger.debug("텔레그램 메시지 전송 성공: %s", response.text)
                return
            except Exception as e:
                retry += 1
                logger.error("텔레그램 메시지 %d회 전송 실패: ", retry)
                if retry > TELEBOT_RETRY_MAX_COUNT:
                    logger.error("텔레그램 메시지 전송 최대 재시도 횟수 초과로 종료합니다.", exc_info=True)
                    raise e
            
            