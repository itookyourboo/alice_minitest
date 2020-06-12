import os
from json import loads
from sqlite3 import connect
from random import choice


db = connect('database.db')
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
        return self.json_data['description']

    @property
    def process(self):
        return self.json_data['process']

    @property
    def intrigue(self):
        return choice(self.json_data['intrigue'])

    @property
    def result(self):
        return choice(self.json_data['result'])

    def like(self, user_id):
        cursor.execute('insert into likes(user_id, test_id) values(?, ?)', (user_id, self.id))
        db.commit()

    def get_likes(self):
        return cursor.execute(f'select count(*) from likes where test_id = {self.id}').fetchone()[0]

    def to_json(self):
        return self.json_data

    def __hash__(self):
        return hash(f'{self.id}_{self.name}')


with open('tests.json', 'r', encoding='utf8') as file:
    data = loads(file.read())
    tests = list(map(lambda x: Test(x), data))


def get_random_test():
    return choice(tests)


def get_top(n):
    n = min(len(tests),  n)
    return sorted(tests, key=lambda x: x.get_likes(), reverse=True)[:n]


def get_new(n):
    n = min(len(tests), n)
    return tests[-n:][::-1]

