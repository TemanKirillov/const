#!/usr/bin/python3 
'''
+ 
    Инкапсуляция всех констант в одном месте
    Пространство имён модуля не захламлено
    Строки документации для констант
    Расширение набора констант наследованием

-
    Усложнение кода
    Дополнительный ввод имени класса для доступа к константе

'''

class Const:
    def __init__(self, value, doc):
        self.value = value
        self.doc = doc
        self.__doc__ = '= {!r}\n(CONST) {}'.format(value, self.doc)
    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return self.value

    def __set__(self, instance, value):
        raise AttributeError("can't set attribute")

    def __repr__(self):
        return 'Const(value={}, doc={})'.format(repr(self.value), repr(self.__doc__))

def const_class(cls):
    ''' Декоратор класса, который содержит только константы. 
        Определяет дополнительное поведение. '''

    @classmethod
    def to_global(cls):
        ''' Метод класса. Копирует все определённые константы в глобальную область видимости. '''
        dct = dict(cls.__iter__())
        globals().update(dct)

    @classmethod
    def __iter__(cls):
        return ((name, const.value) for name, const in cls.__dict__.items() if isinstance(const, Const))

    cls.to_global = to_global
    cls.__iter__ = __iter__
    instance = cls()
    return instance


        

def test():
    #from extract_doc import getmembers
    #[print(i) for i in getmembers('C', C)]
    #c = C()

    @const_class
    class C:
        AUTHOR = Const('Teman', 'the author of the module')

    print(C.AUTHOR)
    try:
        C.AUTHOR = 'alex'
    except AttributeError as e:
        print('Перехвачено исключение', e)
    C.to_global()
    print(AUTHOR)
    print(dict(C))
    help(C)
    #[print(i) for i in getmembers('c', c)]

if __name__ == '__main__':
    test()
