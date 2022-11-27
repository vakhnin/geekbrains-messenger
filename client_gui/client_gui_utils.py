import os
import sys

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow

from common.client_utils import message_to_str

cur_path = os.path.abspath(__file__)
cur_dir, _ = os.path.split(cur_path)
cur_dir += os.sep


class ClientGUIWindow(QMainWindow):
    new_message_signal = QtCore.pyqtSignal(object)
    send_message_signal = QtCore.pyqtSignal(object)

    def __init__(self, client_name, parent=None):
        QMainWindow.__init__(self, parent)
        self.client_name = client_name
        uic.loadUi(cur_dir + 'clientUI.ui', self)

        label_text = f'Привет {client_name}!'
        self.clientNameLabel.setText(label_text)

        self.new_message_signal.connect(self.new_messages_received)

        self.commonMessageSendButton.clicked.connect(self.send_message)

    def new_messages_received(self, jim_obj):
        self.commonChatListWidget.addItem(message_to_str(jim_obj, self.client_name))

    def send_message(self, checked, to='#'):
        self.send_message_signal.emit(
            {'to': to, 'msg': self.commonMessageLineEdit.text()})
        self.commonMessageLineEdit.setText('')


def start_client_window(login):
    app = QtWidgets.QApplication(sys.argv)
    window = ClientGUIWindow()
    window.show()
    app.exec_()
    return
