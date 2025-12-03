import os
import aiosmtplib
from email.message import EmailMessage

FROM_EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # 본인 주소
FROM_EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")  # 생성한 앱 비밀번호
assert FROM_EMAIL_ADDRESS is not None, "환경 변수 EMAIL_ADDRESS가 설정되어 있지 않습니다."
assert FROM_EMAIL_APP_PASSWORD is not None, "환경 변수 EMAIL_APP_PASSWORD가 설정되어 있지 않습니다."

class MailSender:
    def __init__(self):
        pass
    
    async def send_mail(self, subject: str, body: str, to: str):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL_ADDRESS
        msg["To"] = to
        msg.set_content(body)

        await aiosmtplib.send(
            msg,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=FROM_EMAIL_ADDRESS,
            password=FROM_EMAIL_APP_PASSWORD,
        )