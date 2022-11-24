import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_from = Column(String)
    user_to = Column(String)
    time = Column(String)
    msg = Column(String)

    def __init__(self, user_from, user_to, time, msg):
        super().__init__()
        self.user_from = user_from
        self.user_to = user_to
        self.time = time
        self.msg = msg

    def __repr__(self):
        return f'<Message({self.id}, {self.user_from}, {self.user_to}, {self.time}, {self.msg})>'


cur_path = os.path.abspath(__file__)
cur_dir, _ = os.path.split(cur_path)
client_db_dir = cur_dir + os.sep
engine = create_engine(f'sqlite:///{cur_dir}server_db.sqlite')
Base.metadata.create_all(engine)
