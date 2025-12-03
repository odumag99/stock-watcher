from abc import ABC, abstractmethod
from datetime import datetime

from .watch_result import WatchResult

class Watcher(ABC):

    @abstractmethod
    async def watch(self) -> WatchResult:
        ...