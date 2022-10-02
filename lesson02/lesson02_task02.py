# Есть файл orders в формате JSON с информацией о заказах. Написать скрипт,
# автоматизирующий его заполнение данными.
#
# Для этого:
# * Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item),
# количество (quantity), цена (price), покупатель (buyer), дата (date).
# Функция должна предусматривать запись данных в виде словаря в файл orders.json.
# При записи данных указать величину отступа в 4 пробельных символа;
# * Проверить работу программы через вызов функции write_order_to_json()
import json

OUTPUT_FILE = 'orders.json'


def write_order_to_json(item, quantity, price, buyer, date):
    f_n = open(OUTPUT_FILE, 'a+', encoding='utf-8')  # создаем файл, если его нет
    f_n.close()

    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f_n:
            file_content = f_n.read().strip()
            if file_content:
                obj = json.loads(file_content)
            else:
                obj = {'orders': []}
    except json.JSONDecodeError:
        print('Не корректный json')
        return

    obj['orders'].append({
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date,
    })

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_n:
        json.dump(obj, f_n, sort_keys=True, indent=4)


# В условии задачи сказано что используется файл orders с информацией о заказах (не заказе)
# Сделал вывод что функция должна дописывать еще один заказ в файл с заказами
# Каждый вызов функции добавляет (не заменяет) данные в файл
write_order_to_json('Processor', 3, '50.30', 'TRY company', '07/19/2020')
