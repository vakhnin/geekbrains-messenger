# Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.

from chardet import detect

file_name = 'test_file.txt'

with open(file_name, 'rb') as f:
    content = f.read()
encoding = detect(content)['encoding']
print(f'Кодировка файла {file_name}: {encoding}')

print()
print(f'Содержимое файла {file_name}, открытого принудительно с кодировкой UTF-8:')
with open(file_name, encoding='utf-8') as f:
    for line in f:
        print(line, end='')

# Кодировка файла test_file.txt: utf-8
#
# Содержимое файла test_file.txt, открытого принудительно с кодировкой UTF-8:
# сетевое программирование
# сокет
# декоратор
