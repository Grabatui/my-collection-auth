import logging
import os
import datetime
import time
from logging import FileHandler
from pythonjsonlogger import jsonlogger
from flask_log_request_id import current_request_id


startTime = time.strftime('%H.%M.%S')


class Logger():
    def __init__(self, name: str, rootPath: str) -> None:
        self.__name = name
        self.__rootPath = rootPath
        self.__logger = self.__makeLogger()

    def addInfo(self, message: str = '', data: dict = {}):
        self.__logger.info(message, extra=data)

    def addError(self, message: str = '', data: dict = {}):
        self.__logger.error(message, extra=data)

    def __makeLogger(self) -> logging.Logger:
        logger = logging.getLogger(self.__name)
        logger.level = logging.DEBUG

        logFullPath = self.__getDateTimeLogPath()
        logHandler = FileHandler(logFullPath)
        
        logFormatter = jsonlogger.JsonFormatter(timestamp=True)
        
        logHandler.setFormatter(logFormatter)
        
        logger.addHandler(logHandler)

        return logger

    def __getDateTimeLogPath(self) -> str:
        path = os.path.join(
            self.__rootPath,
            'logs',
            datetime.datetime.now().strftime('%Y-%m-%d')
        )

        if not os.path.isdir(path):
            os.makedirs(path)

        return os.path.join(path, '{}.{}.log'.format(startTime, current_request_id()))
