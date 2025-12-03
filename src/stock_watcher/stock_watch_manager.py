import asyncio
from typing import List

from .logger import logger
from .watcher import Watcher
from .watch_result import WatchResult

class StockWatchManager:
    def __init__(self, watchers: List[type[Watcher]]):
        self.watchers = watchers

    async def dispatch(self):
        tasks = []
        for watcher in self.watchers:
            task = asyncio.create_task(watcher().watch()) 
            tasks.append(task)
        
        async for task in asyncio.as_completed(tasks):
            try:
                result: WatchResult = await task
            except Exception as e:
                logger.error(f"WatchResult 수신 실패: {e}")
                continue
            logger.info(f"WatchResult 수신 - {result.korean_name}({result.stock_symbol}) {result.message}")

            try:
                await self._hand_over_to_notifier(result)
            except Exception as e:
                logger.error("알림 발송 실패: %s", e, exc_info=True)

    async def _hand_over_to_notifier(self, watch_result):
        from .notifier import Notifier
        notifier = Notifier(watch_result)
        await notifier.execute()
            
            

        


