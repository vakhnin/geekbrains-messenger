import json
import logging
import logs.server_log_config
from common.utils import parse_received_bytes, choice_jim_action, make_listen_socket
from common.vars import MAX_PACKAGE_LENGTH, ENCODING

log = logging.getLogger('messenger.server')


def main():
    log.debug('Старт сервера')
    sock = make_listen_socket()
    while True:
        conn, addr = sock.accept()
        log.debug(f'Соединение установлено: {addr}')

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
                    log.error(err_msg)
                    conn.close()
                except Exception as e:
                    log.error(f'Unknown error "{e}"')
        except KeyboardInterrupt:
            log.debug('Canceled by keyboard')
            exit(0)
        except Exception as e:
            log.error(f'Unknown error "{e}"')
            exit(1)
        conn.close()


if __name__ == '__main__':
    main()
