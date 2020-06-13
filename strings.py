from random import choice


TEXT_HELLO = 'Привет! Здесь вы можете пройти весёлые тесты.\n' \
             'Назовите категорию, чтобы начать: новое, популярное или случайное.\n' \
             'Или воспользуйтесь поиском, сказав название теста.'
TEXT_INTRO = 'Скажите "Дальше", чтобы показать другой, или "Начать", чтобы пройти тест.\n'
TEXT_RESTARTED = 'Вы просмотрели все тесты. Не переживайте, скоро будут новые!.\n'
TEXT_NE_PONEL = 'Извините, я вас не понимаю'

# TODO: Variations
WORDS_NEW = 'новое/новые/новая/новый/новых'
WORDS_TOP = 'топ/топовые/топовое/топовая/топовый/' \
            'лучший/лучшее/лучшая'
WORDS_RND = 'случайное/случайные/случайная/случайный/' \
            'любой/любое/любая/любые/' \
            'рандом/рандомное/рандомные/рандомная/рандомный'
WORDS_PASS = 'пройти/начать/старт'


def txt(string):
    return choice(string.split('/'))


def tkn(string):
    return tuple(string.split('/'))


def btn(string):
    if isinstance(string, tuple):
        return list(map(lambda x: txt(x), string))
    return txt(string),
