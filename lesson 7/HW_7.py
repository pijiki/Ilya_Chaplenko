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