# Задание №1
# В примере найти и вывести трехзначные числа с помощью регулярных выражений.

'''
import re
sample = 'Exercises number 1, 12, 13, and 345 are important 456'
print(re.findall(r'\d{3}', sample))
'''


# Задание №2
# Напишите регулярное выражение для поиска HTML-цвета, заданного 
# как #ABCDEF, то есть # и содержит затем 6 шестнадцатеричных символов.

'''
import re
collors = ['#ABCDEF', '#54#', '#F08080', '#FA8072', 'fghw3d', '#8B0000']
print(re.findall(r'#\S{6}', str(collors)))
'''

