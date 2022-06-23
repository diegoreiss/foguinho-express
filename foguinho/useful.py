from time import sleep
from os import system

    
def header1(msg):
    print('=' * 50)
    print(f'{msg:^50}')
    print('=' * 50)
    

def header2(msg):
    print('=-' * 25)
    print(f'{msg:^50}')
    print('=-' * 25)
    

def end_points(msg):
    print(msg, end='')
    for _ in range(4):
        print('.', end='', flush=True)
        sleep(0.5)
    print()
    system('clear')