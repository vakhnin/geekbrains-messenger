import json
import logging
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM

from common.utils import make_presence_message, \
    send_message_take_answer, parse_args, user_input, user_output, Client
import logs.client_log_config
from common.vars import ENCODING

log = logging.getLogger('messenger.client')


def main():
    address, port, client_name = parse_args()

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

        receiver = threading.Thread(
            target=user_output, args=(client.sock, client_name))
        receiver.daemon = True
        receiver.start()
        log.debug('Запущены процессы')

        while True:
            time.sleep(10)
            if sender.is_alive() and receiver.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
