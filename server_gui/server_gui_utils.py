import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from storage.models import engine
from storage.server import Storage

cur_path = os.path.abspath(__file__)
cur_dir, _ = os.path.split(cur_path)
cur_dir += os.sep


class ServerGUIWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi(cur_dir + 'serverUI.ui', self)
        self.storage = Storage(engine)

    def show_users_list(self):
        users_table = self.usersTableWidget
        users_list = self.storage.user_list()

        users_table.setRowCount(len(users_list))
        for row, user in enumerate(users_list):
            users_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            users_table.setItem(row, 1, QTableWidgetItem(str(user.login)))
            users_table.setItem(row, 2, QTableWidgetItem(str(user.info)))
