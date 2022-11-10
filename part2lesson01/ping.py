import platform
from ipaddress import ip_address, ip_network
from pprint import pprint
from subprocess import Popen, DEVNULL

# Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться
# доступность сетевых узлов.
# Аргументом функции является список, в котором каждый сетевой узел
# должен быть представлен именем хоста или ip-адресом.
# В функции необходимо перебирать ip-адреса и проверять их доступность с выводом с
# оответствующего сообщения («Узел доступен», «Узел недоступен»).
# При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
REACHABLEMESSAGE = 'Узел доступен'
UNREACHABLEMESSAGE = 'Узел не доступен'


def host_ping(ip_list):
    ping_processes_list = []
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    for ip in ip_list:
        try:
            ip = ip_address(ip)
        except ValueError:
            pass
        command = ["ping", param, "2", str(ip)]
        process = Popen(command, stdout=DEVNULL, stderr=DEVNULL)
        ping_processes_list.append({'ip': ip,
                                    'reachable': process})

    ping_list = []
    for i in range(len(ping_processes_list)):
        ping_result = ping_processes_list[i]['reachable'].wait()
        ping_list.append({'ip': ping_processes_list[i]['ip'],
                          'reachable': UNREACHABLEMESSAGE if ping_result else REACHABLEMESSAGE})

    return ping_list

# Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
# Меняться должен только последний октет каждого адреса.
# По результатам проверки должно выводиться соответствующее сообщение.
def host_range_ping(start_ip, count_ip):
    if count_ip < 1 or not type(count_ip) == int:
        print(f'Количество адресов должно быть целым числом 1 или больше')
        return False

    try:
        ip = ip_address(start_ip)
    except ValueError:
        print(f'{start_ip} не является валидным ip')
        return False

    last_octet = int(ip) % 256
    if last_octet + count_ip > 255:
        print(f'От ip адреса {start_ip} в последний октет не помещается'
              f' {count_ip} адреса, только {255 - last_octet}')
        return False

    ip_list = []
    for i in range(count_ip):
        ip_list.append(ip + i)
    return host_ping(ip_list)


print('==================== Проверка функции host_ping() ======================================================')
# list_for_ping = ['google.com', 'a', '8.8.8.8']
# result = host_ping(list_for_ping)
# pprint(result)

print('==================== Проверка функции host_range_ping() ================================================')
while True:
    ip = input('Введите начальный IP или q для выхода: ')
    if ip == 'q':
        break
    count = input('Введите количестов IP для тестирования или q для выхода: ')
    if count == 'q':
        break
    count = int(count)
    result = host_range_ping(ip, count)
    if result:
        pprint(result)
        break