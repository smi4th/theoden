from os import system

from tools import check

def test_1():
    system('python main.py -f tests/files/for/1.txt -t > tests/files/for/1.out.txt')
    assert check('tests/files/for/1.out.txt', 'tests/files/for/1_expected.txt')

def test_2():
    system('python main.py -f tests/files/for/2.txt -t > tests/files/for/2.out.txt')
    assert check('tests/files/for/2.out.txt', 'tests/files/for/2_expected.txt')

def test_3():
    system('python main.py -f tests/files/for/3.txt -t > tests/files/for/3.out.txt')
    assert check('tests/files/for/3.out.txt', 'tests/files/for/3_expected.txt')