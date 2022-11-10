# Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться
# доступность сетевых узлов.
# Аргументом функции является список, в котором каждый сетевой узел
# должен быть представлен именем хоста или ip-адресом.
# В функции необходимо перебирать ip-адреса и проверять их доступность с выводом с
# оответствующего сообщения («Узел доступен», «Узел недоступен»).
# При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
import platform
from ipaddress import ip_address
from pprint import pprint
from subprocess import Popen, DEVNULL

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


print('==================== Проверка функции host_ping() ======================================================')
list_for_ping = ['google.com', 'a', '8.8.8.8']
result = host_ping(list_for_ping)
pprint(result)
