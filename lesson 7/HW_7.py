# Ilya Chaplenko

# Задание №1
#  Есть список list1 = [i for i in range(100)], создайте новый
# список с пробросом каждого пятого элемента (используйте continue)

'''
list1 = [i for i in range(100)]
list2 = []

for num1 in range(0, len(list1), 5):
    for num2 in list1:
        if num2 == num1:
            list2.append(num2)
            continue
print('Список: ', list2)
'''


# Задание №2
# Напишите скрипт который будет работать циклично в интерактивном режиме,
# скрипт должен запрашивать имя пользователя, если пользователь не вводя 
# имя нажмет на Enter то скрипт должен завершиться (используйте break)
'''
while True:
    name = input('Введите свое имя: ')
    if not name: break
    print('Приветствую вас сударь!', name)
'''


# Задание №4
# Напишите программу, которая запрашивает ввод двух значений. Если хотя бы одно
# из них не является числом, то должна выполняться конкатенация,
# то есть соединение, строк. В остальных случаях введенные числа суммируются.

'''
while True:
    num1 = input('Первое значение: ')
    num2 = input('Второе значение: ')
    try:
        print('Результат: ', float(num1) + float(num2))
    except ValueError:
        print('Результат: ', num1 + num2)
'''
<<<<<<< HEAD


# Задание №5
#  Есть список: list1 = [1, ‘a’, 3, ‘b’, 5, ‘6’, 7, ‘8’, 9, ‘c’], необходимо 
# разделить на два списка, в первом только цифровые значения, а во втором только строки

'''
list1 = [1, 'a', 3, 'b', 5, '6', 7, '8', 9, 'c']
string = []
integer = []
for num in list1:
    num1 = type(num)
    if num1 == str:
        string.append(num)
    else: 
        integer.append(num)
print('Список строк: ', string)
print('Список цифр: ', integer)
'''


# Задание №6
# Тот же самый пример, с сообщением после каждой итерации о том что элемент N добавлен

'''
list1 = [1, 'a', 3, 'b', 5, '6', 7, '8', 9, 'c']
string = []
integer = []
for num in list1:
    num1 = type(num)
    if num1 == str:
        string.append(num)
    else: 
        integer.append(num)
for i in string:
    print(i, 'Добавлен в список строк')
for y in integer:
    print(y, 'Добавлен в список цифр')
'''  


# Задание №7
#  Приведенный ниже код назначает 5-ю букву каждого слова в food новый список fifth. 
#  Однако код в настоящее время выдает ошибки. Вставьте предложение try/except,
#  которое позволит запустить код и создать список 5-й буквы в каждом слове. 
# Если слово недостаточно длинное, оно не должно ничего выводить.
'''
food = ["chocolate", "chicken", "corn", "sandwich", "soup", "potatoes", "beef", "lox", "lemonade"]
fifth = []
for x in food:
    try:
        fifth.append(x[4])
        print(fifth)
    except IndexError:
        pass
'''


# Задание №9
# Дописать код (нельзя использовать просто except)

'''
my_dict ={"key1":"value1","key2":"value2","key3":"value3"}
try:
    search_key = "non-existent key"
    print(my_dict[search_key])
except KeyError:
    print(search_key, 'Это не тот ключ!')
else:
    print(search_key, 'Это тот ключ')
'''
# Задание №10
# Следующий код работает отлично, если пользователь вводит цифровое значение, но всегда есть НО:

'''
try:
    min = int(input("Введите первое число: "))
    max = int(input("Введите второе число: "))
except ValueError:
    print('Try again')
else:
    for i in range(min, max+1):
        print(f"Квадрат числа {i} равен {i*i}")

'''


# Задание №11
# Ловить ошибки это конечно здорово, но уметь логировать их и записывать в файл
# еще лучше, задача разобраться со стандартной библиотекой logging

'''
import logging # Загрузка библиотеки
logging.basicConfig(filename='my_error.log', format="%(asctime)s %(levelname)s %(message)s")
# Файл появится в том каталоге где запущен скрипт
logger = logging
try:
    1/0
except ZeroDivisionError as error:
    logger.error(error)
'''


# Задание №14
# Откройте файл romeo.txt. “Прочитайте” в нем каждую строку. 
# Получите отдельные слова из каждой строки, после чего 
# составьте список слов. В списке слова не должны дублироваться. 
# После чего распечатайте список, в котором все слова будут 
# отсортированы в алфавитном порядке. (используйте open)
'''
text = open("lesson 7/files/romeo.txt", mode="r", encoding='UTF-8').read().split()
text.sort()
print(text)
'''


