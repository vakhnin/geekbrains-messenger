import logging
from collections import deque

import select

import logs.server_log_config
from common.utils import read_requests, write_responses, get_server_param, ServerSocket

log = logging.getLogger('messenger.server')


def main():
    log.debug('Старт сервера')
    print('Старт сервера')

    clients_data = {}
    server_param = get_server_param()
    server_sock = ServerSocket(addr=server_param['addr'], port=server_param['port'])
    server_sock.start_socket()
    while True:
        try:
            conn, addr = server_sock.accept()
            print(f'Соединение установлено: {addr}')
        except OSError:
            pass
        else:
            print(f'Получен запрос на соединение от {addr}')
            clients_data[conn] = \
                {
                    'client_name': '',
                    'msg_for_send': deque(maxlen=100),
                    'answ_for_send': deque(maxlen=100),
                }
        finally:
            wait = 0
            r = []
            w = []
            try:
                r, w, e = \
                    select.select(
                        clients_data.keys(), clients_data.keys(), [], wait)
                log.debug(f'Ошибки сокетов {e}')
            except Exception:
                pass

            read_requests(r, clients_data)
            write_responses(w, clients_data)


if __name__ == '__main__':
    main()