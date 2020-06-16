import os
from json import loads
from sqlite3 import connect
from random import choice

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'tests.json')
DB_PATH = os.path.join(BASE_DIR, 'database.db')

db = connect(DB_PATH)
cursor = db.cursor()
cursor.execute('create table if not exists likes('
               'id integer primary key autoincrement,'
               'user_id string not null,'
               'test_id integer not null);')
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
