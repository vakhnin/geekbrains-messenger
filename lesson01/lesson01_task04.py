# Преобразовать слова «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое и выполнить обратное преобразование
# (используя методы encode и decode).

words = ['разработка', 'администрирование', 'protocol', 'standard']

for word in words:
    enc_word_bytes = word.encode('utf-8')
    print(f'Тип: {type(enc_word_bytes)} Содержимое: |{enc_word_bytes}|')
    dec_str = enc_word_bytes.decode('utf-8')
    print(f'Тип: {type(dec_str)} Содержимое: |{dec_str}|')

# Output
# Тип: <class 'bytes'> Содержимое:
# |b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'|
# Тип: <class 'str'> Содержимое: |разработка|
# Тип: <class 'bytes'> Содержимое:
# |b'\xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5'|
# Тип: <class 'str'> Содержимое: |администрирование|
# Тип: <class 'bytes'> Содержимое: |b'protocol'|
# Тип: <class 'str'> Содержимое: |protocol|
# Тип: <class 'bytes'> Содержимое: |b'standard'|
# Тип: <class 'str'> Содержимое: |standard|