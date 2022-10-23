from subprocess import CREATE_NEW_CONSOLE, Popen

p_list = []
while True:
    users = input(
        'Запустить n клиентов (int) / Закрыть клиентов (x) / Выйти (q) '
    )
    if users == 'q':
        break
    elif users == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
    else:
        try:
            if not int(users):
                continue
            for _ in range((int(users)) // 2):
                p_list.append(Popen('python write_client.py',
                                    creationflags=CREATE_NEW_CONSOLE))
                p_list.append(Popen('python read_client.py',
                                    creationflags=CREATE_NEW_CONSOLE))
            if int(users) % 2:
                p_list.append(Popen('python write_client.py',
                                    creationflags=CREATE_NEW_CONSOLE))
            print(f' Запущено {int(users)} клиентов')
        except ValueError:
            continue
