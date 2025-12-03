import asyncio

from stock_watcher.stock_watch_manager import StockWatchManager

from watchers.google_watcher import GoogleWatcher
from watchers.samsung_electronics_watcher import SamsungElectronicsWatcher

async def main():
    manager = StockWatchManager(
        [GoogleWatcher, SamsungElectronicsWatcher]
    )

    await manager.dispatch()

if __name__ == "__main__":
    asyncio.run(main())