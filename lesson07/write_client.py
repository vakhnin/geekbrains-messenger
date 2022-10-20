from socket import AF_INET, SOCK_STREAM, socket

ADDRESS = ('localhost', 7777)


def echo_client():
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(ADDRESS)
        while True:
            msg = input('Ваше сообщение: ')
            if msg == 'exit':
                break
            sock.send(msg.encode('utf-8'))


if __name__ == '__main__':
    echo_client()
