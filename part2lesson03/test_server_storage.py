from storage.server import Storage

from storage.models import engine

storage = Storage(engine)

# Добавляем пользователей
storage.user_add('Вася')
storage.user_add('Вася')
storage.user_add('Петя', 'Инфо')

# Получаем список пользователей
print(storage.user_list())

# Получаем пользователя по логину
print(storage.user_by_login('Вася'))
print(storage.user_by_login('Вася1111'))

# Добавляем время логина
storage.history_time_add(storage.user_by_login('Вася').id, '127.0.0.1')
storage.history_time_add(storage.user_by_login('Вася').id, '127.0.0.2')
