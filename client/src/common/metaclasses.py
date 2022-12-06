import dis


class ServerVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        attrs = []

        for item in clsdict:
            try:
                ret = dis.get_instructions(clsdict[item])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL' or i.opname == 'LOAD_METHOD':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        if 'connect' in methods:
            raise ValueError('Вызов connect недопустим для серверного сокета')
        if not ('SOCK_STREAM' in methods):
            raise ValueError('Сокет не инициализирован для работы по TCP')

        super().__init__(clsname, bases, clsdict)


class ClientVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        attrs = []

        for item in clsdict:
            try:
                ret = dis.get_instructions(clsdict[item])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL' or i.opname == 'LOAD_METHOD':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
                if 'socket' in methods:
                    raise ValueError('Вызов socket недопустим для клиента')
                if 'accept' in methods:
                    raise ValueError('Вызов accept недопустим для клиента')
                if 'listen' in methods:
                    raise ValueError('Вызов listen недопустим для клиента')

        super().__init__(clsname, bases, clsdict)
