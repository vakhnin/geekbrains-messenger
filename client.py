import json
import logging
import sys
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from client_gui.client_gui_utils import start_client_window
from common.client_utils import make_presence_message, \
    send_message_take_answer, parse_args, user_input, Client, Receiver
import logs.client_log_config
from common.vars import ENCODING

log = logging.getLogger('messenger.client')


class MainApp(QApplication):
    def main_loop(self):
        address, port, client_name = parse_args()

        # client_window = threading.Thread(
        #     target=start_client_window, args=(client_name,))
        # client_window.daemon = True
        # client_window.start()

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
            log.info(
                f'Запущен клиент с парамертами: адрес сервера: {address}, '
                f'порт: {port}, имя пользователя: {client_name}')
            log.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
            print(f'\nПривет {client_name}!\n')
        except Exception as e:
            print('Соединение с сервером не установлено.')
            log.error(f'Соединение с сервером не установлено. Ошибка {e}')
        else:
            sender = threading.Thread(
                target=user_input, args=(client.sock, client_name))
            sender.daemon = True
            sender.start()

            self.thread = QtCore.QThread()
            self.browserHandler = Receiver(client.sock, client_name)
            self.browserHandler.moveToThread(self.thread)
            self.thread.started.connect(self.browserHandler.run)
            self.thread.start()

            log.debug('Запущены процессы')

            while True:
                time.sleep(4)
                if sender.is_alive() and self.thread.isRunning():
                    continue
                break


if __name__ == '__main__':
    main_app = MainApp([])
    main_app.main_loop()
