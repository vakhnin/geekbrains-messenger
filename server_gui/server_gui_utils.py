import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from storage.models import engine
from storage.server_storage import Storage

cur_path = os.path.abspath(__file__)
cur_dir, _ = os.path.split(cur_path)
cur_dir += os.sep


class ServerGUIWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi(cur_dir + 'serverUI.ui', self)

        self.storage = Storage(engine)

        self.refreshUsersListButton.clicked.connect(self.show_users_list)
        self.refreshHystoryLoginsListButton.clicked.connect(self.show_hystory_logins_list)

    def show_users_list(self):
        users_table = self.usersTableWidget

        users_table.clearContents()
        users_table.setRowCount(0)

        users_list = self.storage.user_list()

        users_table.setRowCount(len(users_list))
        for row, user in enumerate(users_list):
            users_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            users_table.setItem(row, 1, QTableWidgetItem(str(user.login)))
            users_table.setItem(row, 2, QTableWidgetItem(str(user.info)))

    def show_hystory_logins_list(self):
        hystory_logins_table = self.hystoryLoginsTableWidget

        hystory_logins_table.clearContents()
        hystory_logins_table.setRowCount(0)

        hystory_logins_list = self.storage.history_all_users()

        hystory_logins_table.setRowCount(len(hystory_logins_list))
        for row, item in enumerate(hystory_logins_list):
            user = self.storage.user_by_id(item.user_id)
            if user:
                user = user.login
            else:
                user = item.user_id
            hystory_logins_table.setItem(row, 0, QTableWidgetItem(str(user)))
            hystory_logins_table.setItem(row, 1, QTableWidgetItem(str(item.login_time)))
            hystory_logins_table.setItem(row, 2, QTableWidgetItem(str(item.ip)))
