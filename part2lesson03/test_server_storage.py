from storage.server import Storage

from storage.models import engine

storage = Storage(engine)

# Добавляем пользователей
storage.user_add('test1')
storage.user_add('test1')
storage.user_add('test2', 'Инфо')

# Получаем список пользователей
print(storage.user_list())
