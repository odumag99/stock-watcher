from datetime import datetime

from stock_watcher.watcher import Watcher
from stock_watcher.watch_result import WatchResult
from stock_watcher.price_getter import PriceGetter

class GoogleWatcher(Watcher):
    stock_symbol: str = "GOOGL"
    korean_name: str = "알파벳(구글)"
    base_date: datetime = datetime.strptime("2025-12-02", "%Y-%m-%d")
    base_price: int = 295
    growth_rate: float = 1.0047

    async def watch(self) -> WatchResult:
        criteria_price = await self._get_criteria_price()
        recent_price = await self._get_recent_price()
        should_notify = recent_price < criteria_price
        message = f"""최근 최저 가격: {recent_price:,.3f}
기준 가격: {criteria_price:,.3f}
기준 미달 여부: {should_notify}"""
        
        return WatchResult(
            datetime=datetime.now(),
            should_notify=should_notify,
            stock_symbol=self.stock_symbol,
            korean_name=self.korean_name,
            message=message,
        )

    @classmethod
    async def _get_criteria_price(cls) -> float:
        today = datetime.now()
        days = (today - cls.base_date).days
        return cls.base_price * (cls.growth_rate ** days)

    @classmethod
    async def _get_recent_price(cls) -> float:
        return await PriceGetter(cls.stock_symbol).get_recent_price()