from sqlalchemy import create_engine, or_
from sqlalchemy.orm import Session

from ..storage.client_models import client_db_dir, Base, Message


class ClientStorage:
    def __init__(self, login):
        super().__init__()
        clear_login = login.replace(' ', '')
        clear_login = clear_login.replace('/', '')
        clear_login = clear_login.replace('\\', '')
        engine = create_engine(f'sqlite:///{client_db_dir}client_db_{clear_login}.sqlite')
        Base.metadata.create_all(engine)
        self._session = Session(engine)

    def add_message(self, user_from, user_to, time, msg):
        msg = Message(user_from, user_to, time, msg)
        self._session.add(msg)
        self._session.commit()

    def get_private_messages_by_contact_name(self, name, limit=30):
        messages = self._session.query(Message). \
            filter(Message.user_to != '#'). \
            filter(or_(Message.user_to == name, Message.user_from == name))\
            .order_by(Message.id.desc()).limit(limit).all()
        return messages
