from os import system

from tools import check

def test_add_1():
    system('python main.py -f tests/files/assign/add/1.txt -t > tests/files/assign/add/1.out.txt')
    assert check('tests/files/assign/add/1.out.txt', 'tests/files/assign/add/1_expected.txt')

def test_add_2():
    system('python main.py -f tests/files/assign/add/2.txt -t > tests/files/assign/add/2.out.txt')
    assert check('tests/files/assign/add/2.out.txt', 'tests/files/assign/add/2_expected.txt')

def test_add_3():
    system('python main.py -f tests/files/assign/add/3.txt -t > tests/files/assign/add/3.out.txt')
    assert check('tests/files/assign/add/3.out.txt', 'tests/files/assign/add/3_expected.txt')

def test_complex_1():
    system('python main.py -f tests/files/assign/complex/1.txt -t > tests/files/assign/complex/1.out.txt')
    assert check('tests/files/assign/complex/1.out.txt', 'tests/files/assign/complex/1_expected.txt')

def test_div_1():
    system('python main.py -f tests/files/assign/div/1.txt -t > tests/files/assign/div/1.out.txt')
    assert check('tests/files/assign/div/1.out.txt', 'tests/files/assign/div/1_expected.txt')

def test_div_2():
    system('python main.py -f tests/files/assign/div/2.txt -t > tests/files/assign/div/2.out.txt')
    assert check('tests/files/assign/div/2.out.txt', 'tests/files/assign/div/2_expected.txt')

def test_div_3():
    system('python main.py -f tests/files/assign/div/3.txt -t > tests/files/assign/div/3.out.txt')
    assert check('tests/files/assign/div/3.out.txt', 'tests/files/assign/div/3_expected.txt')

def test_mod_1():
    system('python main.py -f tests/files/assign/mod/1.txt -t > tests/files/assign/mod/1.out.txt')
    assert check('tests/files/assign/mod/1.out.txt', 'tests/files/assign/mod/1_expected.txt')

def test_mod_2():
    system('python main.py -f tests/files/assign/mod/2.txt -t > tests/files/assign/mod/2.out.txt')
    assert check('tests/files/assign/mod/2.out.txt', 'tests/files/assign/mod/2_expected.txt')

def test_mod_3():
    system('python main.py -f tests/files/assign/mod/3.txt -t > tests/files/assign/mod/3.out.txt')
    assert check('tests/files/assign/mod/3.out.txt', 'tests/files/assign/mod/3_expected.txt')

def test_mod_4():
    system('python main.py -f tests/files/assign/mod/4.txt -t > tests/files/assign/mod/4.out.txt')
    assert check('tests/files/assign/mod/4.out.txt', 'tests/files/assign/mod/4_expected.txt')

def test_mul_1():
    system('python main.py -f tests/files/assign/mul/1.txt -t > tests/files/assign/mul/1.out.txt')
    assert check('tests/files/assign/mul/1.out.txt', 'tests/files/assign/mul/1_expected.txt')

def test_mul_2():
    system('python main.py -f tests/files/assign/mul/2.txt -t > tests/files/assign/mul/2.out.txt')
    assert check('tests/files/assign/mul/2.out.txt', 'tests/files/assign/mul/2_expected.txt')

def test_mul_3():
    system('python main.py -f tests/files/assign/mul/3.txt -t > tests/files/assign/mul/3.out.txt')
    assert check('tests/files/assign/mul/3.out.txt', 'tests/files/assign/mul/3_expected.txt')

def test_number_1():
    system('python main.py -f tests/files/assign/number/1.txt -t > tests/files/assign/number/1.out.txt')
    assert check('tests/files/assign/number/1.out.txt', 'tests/files/assign/number/1_expected.txt')

def test_number_2():
    system('python main.py -f tests/files/assign/number/2.txt -t > tests/files/assign/number/2.out.txt')
    assert check('tests/files/assign/number/2.out.txt', 'tests/files/assign/number/2_expected.txt')

def test_number_3():
    system('python main.py -f tests/files/assign/number/3.txt -t > tests/files/assign/number/3.out.txt')
    assert check('tests/files/assign/number/3.out.txt', 'tests/files/assign/number/3_expected.txt')

def test_number_4():
    system('python main.py -f tests/files/assign/number/4.txt -t > tests/files/assign/number/4.out.txt')
    assert check('tests/files/assign/number/4.out.txt', 'tests/files/assign/number/4_expected.txt')

def test_number_5():
    system('python main.py -f tests/files/assign/number/5.txt -t > tests/files/assign/number/5.out.txt')
    assert check('tests/files/assign/number/5.out.txt', 'tests/files/assign/number/5_expected.txt')

def test_sub_1():
    system('python main.py -f tests/files/assign/sub/1.txt -t > tests/files/assign/sub/1.out.txt')
    assert check('tests/files/assign/sub/1.out.txt', 'tests/files/assign/sub/1_expected.txt')

def test_sub_2():
    system('python main.py -f tests/files/assign/sub/2.txt -t > tests/files/assign/sub/2.out.txt')
    assert check('tests/files/assign/sub/2.out.txt', 'tests/files/assign/sub/2_expected.txt')

def test_sub_3():
    system('python main.py -f tests/files/assign/sub/3.txt -t > tests/files/assign/sub/3.out.txt')
    assert check('tests/files/assign/sub/3.out.txt', 'tests/files/assign/sub/3_expected.txt')

def test_chars_1():
    system('python main.py -f tests/files/assign/chars/1.txt -t > tests/files/assign/chars/1.out.txt')
    assert check('tests/files/assign/chars/1.out.txt', 'tests/files/assign/chars/1_expected.txt')

def test_chars_2():
    system('python main.py -f tests/files/assign/chars/2.txt -t > tests/files/assign/chars/2.out.txt')
    assert check('tests/files/assign/chars/2.out.txt', 'tests/files/assign/chars/2_expected.txt')

def test_array_1():
    system('python main.py -f tests/files/assign/array/1.txt -t > tests/files/assign/array/1.out.txt')
    assert check('tests/files/assign/array/1.out.txt', 'tests/files/assign/array/1_expected.txt')

def test_array_2():
    system('python main.py -f tests/files/assign/array/2.txt -t > tests/files/assign/array/2.out.txt')
    assert check('tests/files/assign/array/2.out.txt', 'tests/files/assign/array/2_expected.txt')

def test_array_3():
    system('python main.py -f tests/files/assign/array/3.txt -t > tests/files/assign/array/3.out.txt')
    assert check('tests/files/assign/array/3.out.txt', 'tests/files/assign/array/3_expected.txt')

def test_array_4():
    system('python main.py -f tests/files/assign/array/4.txt -t > tests/files/assign/array/4.out.txt')
    assert check('tests/files/assign/array/4.out.txt', 'tests/files/assign/array/4_expected.txt')

def test_array_5():
    system('python main.py -f tests/files/assign/array/5.txt -t > tests/files/assign/array/5.out.txt')
    assert check('tests/files/assign/array/5.out.txt', 'tests/files/assign/array/5_expected.txt')

def test_array_6():
    system('python main.py -f tests/files/assign/array/6.txt -t > tests/files/assign/array/6.out.txt')
    assert check('tests/files/assign/array/6.out.txt', 'tests/files/assign/array/6_expected.txt')

def test_array_7():
    system('python main.py -f tests/files/assign/array/7.txt -t > tests/files/assign/array/7.out.txt')
    assert check('tests/files/assign/array/7.out.txt', 'tests/files/assign/array/7_expected.txt')