import os
import sys

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow

cur_path = os.path.abspath(__file__)
cur_dir, _ = os.path.split(cur_path)
cur_dir += os.sep


class ClientGUIWindow(QMainWindow):
    new_message_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi(cur_dir + 'clientUI.ui', self)
        self.new_message_signal.connect(self.new_messages_received)

    def new_messages_received(self, s):
        print(f'window {s}')


def start_client_window(login):
    app = QtWidgets.QApplication(sys.argv)
    window = ClientGUIWindow()
    window.show()
    app.exec_()
    return
