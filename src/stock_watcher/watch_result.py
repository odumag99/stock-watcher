from dataclasses import dataclass
from datetime import datetime

@dataclass
class WatchResult:
    datetime: datetime
    should_notify: bool
    stock_symbol: str
    korean_name: str
    message: str