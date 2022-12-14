import datetime
import hashlib
import sys

from sqlalchemy.orm import Session

sys.path.append('..')
from storage.server_models import User, History, Contact


def password_to_md5(password):
    salt = '%@V7@A9Cpg'
    return hashlib.md5((password + salt).encode('utf-8')).hexdigest()


class Storage:
    def __init__(self, engine):
        self._session = Session(engine)

    def user_add(self, login, password, info=''):
        if self._session.query(User).filter_by(login=login).first():
            return None
        user = User(login, password, info)
        self._session.add(user)
        self._session.commit()

    def user_list(self):
        return self._session.query(User).all()

    def user_by_login(self, login):
        return self._session.query(User).filter_by(login=login).first()

    def user_by_id(self, id):
        return self._session.query(User).filter_by(id=id).first()

    def history_time_add(self, user_login, ip, login_time=datetime.datetime.now()):
        user = self.user_by_login(user_login)
        if not user:
            print(f'Ошибка history_time_add: пользователя с логином {user_login} не существует')
            return
        history = History(user.id, ip, login_time)
        self._session.add(history)
        self._session.commit()

    def history_all_users(self):
        return self._session.query(History).all()

    def contact_add(self, user_login, contact_user_login):
        user = self.user_by_login(user_login)
        if not user:
            print(f'Ошибка contact_add: пользователя с логином {user_login} не существует')
            return False

        contact_user = self.user_by_login(contact_user_login)
        if not contact_user:
            print(f'Ошибка contact_add: пользователя с логином {contact_user} не существует')
            return False

        contact = self._session.query(Contact). \
            filter_by(user_id=user.id). \
            filter_by(contact_user_id=contact_user.id).all()
        if contact:
            return False

        contact = Contact(user.id, contact_user.id)
        self._session.add(contact)
        self._session.commit()
        return True

    def contact_del(self, user_login, contact_user_login):
        user = self.user_by_login(user_login)
        if not user:
            print(f'Ошибка contact_add: пользователя с логином {user_login} не существует')
            return False

        contact_user = self.user_by_login(contact_user_login)
        if not contact_user:
            print(f'Ошибка contact_add: пользователя с логином {contact_user} не существует')
            return False

        contact = self._session.query(Contact). \
            filter_by(user_id=user.id). \
            filter_by(contact_user_id=contact_user.id).first()
        if not contact:
            return False
        self._session.delete(contact)
        self._session.commit()
        return True

    def contact_list_by_login(self, login):
        user = self.user_by_login(login)
        if not user:
            print(f'Ошибка contact_add: пользователя с логином {login} не существует')
            return []
        contacts_list = self._session.query(Contact) \
            .filter_by(user_id=self.user_by_login(login).id).all()
        return [self.user_by_id(user.contact_user_id).login for user in contacts_list]
