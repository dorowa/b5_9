#!/usr/local/bin/python3
import time

#сколько проходов делать в заглушке
ITER = 100000

#ДАЛЬШЕ ВНИЗУ РЕАЛИЗОВАНЫ ВСЕ ПРЕДЛОЖЕННЫЕ ЗАДАЧИ!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#простой декоратор при помощи функций
#тройное вложение, позволяет указать нужное количество итераций
#для оценки среднего времени выполнения функции
def deco_time(times_to_cals):
    def out_line_(func):
        def inline_(*params, **params2): #оставим задел на случай, если функции нужно передать аргументы
            delta_ = []  #список замеров времени выполнения
            for i in range(times_to_cals+1):
                start_ = time.time() #начало отсчета времени
                ret = func(*params,**params2) #выполняем работу
                end_ = time.time() #окончание работы
                delta = end_ - start_ #длительность выполнения функции
                #print(delta) #можно раскомментировать чтобы посмотреть промежуточный вывод
                delta_.append(delta)
            print(f"    Среднее время выполнения: {sum(delta_)/len(delta_)}")
            return ret
        return inline_
    return out_line_

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#декоратор через - КЛАСС (Вариант 1)
#переопределение без @декоратор, но принцип тот же
#получаем функцию и количество запусков при инициализации обьекта класса
class DeClass:
    def __init__(self,func,times_to_cal):
        self.delta = 0
        self.__delta_block = 0
        self.__delta_block_0 = 0
        self.__delta_block_1 = 0
        def class_deco_time(times_to_cal):
            def class_out_line_(func):
                self.func_name = func.__name__ #сохраняем имя исходной функции для вывода
                def class_inline_(*params, **params2): #оставляем возможность передать аргументы
                    delta_ = []
                    for i in range(times_to_cal+1):
                        start_ = time.time()
                        ret = func(*params,**params2)
                        end_ = time.time()
                        delta = end_ - start_
                        #print(delta) #раскоментировать для промеж результатов
                        delta_.append(delta)
                    self.delta = sum(delta_)/len(delta_)
                    return ret
                return class_inline_
            return class_out_line_
        self.func = class_deco_time(times_to_cal)(func)
    def __enter__(self):
        self.__delta_block_0 = time.time() #фиксируем время входа в контекст
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__delta_block_1 = time.time() #фиксируем время выхода из блока
        self.__delta_block = self.__delta_block_1 - self.__delta_block_0
        print(f"    Среднее время выполнения функции {self.func_name} в блоке: {self.delta}")
        print(f"    Время выполнения блока операторов: {self.__delta_block}")

    def __call__(self):
        return self.func #возвращаем декорированную функцию
    
    def __str__(self):
        return f"{self.delta}"


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#декоратор через - КЛАСС (Вариант 2)
#декоратор через метод обьекта класса по феншую @ или вариант2

class D2class:
    def __init__(self):
        self.delta = 0
        self.__delta_block_0 = 0
        self.__delta_block_1 = 0
        self.__delta_block = 0
    #определяем меджик-метод для "вызова", чтобы можно было декорировать вызовом метода через @
    def __call__(self,times_to_call):
        def out_line_(func):
            self.func_name = func.__name__ #сохраняем имя функции
            def inline_(*params, **params2): #при необходимости передаем аргументы
                delta_ = []
                for i in range(times_to_call+1):
                    start_ = time.time()
                    ret = func(*params,**params2) #сохраняем результат выполнения функции, чтоб вернуть по-людски
                    end_ = time.time()
                    delta = end_ - start_
                    #print(i,delta)
                    delta_.append(delta)
                self.delta = sum(delta_)/len(delta_) #можно вывод поставить тут, чтобы минимально влиять на основной код
                return ret
            return inline_
        return out_line_
    def __enter__(self):
        self.__delta_block_0 = time.time()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.__delta_block_1 = time.time()
        self.__delta_block = self.__delta_block_1 - self.__delta_block_0
        print(f"    Среднее время выполнения функции {self.func_name} в блоке: {self.delta} сек.")
        print(f"    Время выполнения блока операторов: {self.__delta_block} сек.")

    def __str__(self):
        return f"{self.delta}"



def main():
    #первым параметром указываем количество повторных вызовов функции
    #тут и далее аргументы data1, data2, data3, data4 используются
    #только для примера транзита аргументов в декорируемую функцию
    @deco_time(100)
    def test_test(data1, data2, data3 = 15, data4 = 16): #передаем аргументы функции 
        #print(f"data1 = {data1}, data2 = {data2}, data3 = {data3}, data4 = {data4}") #раскоментировать промежуточный вывод
        for j in range(ITER):
            pass

    print("Простой декоратор")
    test_test(1,2,4,5)
    print("-"*50)

    #========================ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ===========================
    #------------------функция для рассчета Number-ного элемента ряда Фибоначчи
    def fibb(Number=0):
        if Number == 0: return 1
        if Number == 1: return 2
        fib = [1,2]
        fib_next = 0
        for i in range(2,Number+1):
            fib_next = fib[0]+fib[1]
            fib[0],fib[1] = fib[1], fib_next
        return fib_next
    #----функция для вывода номера элемента ряда Фибоначчи меньшего чем Number
    def get_under_fib(Number):
        i = 1
        while fibb(i)<Number:
            i+=1
        return (i-1)
    #==========================================================================
    
    #вариант №1 Класс с декоратором и менеджером контента
    #проверочная функция        
    def class_test_test(data3 = 15, data4 = 16):
        #print(f"data1 = {data1}, data2 = {data2}, data3 = {data3}, data4 = {data4}") #раскоментировать если нужен промежуточный вывод
        for j in range(ITER):
            pass

    metricA = DeClass(class_test_test, 100)
    class_test_test = metricA() #декорируем функцию
    class_test_test(15,16)
    print("Декоратор через класс, вариант 1")
    print("    Среднее время выполнения функции:",metricA)
    #теперь тот же класс через контекст менеджер
    print("Декоратор в контекстном менеджере")
    #тут протестируем функции Фибонначи
    with DeClass(get_under_fib,5) as d_guf:
        get_under_fib = d_guf() #декорируем функцию
        Nm = 40000000000000000000000
        print(f"    {Nm} всего лишь: {get_under_fib(Nm)}-й")
    print("-"*50)
    
    #вариант №2 Класс с декоратором и менеджером контента, декорация через @
    print("Декоратор в классе, вариант2")
    d2 = D2class()

    #декорируем функцию
    @d2(100)
    def d2_test_test(data1, data2, data3 = 15, data4 = 16):
        #print(f"data1 = {data1}, data2 = {data2}, data3 = {data3}, data4 = {data4}")
        for j in range(data1,data2):
            pass
            #print(data3**data4)

    d2_test_test(1, ITER, data3 = 50, data4 = 50)
    print("    Среднее время выполнения функции:",d2)
    #print("-"*50)
    print("Вариант2 через менеджер контекста with:")

    #добавим немного Фибоначчи
    with D2class() as f2:
        @f2(10) #декорируем функцию, при вызове - вызываем в цикле 10 раз, для вычисления среднего времени
        def fibb(Number=0):
            if Number == 0: return 1
            if Number == 1: return 2
            fib = [1,2]
            fib_next = 0
            for i in range(2,Number+1):
                fib_next = fib[0]+fib[1]
                fib[0],fib[1] = fib[1], fib_next
            return fib_next
        Nm = 107
        print(f"    {Nm}-е число ряда: {fibb(Nm)}")

if __name__ == "__main__":
    main()






