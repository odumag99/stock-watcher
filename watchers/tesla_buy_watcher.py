from datetime import datetime, timedelta, timezone

from stock_watcher.price_getter import PriceGetter
from stock_watcher.watcher import Watcher
from stock_watcher.watch_result import WatchResult
from stock_watcher.logger import logger

KST = timezone(timedelta(hours=9))

class TeslaBuyWatcher(Watcher):
    def __init__(self):
        self.stock_symbol: str = "TSLA"
        self.korean_name: str = "테슬라"
        
    async def watch(self) -> WatchResult:
        current_price = await self._get_current_price()
        threshold_price = await self._get_threshold_price()

        should_notify = current_price <= threshold_price
        
        if should_notify:
            message = f"""\
[Tesla 매수 알림]
매수 권장 타이밍입니다.
현재 가격: {current_price:,.2f}
기준 가격: {threshold_price:,.2f}
알림 여부: {should_notify}"""
        else:
            message = f"[Tesla 매수 알림] 현재 가격 - {current_price:,.2f}, 기준 가격 - {threshold_price:,.2f}, 알림 여부 - False"
        
        return WatchResult(
            datetime=datetime.now(tz=KST),
            should_notify=should_notify,
            stock_symbol=self.stock_symbol,
            korean_name=self.korean_name,
            message=message,
        )
    
    async def _get_current_price(self) -> float:
        return await PriceGetter(self.stock_symbol).get_recent_price()
    
    async def _get_threshold_price(self) -> float:
        base_price = 407.55
        baseday = datetime.strptime("2025-12-01", "%Y-%m-%d")
        now = datetime.now()
        diff_days = (now - baseday).days
        growth_rate = 1.003
        return base_price * (growth_rate ** diff_days)

