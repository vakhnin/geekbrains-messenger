# Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt
# и формирующий новый «отчетный» файл в формате CSV.
#
# Для этого:
# * Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
# их открытие и считывание данных. В этой функции из считанных данных необходимо
# с помощью регулярных выражений извлечь значения параметров «Изготовитель системы», «Название ОС»,
# «Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список.
# Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list.
# В этой же функции создать главный список для хранения данных отчета — например, main_data —
# и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС»,
# «Код продукта», «Тип системы». Значения для этих столбцов также оформить в виде списка и
# поместить в файл main_data (также для каждого файла);
# * Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
# В этой функции реализовать получение данных через вызов функции get_data(),
# а также сохранение подготовленных данных в соответствующий CSV-файл;
# * Проверить работу программы через вызов функции write_to_csv().

import csv
import re

from chardet import detect

files_list = ('info_1.txt', 'info_2.txt', 'info_3.txt')


def get_data(files_list_):
    data_keys = [
            'Изготовитель системы',
            'Название ОС',
            'Код продукта',
            'Тип системы',
    ]

    data = {}
    for key in data_keys:
        data[key] = []

    for file_name in files_list_:
        with open(file_name, 'rb') as file:
            content = file.read()
        encoding = detect(content)['encoding']

        for parameter in data.keys():
            data[parameter].append('')

        with open(file_name, encoding=encoding) as f_n:
            for line in f_n:
                for parameter in data.keys():
                    re_pattern = r'\s*{}\s*:(.+)'.format(parameter)
                    match = re.findall(re_pattern, line)
                    if match:
                        idx_data = len(data[parameter])-1
                        data[parameter][idx_data] = match[0].strip()

    main_data = [[]]
    for parameter in data.keys():
        main_data[0].append(parameter)
    for i in range(len(data[data_keys[0]])):
        tmp_arr = []
        for parameter in data.keys():
            tmp_arr.append(data[parameter][i])
        main_data.append(tmp_arr)

    return main_data


def write_to_csv(output_file):
    data = get_data(files_list)
    with open(output_file, 'w', encoding='utf-8', newline='') as f_n:
        f_n_writer = csv.writer(f_n, quoting=csv.QUOTE_NONNUMERIC)
        for row in data:
            f_n_writer.writerow(row)


write_to_csv('csv_output.csv')
