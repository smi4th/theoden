from os import system

from tests.tools import check

def test_1():
    system('py main.py -f tests/files/conditions/1.txt -t > tests/files/conditions/1.out.txt')
    assert check('tests/files/conditions/1.out.txt', 'tests/files/conditions/1_expected.txt')

def test_2():
    system('py main.py -f tests/files/conditions/2.txt -t > tests/files/conditions/2.out.txt')
    assert check('tests/files/conditions/2.out.txt', 'tests/files/conditions/2_expected.txt')

def test_3():
    system('py main.py -f tests/files/conditions/3.txt -t > tests/files/conditions/3.out.txt')
    assert check('tests/files/conditions/3.out.txt', 'tests/files/conditions/3_expected.txt')

def test_4():
    system('py main.py -f tests/files/conditions/4.txt -t > tests/files/conditions/4.out.txt')
    assert check('tests/files/conditions/4.out.txt', 'tests/files/conditions/4_expected.txt')

def test_5():
    system('py main.py -f tests/files/conditions/5.txt -t > tests/files/conditions/5.out.txt')
    assert check('tests/files/conditions/5.out.txt', 'tests/files/conditions/5_expected.txt')

def test_6():
    system('py main.py -f tests/files/conditions/6.txt -t > tests/files/conditions/6.out.txt')
    assert check('tests/files/conditions/6.out.txt', 'tests/files/conditions/6_expected.txt')

def test_7():
    system('py main.py -f tests/files/conditions/7.txt -t > tests/files/conditions/7.out.txt')
    assert check('tests/files/conditions/7.out.txt', 'tests/files/conditions/7_expected.txt')