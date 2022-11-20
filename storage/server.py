from sqlalchemy.orm import Session

from storage.models import User


class Storage:
    def __init__(self, engine):
        self._session = Session(engine)

    def add_user(self, login, info=''):
        if self._session.query(User).filter_by(login=login).first():
            return
        user = User(login, info)
        self._session.add(user)
        self._session.commit()
