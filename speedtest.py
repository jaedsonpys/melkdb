# install Faker: pip install Faker

from faker import Faker
from melkdb import melkdb
from time import time

from random import randint

DATA_NUM = 1_000

fake = Faker()
db = melkdb.MelkDB('speedtest')

print('\033[33mGenerate names list...\033[m')

fake_value = {'address': fake.address(), 'text': fake.text()}
data = [(fake.name(), fake_value) for _ in range(DATA_NUM)]

print(f'\033[32m{len(data)} data generated\033[m')
print('-=' * 15)

print('\033[33mAdding all items to database...\033[m')
s_add = time()

for name, value in data:
    db.add(name, value)

e_add = time()
print(f'Add all names in {(e_add-s_add):.4f}')
print('-=' * 15)

print('\033[33mGetting all items from database...\033[m')
full_get_time = 0

for __ in range(DATA_NUM):
    choose = randint(0, DATA_NUM)
    name = data[choose][0]

    s_get = time()
    value = db.get(f'{name}/address')
    e_get = time()

    assert value == data[choose][1]['address']

    get_time = e_get-s_get
    full_get_time += get_time

print(f'\033[32mGet all items in {full_get_time:.4f}\033[m')