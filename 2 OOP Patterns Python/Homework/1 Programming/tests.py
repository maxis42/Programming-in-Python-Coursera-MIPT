import unittest


def factorize(x):
    """
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    pass


class TestFactorize(unittest.TestCase):
    """
    Необходимо написать комплект тестов используя модуль unittest
    стандартной библиотеки Python. Имя тестового класса - TestFactorize.

    ВАЖНО!  Все входные данные должны быть такими, как указано в условии.
    Название переменной в каждом тестовом случае должно быть именно "x". При
    этом несколько различных проверок в рамках одного теста должны быть
    обработаны как подслучаи с указанием x: subTest(x=...). В задании
    необходимо реализовать ТОЛЬКО класс TestFactorize, кроме этого
    реализовывать ничего не нужно. Импортировать unittest и вызывать
    unittest.main() в решении также не нужно.
    """
    def test_wrong_types_raise_exception(self):
        """
        test_wrong_types_raise_exception - проверяет, что передаваемый в функцию
        аргумент типа float или str вызывает исключение TypeError. Тестовый
        набор входных данных:  'string',  1.5
        :return:
        """
        for x in ["string", 1.5]:
            with self.subTest(x=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        """
        test_negative - проверяет, что передача в функцию factorize
        отрицательного числа вызывает исключение ValueError. Тестовый набор
        входных данных:   -1,  -10,  -100
        :return:
        """
        for x in [-1, -10, -100]:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        """
        test_zero_and_one_cases - проверяет, что при передаче в функцию целых
        чисел 0 и 1, возвращаются соответственно кортежи (0,) и (1,). Набор
        тестовых данных: 0 → (0, ),  1 → (1, )
        :return:
        """
        for x, ret in [
            (0, (0,)),
            (1, (1,))
        ]:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), ret)

    def test_simple_numbers(self):
        """
        test_simple_numbers - что для простых чисел возвращается кортеж,
        содержащий одно данное число. Набор тестовых данных: 3 → (3, ),
        13 → (13, ),   29 → (29, )
        :return:
        """
        for x, ret in [
            (3, (3,)),
            (13, (13,)),
            (29, (29,))
        ]:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), ret)

    def test_two_simple_multipliers(self):
        """
        test_two_simple_multipliers — проверяет случаи, когда передаются
        числа для которых функция factorize возвращает кортеж с числом элементов
        равным 2. Набор тестовых данных: 6 → (2, 3),   26 → (2, 13),
        121 --> (11, 11)
        :return:
        """
        for x, ret in [
            (6, (2, 3)),
            (26, (2, 13)),
            (121, (11, 11))
        ]:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), ret)

    def test_many_multipliers(self):
        """
        test_many_multipliers - проверяет случаи, когда передаются числа для
        которых функция factorize возвращает кортеж с числом элементов больше 2.
        Набор тестовых данных: 1001 → (7, 11, 13) ,
        9699690 → (2, 3, 5, 7, 11, 13, 17, 19)
        :return:
        """
        for x, ret in [
            (1001, (7, 11, 13)),
            (9699690, (2, 3, 5, 7, 11, 13, 17, 19))
        ]:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), ret)
