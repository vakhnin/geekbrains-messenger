import datetime

from sqlalchemy.orm import Session

from storage.models import User, History


class Storage:
    def __init__(self, engine):
        self._session = Session(engine)

    def user_add(self, login, info=''):
        if self._session.query(User).filter_by(login=login).first():
            return None
        user = User(login, info)
        self._session.add(user)
        self._session.commit()

    def user_list(self):
        return self._session.query(User).all()

    def user_by_login(self, login):
        return self._session.query(User).filter_by(login=login).first()

    def history_time_add(self, user_login, ip, login_time=datetime.datetime.now()):
        user = self.user_by_login(user_login)
        if not user:
            print(f'Ошибка: пользователя с логином {user_login} не существует')
            return
        history = History(user.id, ip, login_time)
        self._session.add(history)
        self._session.commit()

    def history_all_users(self):
        return self._session.query(History).all()
