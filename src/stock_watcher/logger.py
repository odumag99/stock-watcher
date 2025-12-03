import os
from datetime import datetime
from logging import FileHandler, Formatter, Logger, StreamHandler, getLogger
from pathlib import Path

LOGGER_NAME = "stock_watcher_logger"

def get_stock_watcher_logger() -> Logger:
    logger = getLogger(LOGGER_NAME)
    if logger.hasHandlers():
        return logger
    
    logger.setLevel("DEBUG")

    # Create file handler
    log_file_name = f"{LOGGER_NAME}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    log_file_path = Path(os.getcwd()) / "logs" / log_file_name
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    # log_file_path
    file_handler = FileHandler(log_file_path)
    file_handler.setLevel("DEBUG")
    formatter = Formatter('[%(levelname)s] %(asctime)s - %(filename)s:%(lineno)d - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create console handler
    console_handler = StreamHandler()
    console_handler.setLevel("INFO")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = get_stock_watcher_logger()

