from common.utils import parse_answer, make_presence_message, \
    send_message_take_answer, make_sent_socket


def main():
    try:
        sock = make_sent_socket()

        message = make_presence_message('C0deMaver1ck', 'Yep, I am here!')
        answer = send_message_take_answer(sock, message)
        parse_answer(answer)

        sock.close()
    except ConnectionRefusedError:
        err_msg = 'Подключение не установлено, т.к. конечный компьютер ' + \
                  'отверг запрос на подключение'
        print(err_msg)


if __name__ == '__main__':
    main()
