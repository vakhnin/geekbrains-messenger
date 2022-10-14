import logging

from common.utils import parse_answer, make_presence_message, \
    send_message_take_answer, make_sent_socket
import logs.client_log_config

log = logging.getLogger('messenger.client')


def main():
    try:
        log.debug('Старт клиента')
        sock = make_sent_socket()

        message = make_presence_message('C0deMaver1ck', 'Yep, I am here!')
        answer = send_message_take_answer(sock, message)
        parse_answer(answer)

        sock.close()
    except KeyboardInterrupt:
        log.debug('Canceled by keyboard')
        exit(1)
    except ConnectionRefusedError:
        err_msg = 'Подключение не установлено, т.к. конечный компьютер ' + \
                  'отверг запрос на подключение'
        log.error(err_msg)
        exit(1)
    except ConnectionResetError:
        err_msg = 'Удаленный хост принудительно разорвал ' + \
                  'существующее подключение'
        log.error(err_msg)
        sock.close()
        exit(1)
    except Exception as e:
        log.error(f'Unknown error "{e}"')


if __name__ == '__main__':
    main()
