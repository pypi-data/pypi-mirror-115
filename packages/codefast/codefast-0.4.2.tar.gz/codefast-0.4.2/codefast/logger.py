# coding:utf-8
import inspect
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Any

import colorlog  # 控制台日志输入颜色

log_colors_config = {
    'DEBUG': 'white',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}


class Logger:
    def __init__(self, logname: str = '/tmp/codefast.log'):
        self._logname = logname
        self._lazy = True
        self._level = logging.DEBUG

    def __call__(self, *msg: Any) -> None:
        self.info(*msg)

    @property
    def level(self) -> str:
        return self._level

    @level.setter
    def level(self, level_name: str) -> str:
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        self._level = levels.get(level_name.upper(), logging.DEBUG)

    def lazy_init(self):
        self._lazy = False
        self.logger = logging.getLogger()
        self.logger.setLevel(self._level)
        self.formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(levelname)s]- %(message)s',
            log_colors=log_colors_config)

        if self.logger.hasHandlers():  # To above duplicated lines
            return

        # 创建一个 FileHandler，写到本地
        fh = logging.handlers.TimedRotatingFileHandler(self._logname,
                                                       when='MIDNIGHT',
                                                       interval=1,
                                                       encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,写到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

    @staticmethod
    def __get_call_info():
        stack = inspect.stack()
        cur = stack[3]
        fn, ln, func = cur[1:4]
        # fn = "..." + fn[-10:]  # Restrict file path length
        fn = os.path.basename(fn).rstrip('.py')
        return fn, func, ln

    def console(self, level: str, *message) -> None:
        if self._lazy:
            self.lazy_init()

        LV = {
            'debug': self.logger.debug,
            'info': self.logger.info,
            'warn': self.logger.warning,
            'warning': self.logger.warning,
            'error': self.logger.error,
            'critical': self.logger.critical
        }
        f = LV.get(level, self.debug)
        text = "[{}.{}-{}] {}".format(*self.__get_call_info(),
                                      ' '.join(map(str, message)))
        f(text)

    def debug(self, *message):
        self.console('debug', *message)

    def info(self, *message):
        self.console('info', *message)

    def warning(self, *message):
        self.console('warning', *message)

    def error(self, *message):
        self.console('error', *message)

    def critical(self, *message):
        self.console('critical', *message)

    def __repr__(self) -> str:
        d = {'level': self._level, 'logname': self._logname}
        return str(d)


def test():
    frames = inspect.stack()
    print(frames)
    Logger().info("Line 6666")


if __name__ == "__main__":
    log = Logger()
    log.info("测试1")
    log.debug("测试2")
    log.warning("warning")
    log.error("error")
    log.critical("critical")
    test()
