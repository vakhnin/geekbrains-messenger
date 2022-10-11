import json

from common.utils import parse_received_bytes, choice_jim_action, make_listen_socket
from common.vars import MAX_PACKAGE_LENGTH, ENCODING


def main():
    sock = make_listen_socket()
    while True:
        conn, addr = sock.accept()
        print(f'Соединение установлено: {addr}')

        try:
            while True:
                try:
                    data = conn.recv(MAX_PACKAGE_LENGTH)
                    if not data:
                        break
                    jim_obj = parse_received_bytes(data)
                    answer = choice_jim_action(jim_obj)
                    answer = json.dumps(answer, separators=(',', ':'))
                    conn.send(answer.encode(ENCODING))
                except ConnectionResetError:
                    err_msg = 'Удаленный хост принудительно разорвал ' + \
                              'существующее подключение'
                    print(err_msg)
                    conn.close()
        finally:
            conn.close()


if __name__ == '__main__':
    main()
