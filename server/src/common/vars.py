# Порт поумолчанию для сетевого ваимодействия
DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'

# Ошибки разбора
NOT_BYTES = 'Arg is not bytes'
NOT_DICT = 'Data is not dict'
NO_ACTION = 'Request has no "action"'
NO_TIME = 'Request has no "time""'
BROKEN_JIM = 'JSON broken'
UNKNOWN_ACTION = 'Unknown action'
LOGIN_ERROR = 405
LOGIN_OK = 205
