from storage.server import Storage

from storage.models import engine

storage = Storage(engine)
storage.add_user('test1')
