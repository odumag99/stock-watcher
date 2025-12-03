import asyncio
from datetime import datetime, timedelta

class PriceGetter:
    def __init__(self, stock_symbol: str):
        self.stock_symbol = stock_symbol
    
    async def get_recent_price(self) -> float:
        import yfinance as yf
        yf_fail_count = 0
        
        while True:
            try:
                yf_ticker = await asyncio.to_thread(yf.Ticker, self.stock_symbol)
                break
            except Exception as e:
                yf_fail_count += 1

                if yf_fail_count > 5:
                    print("yfinance에서 티커 생성 5회 실패, 종료합니다.")
                    raise e
                
                print(f"yfinance에서 티커 생성 실패: {e}, {yf_fail_count}회 재시도 중...")
                await asyncio.sleep(1)

        yf_fail_count = 0
        interval = timedelta(hours=1)
        start_datetime = datetime.now() - interval
        
        while True:
            try:
                history = await asyncio.to_thread(yf_ticker.history, interval='1h', start=start_datetime)
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
                await asyncio.sleep(1)
                
        return history.iloc[-1].loc['Low']
