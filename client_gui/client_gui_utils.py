import os
import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow

cur_path = os.path.abspath(__file__)
cur_dir, _ = os.path.split(cur_path)
cur_dir += os.sep


class ClientGUIWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi(cur_dir + 'clientUI.ui', self)


def start_client_window(login):
    app = QtWidgets.QApplication(sys.argv)
    window = ClientGUIWindow()
    window.show()
    sys.exit(app.exec_())
