import os
import sys

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow

from common.client_utils import message_to_str

cur_path = os.path.abspath(__file__)
cur_dir, _ = os.path.split(cur_path)
cur_dir += os.sep


class ClientGUIWindow(QMainWindow):
    new_message_signal = QtCore.pyqtSignal(object)
    send_message_signal = QtCore.pyqtSignal(object)
    contact_list_signal = QtCore.pyqtSignal(object)
    new_contact_list_signal = QtCore.pyqtSignal(object)

    timer = QTimer()
    timer_count = 10
    contact_list = None

    def __init__(self, client_name, parent=None):
        QMainWindow.__init__(self, parent)
        self.client_name = client_name
        self.current_private_contact = None
        uic.loadUi(cur_dir + 'clientUI.ui', self)

        label_text = f'Привет {client_name}!'
        self.clientNameLabel.setText(label_text)

        self.new_message_signal.connect(self.new_messages_received)
        self.new_contact_list_signal.connect(self.new_contact_list)

        self.commonMessageSendButton.clicked.connect(self.send_message)
        self.privateMessageSendButton.clicked \
            .connect(lambda: self.send_message(to=self.current_private_contact))
        self.addContactButton.clicked \
            .connect(lambda: self.send_contact_list_command(command='a'))
        self.delContactButton.clicked \
            .connect(lambda: self.send_contact_list_command(command='d'))

        self.contactListWidget.addItem('Старт загрузки списка контактов')
        self.timer.timeout.connect(self.try_receive_contact_list)
        self.timer.start(1000)
        self.contactListWidget.itemDoubleClicked.connect(self.set_current_private_contact)

    def set_current_private_contact(self, item):
        self.current_private_contact = item.text()
        self.headerPrivateChatLabel.setText(f'Приватный чат c '
                                            f'{self.current_private_contact}')
        self.privateChatListWidget.clear()

    def new_contact_list(self, contact_list):
        self.contact_list = contact_list
        self.contactListWidget.clear()
        if len(contact_list):
            for contact in contact_list:
                self.contactListWidget.addItem(contact)
        else:
            self.contactListWidget.addItem('Список контактов пуст')

    def try_receive_contact_list(self):
        if self.contact_list is not None:
            self.timer.stop()
        elif self.timer_count <= 0:
            self.timer.stop()
            self.contactListWidget \
                .item(0).setText('Не удалось получить список контактов')
        else:
            self.contactListWidget \
                .item(0).setText(f'Пытаемся загрузить спиок контактов ({self.timer_count}) ...')
            self.timer_count -= 1
            self.send_contact_list_command()

    def send_contact_list_command(self, checked=True, command='c'):
        self.contact_list_signal.emit(
            {'command': command, 'contact_name': self.contactLineEdit.text()})

    def new_messages_received(self, jim_obj):
        self.commonChatListWidget.addItem(message_to_str(jim_obj, self.client_name))

    def send_message(self, checked=True, to='#'):
        if to == '#':
            self.send_message_signal.emit(
                {'to': to, 'msg': self.commonMessageLineEdit.text()})
            self.commonMessageLineEdit.setText('')
            return
        if self.current_private_contact is None:
            self.privateChatListWidget \
                .addItem('Для открытия приватного чата сделайте двойной клик '
                         'по имени контакта в списке контактов слева')
            return
        self.send_message_signal.emit(
            {'to': to, 'msg': self.privateMessageLineEdit.text()})
        self.privateMessageLineEdit.setText('')

def start_client_window(login):
    app = QtWidgets.QApplication(sys.argv)
    window = ClientGUIWindow()
    window.show()
    app.exec_()
    return
