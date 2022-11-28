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
    send_message_take_answer, parse_args, Client, Receiver, Sender, make_msg_message, make_get_contacts_message, \
    make_add_contact_message, make_del_contact_message
import logs.client_log_config
from common.vars import ENCODING
from storage.client_storage import ClientStorage

log = logging.getLogger('messenger.client')


class MainApp(QtWidgets.QWidget):
    def __init__(self, address, port, client_name):
        super(MainApp, self).__init__()
        self.client_name = client_name
        self.sock = self.make_socket_send_presens_message(address, port, client_name)
        self.storage = ClientStorage(self.client_name)

        self.sender_thread = Sender(self.sock, client_name)
        self.sender_thread.start()
        self.receiver_thread = Receiver(self.sock, self.storage, client_name)
        self.receiver_thread.start()
        self.receiver_thread.new_message_signal.connect(self.new_messages_received)
        self.receiver_thread.new_contact_list_signal.connect(self.new_contact_list_received)

        self.main_window = ClientGUIWindow(client_name, self.storage)
        self.main_window.show()
        self.main_window.send_message_signal.connect(self.send_message)
        self.main_window.contact_list_signal.connect(self.contact_list_command)

    def new_contact_list_received(self, contact_list):
        self.main_window.new_contact_list_signal.emit(contact_list)

    def contact_list_command(self, obj):
        msg = {}
        if obj['command'] == 'c':
            msg = make_get_contacts_message(self.client_name)
        elif obj['command'] == 'a':
            msg = make_add_contact_message(self.client_name, obj['contact_name'])
        elif obj['command'] == 'd':
            msg = make_del_contact_message(self.client_name, obj['contact_name'])
        msg = json.dumps(msg, separators=(',', ':'))
        self.sock.send(msg.encode(ENCODING))

    def send_message(self, obj):
        msg = make_msg_message(self.client_name, obj['msg'], obj['to'])
        msg = json.dumps(msg, separators=(',', ':'))
        self.sock.send(msg.encode(ENCODING))

    def new_messages_received(self, jim_obj):
        self.main_window.new_message_signal.emit(jim_obj)

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
