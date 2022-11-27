import json
import logging
import sys
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication

from client_gui.client_gui_utils import start_client_window, ClientGUIWindow
from common.client_utils import make_presence_message, \
    send_message_take_answer, parse_args, Client, Receiver, Sender
import logs.client_log_config
from common.vars import ENCODING

log = logging.getLogger('messenger.client')


class MainApp(QtWidgets.QWidget):
    def __init__(self, address, port, client_name):
        super(MainApp, self).__init__()
        self.client_name = client_name
        self.sock = self.make_socket_send_presens_message(address, port, client_name)

        self.sender_thread = Sender(self.sock, client_name)
        self.sender_thread.start()
        self.receiver_thread = Receiver(self.sock, client_name)
        self.receiver_thread.start()
        self.receiver_thread.new_message_signal.connect(self.new_messages_received)

        self.main_window = ClientGUIWindow(client_name)
        self.main_window.show()

    def new_messages_received(self, s):
        self.main_window.new_message_signal.emit(s)
        print(f'main {s}')

    def make_socket_send_presens_message(self, address, port, client_name):
        try:
            print('Консольный месседжер. Клиентский модуль.')
            sock = socket(AF_INET, SOCK_STREAM)
            client = Client(sock)
            client.connect((address, port))
            message = make_presence_message(client_name, 'I am here!')
            answer = send_message_take_answer(client.sock, message)
            message = json.dumps(message, separators=(',', ':'))
            client.sock.send(message.encode(ENCODING))
            print('Установлено соединение с сервером.')
            print(f'\nПривет {client_name}!\n')
            return sock
        except Exception as e:
            print('Соединение с сервером не установлено.')
            log.error(f'Соединение с сервером не установлено. Ошибка {e}')
            sys.exit(-1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    address, port, client_name = parse_args()
    main_app = MainApp(address, port, client_name)
    sys.exit(app.exec_())
