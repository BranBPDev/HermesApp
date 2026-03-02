import logging
import sys
from logging.handlers import RotatingFileHandler
from app.utils.paths_util import MAIN_LOG_PATH

class HermesLogger:
    _loggers = {}

    @staticmethod
    def get_logger(name: str = "SYSTEM"):
        if name in HermesLogger._loggers:
            return HermesLogger._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        if not logger.handlers:
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            
            # Rotación: 5MB por archivo, máximo 5 backups
            file_handler = RotatingFileHandler(MAIN_LOG_PATH, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)

            logger.addHandler(file_handler)

        HermesLogger._loggers[name] = logger
        return logger

sys_log = HermesLogger.get_logger("SYSTEM")