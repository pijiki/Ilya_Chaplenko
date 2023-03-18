# ILya Chaplenko

# Задание №1
# Напишите функцию, чтобы найти максимальное из трех чисел


def who_is_bigger (a, b, c: int) -> int:
    """Функция которая ищет самое большое число из трех чисел"""
    if a < c > b:
        num = c
    elif a < b > c:
        num = b
    elif b < a > c:
        num = a
    else:
        num = "Все числа равны!"
    return num


        
