import select
from socket import AF_INET, SOCK_STREAM, socket


def read_requests(r_clients, all_clients):
    responses = {}

    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except:
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            all_clients.remove(sock)

    return responses


def write_responses(responses, w_clients, all_clients):
    for _, resp in responses.items():
        for sock in w_clients:
            try:
                sock.send(resp.encode('utf-8'))
            except:
                print(
                    f'Клиент {sock.fileno()} {sock.getpeername()} отключился'
                )
                sock.close()
                all_clients.remove(sock)


def mainloop():
    address = ('', 7777)
    clients = []

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.settimeout(0.2)
    while True:
        try:
            conn, addr = s.accept()
        except OSError:
            pass
        else:
            print('Получен запрос на соединение от %s' % str(addr))
            clients.append(conn)
        finally:
            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass

            responses = read_requests(r, clients)
            if responses != {}:
                print(responses)
            write_responses(responses, w, clients)


print('Эхо-сервер запущен!')
mainloop()
