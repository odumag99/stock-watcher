import asyncio

from stock_watcher.stock_watch_manager import StockWatchManager

from watchers.google_watcher import GoogleWatcher
from watchers.samsung_electronics_watcher import SamsungElectronicsWatcher
from watchers.tesla_buy_watcher import TeslaBuyWatcher
from watchers.tesla_sell_watcher import TeslaSellWatcher
from watchers.msft_buy_watcher import MSFTBuyWatcher
from watchers.msft_sell_watcher import MSFTSellWatcher

async def main():
    manager = StockWatchManager(
        [
            GoogleWatcher, SamsungElectronicsWatcher,
            TeslaBuyWatcher, TeslaSellWatcher,
            MSFTBuyWatcher, MSFTSellWatcher
        ]
    )

    await manager.dispatch()

if __name__ == "__main__":
    asyncio.run(main())