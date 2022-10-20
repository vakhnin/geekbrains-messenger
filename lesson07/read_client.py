from socket import AF_INET, SOCK_STREAM, socket

ADDRESS = ('localhost', 7777)


def read_client():
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(ADDRESS)
        while True:
            data = sock.recv(1024).decode('utf-8')
            print(data)


if __name__ == '__main__':
    read_client()
