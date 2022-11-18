import dis
from pprint import pprint


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
