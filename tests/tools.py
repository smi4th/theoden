from filecmp import cmp

def check(output, expected):
    return cmp(output, expected)

if __name__ == '__main__':

    dirs = [
        # 'conditions',
        'for',
        # 'functions',
        # 'while',
        # 'assign/add',
        # 'assign/complex',
        # 'assign/div',
        # 'assign/mod',
        # 'assign/mul',
        # 'assign/number',
        # 'assign/sub',
    ]

    import os, argparse

    parser = argparse.ArgumentParser(description='Run all the tests files, to generate the expected output')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode', required=False)
    args = parser.parse_args()

    for directory in dirs:
        for file in os.listdir(f'tests/files/{directory}'):
            if file.endswith('_expected.txt') or file.endswith('out.txt'):
                if args.verbose:
                    print(f"Removing {directory}/{file}")
                os.remove(f'tests/files/{directory}/{file}')

    for directory in dirs:
        for file in os.listdir(f'tests/files/{directory}'):
            if file.endswith('.txt'):
                if args.verbose:
                    print(f"Running {directory}/{file}")
                os.system(f'py main.py -f tests/files/{directory}/{file} -t > tests/files/{directory}/{file.replace(".txt", "")}_expected.txt')