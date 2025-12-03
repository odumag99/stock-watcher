from datetime import datetime, timedelta
from time import sleep
from dotenv import load_dotenv
import smtplib
import os
from email.message import EmailMessage

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # TLS
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # 본인 주소
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")  # 생성한 앱 비밀번호
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
RECENT_NOTIFICATION_DATETIME_FILE_PATH = "./RECENT_NOTIFICATION_DATETIME"

STOCK_SYMBOL = "005930.KS"  # 삼성전자
STOCK_NAME = "삼성전자"

assert EMAIL_ADDRESS is not None, "EMAIL_ADDRESS 환경변수가 설정되지 않았습니다."
assert EMAIL_APP_PASSWORD is not None, "EMAIL_APP_PASSWORD 환경변수가 설정되지 않았습니다."

def send_mail_to_me(subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS  # 나에게 보내기
    msg.set_content(body)

    # 1) 서버 접속
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        # 서버에게 "STARTTLS로 암호화하자" 요청
        smtp.starttls()
        # 2) 로그인
        smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        # 3) 메일 전송
        smtp.send_message(msg)

def get_recent_notification_datetime() -> datetime:
    with open(RECENT_NOTIFICATION_DATETIME_FILE_PATH, "r") as f:
        recent_notification_datetime_str = f.readline()
    recent_notification_datetime = datetime.strptime(recent_notification_datetime_str, DATETIME_FORMAT)
    return recent_notification_datetime

def get_recent_price(ticker: str) -> float:
    import yfinance as yf
    yf_fail_count = 0
    
    while True:
        try:
            yf_ticker = yf.Ticker(ticker)
            break
        except Exception as e:
            yf_fail_count += 1

            if yf_fail_count > 5:
                print("yfinance에서 티커 생성 5회 실패, 종료합니다.")
                raise e
            
            print(f"yfinance에서 티커 생성 실패: {e}, {yf_fail_count}회 재시도 중...")
            sleep(1)

    yf_fail_count = 0
    interval = timedelta(hours=1)
    start_datetime = datetime.now() - interval
    
    while True:
        try:
            history = yf_ticker.history(interval='1h', start=start_datetime)
            if history.empty:
                start_datetime -= interval
                continue
            else:
                break
        except Exception as e:
            yf_fail_count += 1

            if yf_fail_count > 5:
                print("yfinance에서 history 데이터 불러오기 5회 실패, 종료합니다.")
                raise e

            print(f"yfinance에서 history 데이터 불러오기 실패: {e}, {yf_fail_count}회 재시도 중...")
            sleep(1)
            
    return history.iloc[-1].loc['Low']

def get_criteria_price() -> float:
    # 기준 날짜
    base_day = datetime.strptime("2025-12-02", "%Y-%m-%d")
    today = datetime.now()
    days = (today - base_day).days
    return 100567 * (1.0008 ** (days))

def write_mail_body(present_price: float, criteria_price: float) -> str:
    return f"""{STOCK_NAME} 주식 알림

현재 시각: {datetime.now().strftime(DATETIME_FORMAT)}
최근 최저 가격: {present_price:,.0f}원
기준 가격: {criteria_price:,.0f}원
"""

def write_recent_notification_datetime(dt: datetime):
    with open(RECENT_NOTIFICATION_DATETIME_FILE_PATH, "w") as f:
        f.write(dt.strftime(DATETIME_FORMAT))

def main():
    present_price = get_recent_price(STOCK_SYMBOL)
    criteria_price = get_criteria_price()
    print(f"{datetime.now().strftime(DATETIME_FORMAT)} - {STOCK_NAME}({STOCK_SYMBOL}) 최근 최저 가격 {present_price:,.0f}원, 기준 가격 {criteria_price:,.0f}원", end="")

    if present_price >= criteria_price:
        print(" / 알림 조건 미충족")
        return

    try:
        recent_notification_datetime = get_recent_notification_datetime()
        if datetime.now() - recent_notification_datetime < timedelta(hours=23, minutes=59):
            print("최근 24시간 이내에 알림을 보냈으므로, 이번에는 보내지 않습니다.")
            return
    except Exception as e:
        print(f"최근 알림 일시를 불러오기 실패: {e}")


    mail_body = write_mail_body(present_price, criteria_price)
    send_mail_to_me(
        subject=f"{STOCK_NAME} 주식 알림",
        body=mail_body
    )
    write_recent_notification_datetime(datetime.now())
    
    return


if __name__ == "__main__":
    main()

