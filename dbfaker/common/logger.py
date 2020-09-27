# -*- encoding: utf-8 -*-
import datetime
import logging
import os
from logging import handlers

from dbfaker.common.tools import check_path

__all__ = ['Logger', 'log']


class Logger:
    LOG_FORMAT = '%(asctime)s [%(levelname)s]   [%(filename_ca)s] [line:%(lineno_ca)d]: %(message)s'
    DATE_FORMAT = '%Y/%m/%d %H:%M:%S %p'

    def __init__(self, name, path=None):
        self._logger = logging.Logger(name)
        self._logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(Logger.LOG_FORMAT)
        if path:
            path = check_path(path)
            if not os.path.exists(os.path.dirname(path)):
                os.mkdir(os.path.dirname(path))
            # print('log into file [%s].' % os.path.abspath(path))
            file_handler = handlers.TimedRotatingFileHandler(path, when='midnight', interval=1, backupCount=10,
                                                             encoding='utf-8', atTime=datetime.time(0, 0, 0, 0))
            file_handler.setFormatter(fmt)
            file_handler.setLevel(logging.DEBUG)
            self._logger.addHandler(file_handler)
        # stream_handler = logging.StreamHandler()
        # stream_handler.setLevel(logging.DEBUG)
        # stream_handler.setFormatter(fmt)
        # self._logger.addHandler(stream_handler)

    def i(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **self.wrap_stack(**kwargs))

    def d(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **self.wrap_stack(**kwargs))

    def w(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **self.wrap_stack(**kwargs))

    def e(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **self.wrap_stack(**kwargs))

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self._logger.exception(msg, *args, exc_info=exc_info, **self.wrap_stack(**kwargs))

    def c(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, **self.wrap_stack(**kwargs))

    def wrap_stack(self, **kwargs):
        extra = kwargs['extra'] if 'extra' in kwargs else {}
        caller = self._logger.findCaller(stack_info=False)
        cwd = os.getcwd().replace('\\', '/')
        caller_file = caller[0].replace(os.getcwd(), '')
        caller_file = caller_file.replace(cwd, '')
        if caller_file.startswith('/') or caller_file.startswith('\\'):
            caller_file = caller_file[1:]
        extra['filename_ca'] = caller_file
        extra['lineno_ca'] = caller[1]
        kwargs['extra'] = extra
        return kwargs


log = Logger('dbfaker', path=r'log/dbfaker.log')
