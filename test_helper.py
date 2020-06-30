import os
from difflib import SequenceMatcher as sequence
from json import loads
from sqlite3 import connect
from random import choice


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'tests.json')
DB_PATH = os.path.join(BASE_DIR, 'database.db')
MIN_MATCH = 0.6

db = connect(DB_PATH)
cursor = db.cursor()
cursor.execute('create table if not exists likes('
               'id integer primary key autoincrement,'
               'user_id string not null,'
               'test_id integer not null);')
cursor.execute('create table if not exists rated('
               'id integer primary key autoincrement,'
               'user_id string not null'
               ');')
db.commit()


class Test:
    def __init__(self, json_data):
        self.json_data = json_data

    @property
    def id(self):
        return self.json_data['id']

    @property
    def name(self):
        return self.json_data['name']

    @property
    def description(self):
        return self.json_data.get('description')

    @property
    def process(self):
        return self.json_data.get('process')

    @property
    def intrigue(self):
        return choice(self.json_data['intrigue'])

    @property
    def result(self):
        return choice(self.json_data['result'])

    @property
    def results(self):
        return self.json_data['result']

    def like(self, user_id):
        cursor.execute('insert into likes(user_id, test_id) values(?, ?)', (user_id, self.id))
        db.commit()

    def liked(self, user_id):
        return cursor.execute(
            f"select * from likes where user_id = '{user_id}' and test_id = {self.id}").fetchone() is not None

    def get_likes(self):
        return cursor.execute(f'select count(*) from likes where test_id = {self.id}').fetchone()[0]

    def to_json(self):
        return self.json_data

    def __str__(self):
        return f'{self.name}\n{self.description}'

    def __hash__(self):
        return hash(f'{self.id}_{self.name}')


with open(JSON_PATH, 'r', encoding='utf8') as file:
    data = loads(file.read())
    tests = list(map(lambda x: Test(x), data))
    top = sorted(tests, key=lambda x: x.get_likes(), reverse=True)
    new = tests[::-1]
    COUNT = len(tests)


def get_random_test():
    return choice(tests)


# Returns True, if it cycles
def get_top_test(idx):
    return idx >= COUNT, top[idx % COUNT]


# Analogically
def get_new_test(idx):
    return idx >= COUNT, new[idx % COUNT]


def get_top(n):
    n = min(COUNT, n)
    return sorted(tests, key=lambda x: x.get_likes(), reverse=True)[:n]


def get_new(n):
    n = min(COUNT, n)
    return tests[-n:][::-1]


def has_rated(user_id):
    return cursor.execute(f"select * from rated where user_id = '{user_id}'").fetchone() is not None


def rate_skill(user_id):
    if has_rated(user_id):
        return
    else:
        cursor.execute('insert into rated (user_id) values(?)', (user_id, ))
        db.commit()


def add_wtf(text):
    with open(os.path.join(BASE_DIR, 'wtf.txt'), 'a', encoding='utf8') as file:
        file.write(text + '\n')


def try_to_find_test(text):
    text = text.lower()
    mx = MIN_MATCH
    result = None
    for test in tests:
        mx_diff = max(map(lambda x: sequence(None, text, x).ratio(),
                          [test.name.lower(), test.description.lower()]))
        if mx_diff > mx:
            result = test
            mx = mx_diff

    return result


def morph_words(num):
    if 10 <= num % 100 <= 20:
        return 'тестов'

    elif (num % 10) in (0, 5, 6, 7, 8, 9):
        return 'тестов'

    elif num % 10 == 1:
        return 'тест'
    elif (num % 10) in (2, 3, 4):
        return 'теста'


if __name__ == '__main__':
    while True:
        cursor.execute(input())
        [print(i) for i in cursor.fetchall()]
        db.commit()