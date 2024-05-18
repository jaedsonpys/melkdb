# install Faker: pip install Faker

from faker import Faker
from melkdb import MelkDB
from time import time

DATA_NUM = 10_000

# If key is available, all test data will be encrypted
db = MelkDB('speedtest', encrypt_key='speedtest-secret-key')

data = list()
fake = Faker()

print('\033[33mGenerate names list...\033[m')

for __ in range(DATA_NUM):
    name = fake.name()
    data.append((name, name))

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

for choose in range(DATA_NUM):
    name = data[choose][0]

    s_get = time()
    value = db.get(name)
    e_get = time()

    assert value == data[choose][1]

    get_time = e_get-s_get
    full_get_time += get_time

print(f'\033[32mGet all items in {full_get_time:.4f}\033[m')