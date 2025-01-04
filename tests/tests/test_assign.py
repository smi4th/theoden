from os import system

from tests.tools import check

def test_add_1():
    system('py main.py -f tests/files/assign/add/1.txt -t > tests/files/assign/add/1.out.txt')
    assert check('tests/files/assign/add/1.out.txt', 'tests/files/assign/add/1_expected.txt')

def test_add_2():
    system('py main.py -f tests/files/assign/add/2.txt -t > tests/files/assign/add/2.out.txt')
    assert check('tests/files/assign/add/2.out.txt', 'tests/files/assign/add/2_expected.txt')

def test_complex_1():
    system('py main.py -f tests/files/assign/complex/1.txt -t > tests/files/assign/complex/1.out.txt')
    assert check('tests/files/assign/complex/1.out.txt', 'tests/files/assign/complex/1_expected.txt')

def test_div_1():
    system('py main.py -f tests/files/assign/div/1.txt -t > tests/files/assign/div/1.out.txt')
    assert check('tests/files/assign/div/1.out.txt', 'tests/files/assign/div/1_expected.txt')

def test_div_2():
    system('py main.py -f tests/files/assign/div/2.txt -t > tests/files/assign/div/2.out.txt')
    assert check('tests/files/assign/div/2.out.txt', 'tests/files/assign/div/2_expected.txt')

def test_mul_1():
    system('py main.py -f tests/files/assign/mul/1.txt -t > tests/files/assign/mul/1.out.txt')
    assert check('tests/files/assign/mul/1.out.txt', 'tests/files/assign/mul/1_expected.txt')

def test_mul_2():
    system('py main.py -f tests/files/assign/mul/2.txt -t > tests/files/assign/mul/2.out.txt')
    assert check('tests/files/assign/mul/2.out.txt', 'tests/files/assign/mul/2_expected.txt')

def test_number_1():
    system('py main.py -f tests/files/assign/number/1.txt -t > tests/files/assign/number/1.out.txt')
    assert check('tests/files/assign/number/1.out.txt', 'tests/files/assign/number/1_expected.txt')

def test_number_2():
    system('py main.py -f tests/files/assign/number/2.txt -t > tests/files/assign/number/2.out.txt')
    assert check('tests/files/assign/number/2.out.txt', 'tests/files/assign/number/2_expected.txt')

def test_sub_1():
    system('py main.py -f tests/files/assign/sub/1.txt -t > tests/files/assign/sub/1.out.txt')
    assert check('tests/files/assign/sub/1.out.txt', 'tests/files/assign/sub/1_expected.txt')

def test_sub_2():
    system('py main.py -f tests/files/assign/sub/2.txt -t > tests/files/assign/sub/2.out.txt')
    assert check('tests/files/assign/sub/2.out.txt', 'tests/files/assign/sub/2_expected.txt')