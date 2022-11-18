from common.utils import ServerSocket

# Проверка вызова исключения при неверном номере порта
try:
    server_sock = ServerSocket('', -10)
except ValueError as e:
    print(f'Ошибка: {e}')

# Проверка вызова исключения при типе пераметра порта не int
try:
    server_sock = ServerSocket('', 'abc')
except ValueError as e:
    print(f'Ошибка: {e}')
