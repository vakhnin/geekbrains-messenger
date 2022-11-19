from common.utils import Server

# Проверка вызова исключения при неверном номере порта
try:
    server_sock = Server('', -10)
except ValueError as e:
    print(f'Ошибка: {e}')

# Проверка вызова исключения при типе пераметра порта не int
try:
    server_sock = Server('', 'abc')
except ValueError as e:
    print(f'Ошибка: {e}')
