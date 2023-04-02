# Задание №1

# Прописать метод строкового представления класса

'''
class Computer:
    def __init__(self, user, processor, RAM, memory, monitor):
        self.user = user
        self.processor = processor
        self.RAM = RAM
        self.memory = memory
        self.monitor = monitor
    def __str__(self):
        return f'User: {self.user}, Processor: {self.processor}, \
RAM: {self.RAM}, Memory: {self.memory}, Monitor: {self.monitor}'
'''

# Создать метод который будет возвращать имя владельца компьютера:

'''
class Computer:
    def __init__(self, user, processor, RAM, memory, monitor):
        self.user = user
        self.processor = processor
        self.RAM = RAM
        self.memory = memory
        self.monitor = monitor
        self.user_name()
    def user_name(self):
        return f'User name {self.user}'
'''
# Создать метод который будет сравнивать два класса по их ОЗУ
#