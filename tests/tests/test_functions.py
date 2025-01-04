from os import system

from tests.tools import check

def test_1():
    system('py main.py -f tests/files/functions/1.txt -t > tests/files/functions/1.out.txt')
    assert check('tests/files/functions/1.out.txt', 'tests/files/functions/1_expected.txt')

def test_2():
    system('py main.py -f tests/files/functions/2.txt -t > tests/files/functions/2.out.txt')
    assert check('tests/files/functions/2.out.txt', 'tests/files/functions/2_expected.txt')

def test_3():
    system('py main.py -f tests/files/functions/3.txt -t > tests/files/functions/3.out.txt')
    assert check('tests/files/functions/3.out.txt', 'tests/files/functions/3_expected.txt')

def test_4():
    system('py main.py -f tests/files/functions/4.txt -t > tests/files/functions/4.out.txt')
    assert check('tests/files/functions/4.out.txt', 'tests/files/functions/4_expected.txt')

def test_5():
    system('py main.py -f tests/files/functions/5.txt -t > tests/files/functions/5.out.txt')
    assert check('tests/files/functions/5.out.txt', 'tests/files/functions/5_expected.txt')

def test_6():
    system('py main.py -f tests/files/functions/6.txt -t > tests/files/functions/6.out.txt')
    assert check('tests/files/functions/6.out.txt', 'tests/files/functions/6_expected.txt')

def test_7():
    system('py main.py -f tests/files/functions/7.txt -t > tests/files/functions/7.out.txt')
    assert check('tests/files/functions/7.out.txt', 'tests/files/functions/7_expected.txt')

def test_8():
    system('py main.py -f tests/files/functions/8.txt -t > tests/files/functions/8.out.txt')
    assert check('tests/files/functions/8.out.txt', 'tests/files/functions/8_expected.txt')

def test_9():
    system('py main.py -f tests/files/functions/9.txt -t > tests/files/functions/9.out.txt')
    assert check('tests/files/functions/9.out.txt', 'tests/files/functions/9_expected.txt')

def test_10():
    system('py main.py -f tests/files/functions/10.txt -t > tests/files/functions/10.out.txt')
    assert check('tests/files/functions/10.out.txt', 'tests/files/functions/10_expected.txt')