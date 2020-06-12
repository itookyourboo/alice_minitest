from random import choice


TEXT_HELLO = 'Привет!'
TEXT_NE_PONEL = 'Извините, я вас не понимаю'


def txt(string):
    return choice(string.split('/'))


def tkn(string):
    return tuple(string.split('/'))


def btn(string):
    if isinstance(string, tuple):
        return list(map(lambda x: txt(x), string))
    return txt(string),
