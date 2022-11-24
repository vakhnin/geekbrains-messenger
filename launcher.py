import os
import subprocess
import sys

PROCESSES = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна, '
                   'gs - запустить виджет сервера: ')

    if ACTION == 'q':
        break
    elif ACTION == 'gs':
        PROCESSES.append(
            subprocess.Popen('python start_server_gui.py',
                             env=({**os.environ, 'PYTHONPATH': ';'.join(sys.path)}),
                             creationflags=subprocess.CREATE_NO_WINDOW),
        )
    elif ACTION == 's':
        PROCESSES.append(
            subprocess.Popen('python server.py',
                             env=({**os.environ, 'PYTHONPATH': ';'.join(sys.path)}),
                             creationflags=subprocess.CREATE_NEW_CONSOLE),
        )

        for i in range(1, 3):
            PROCESSES.append(
                subprocess.Popen(f'python client.py -n test{i}',
                                 env=({**os.environ, 'PYTHONPATH': ';'.join(sys.path)}),
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
            )
    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()
