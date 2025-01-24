from os import system

from tools import check

def test_1():
    system('python main.py -f tests/files/while/1.txt -t > tests/files/while/1.out.txt')
    assert check('tests/files/while/1.out.txt', 'tests/files/while/1_expected.txt')

def test_2():
    system('python main.py -f tests/files/while/2.txt -t > tests/files/while/2.out.txt')
    assert check('tests/files/while/2.out.txt', 'tests/files/while/2_expected.txt')

def test_3():
    system('python main.py -f tests/files/while/3.txt -t > tests/files/while/3.out.txt')
    assert check('tests/files/while/3.out.txt', 'tests/files/while/3_expected.txt')