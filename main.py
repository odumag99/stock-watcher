import asyncio

from stock_watcher.stock_watch_manager import StockWatchManager

from watchers.google_watcher import GoogleWatcher
from watchers.samsung_electronics_watcher import SamsungElectronicsWatcher
from watchers.tesla_buy_watcher import TeslaBuyWatcher
from watchers.tesla_sell_watcher import TeslaSellWatcher

async def main():
    manager = StockWatchManager(
        [GoogleWatcher, SamsungElectronicsWatcher, TeslaBuyWatcher, TeslaSellWatcher]
    )

    await manager.dispatch()

if __name__ == "__main__":
    asyncio.run(main())