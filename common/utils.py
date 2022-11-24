import functools
import logging
import sys
import traceback

import logs.client_log_config
import logs.server_log_config

client_log = logging.getLogger('messenger.client')
server_log = logging.getLogger('messenger.server')


class Log:
    """Класс-декоратор"""

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        if sys.argv[0].endswith('server.py'):
            logger = server_log
        else:
            logger = client_log
        res = self.func(*args, **kwargs)
        logger.debug((f'Функция {self.func.__name__}() '
                      f'вызвана из функции {traceback.extract_stack()[-2].name}()'))
        logger.debug(f'Функция: {self.func.__name__}({args}, {kwargs}) = {res}')
        return res
