from filecmp import cmp

def check(output, expected):
    return cmp(output, expected)

if __name__ == '__main__':

    dirs = [
        'conditions',
        'for',
        'functions',
        'while',
        'assign/add',
        'assign/complex',
        'assign/div',
        'assign/mod',
        'assign/mul',
        'assign/number',
        'assign/sub',
    ]

    import os, tqdm

    for directory in tqdm.tqdm(dirs, desc='Removing old expected files...'):
        for file in os.listdir(f'tests/files/{directory}'):
            if file.endswith('_expected.txt') or file.endswith('out.txt'):
                os.remove(f'tests/files/{directory}/{file}')
                
    for directory in tqdm.tqdm(dirs, desc='Creating new expected files...'):
        for file in os.listdir(f'tests/files/{directory}'):
            if file.endswith('.txt'):
                os.system(f'py main.py -f tests/files/{directory}/{file} -t > tests/files/{directory}/{file.replace(".txt", "")}_expected.txt')