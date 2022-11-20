import os
import subprocess
import sys

PROCESSES = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESSES.append(
            subprocess.Popen('python server.py',
                             env=({**os.environ, 'PYTHONPATH': ';'.join(sys.path)}),
                             creationflags=subprocess.CREATE_NEW_CONSOLE),
        )

        for i in range(1, 4):
            PROCESSES.append(
                subprocess.Popen(f'python client.py -n test{i}',
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
            )
    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()
