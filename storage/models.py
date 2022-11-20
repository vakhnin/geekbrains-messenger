import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    info = Column(String)

    def __init__(self, login, info=''):
        super().__init__()
        self.login = login
        self.info = info

    def __repr__(self):
        return f'<User({self.id}, {self.login}, {self.info})>'


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    login_time = Column(DateTime)
    ip = Column(String)

    def __init__(self, user_id, ip, login_time):
        super().__init__()
        self.user_id = user_id
        self.login_time = login_time
        self.ip = ip

    def __repr__(self):
        return f'<User({self.id}, {self.user_id}, {self.ip}, {self.login_time})>'


cur_path = os.path.abspath(__file__)
cur_dir, _ = os.path.split(cur_path)
cur_dir += os.sep
engine = create_engine(f'sqlite:///{cur_dir}server_db.sqlite', pool_recycle=7200)
Base.metadata.create_all(engine)
