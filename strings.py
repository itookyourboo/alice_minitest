from random import choice
from .state import State

TEXT = {
    'hello': 'Привет! Здесь вы можете пройти весёлые тесты.\n'
             'Назовите категорию, чтобы начать: новое, популярное или случайное.',
    'can_search': 'Также вы можете воспользоваться поиском, сказав название теста',
    'intro': 'Скажите "Дальше", чтобы показать другой, или "Начать", чтобы пройти тест.\n',
    'restarted': 'Вы просмотрели все тесты. Не переживайте, скоро будут новые!\n',
    'ne_ponel': 'Извините, я вас не понимаю.\n'
                'Скажите "Помощь" или "Повтори", если не расслышали.',
    'back': 'Новое, популярное или случайное?\n'
            'Если вы хотите выйти, скажите ещё раз.',
    'bye': 'До свидания!/Пока!/До скорой встречи!',
    'enter_name': 'Введите ваше имя или имя друга.',
    'no_name': 'Извините, я не расслышала ваше имя, попробуйте ещё раз или скажите "Помощь".',
    'end_test': 'Чтобы пройти заново, назовите имя. Скажите "Дальше" для перехода к другому тесту.',
    'start': 'Стартуем!/Поехали!/Начинаем!',
    'wanna_like': 'Если вам понравился тест, скажите "Лайк"!',
    'already_liked': 'Вы уже лайкали этот тест!/Вы это уже делали ранее.',
    'thanks': 'Спасибо!/Благодарю!/Огромное спасибо!/Спасибо большое!',
    'not_found': 'Извините, я не нашла тестов с таким названием.',
    'found_1': 'Я нашла один тест.\n{}\n{}\n'
               'Если это он, скажите "Пройти". Если нет, скажите "Назад".',
    'found_several': 'Я нашла {} {}. Пролистать - "Дальше", выйти - "Назад", пройти тест - "Пройти".\n{}\n{}',
    'ability': 'Я даю вам веселые тесты, которые поднимут настроение вам и вашей компании :)',
    'rate': '⭐Оценить навык',
    'rated': 'Уже оценил(а)'
}

for t in TEXT:
    TEXT[t] = tuple(TEXT[t].split('/'))

HELP = {
    State.MENU: 'Чтобы найти тест, выберите категорию "Новое", "Популярное" или "Случайное".\n'
                'Если захотите его пройти, скажите "Старт", если нет - "Дальше" или "Выйти".',
    State.PASS_TEST: 'Назовите ваше имя или имя вашего друга. Не используйте псевдонимы.'
}
for choose in State.CHOOSE:
    HELP[choose] = 'Заинтересовало? Скажите "Пройти". Если хотите посмотреть ещё, скажите "Дальше"'

WORDS = {
    'new': 'новое/новые/новая/новый/новых',
    'top': 'топ/топовые/топовое/топовая/топовый/'
           'лучший/лучшее/лучшая/популярное/популярные/популярная',
    'rnd': 'случайное/случайные/случайная/случайный/'
           'любой/любое/любая/любые/случайно/'
           'рандом/рандомное/рандомные/рандомная/рандомный',
    'rated': 'оценить/оценил/оценила/оценило/оценка',
    'next': 'еще/ещё/дальше/больше/вперед/вперёд/следующая/следующий/'
            'следующее/далее/не/неа/фу/нет/другой/другое/другая/другие',
    'pass': 'пройти/начать/старт/играть/давай/начинай/хорошо/сыграем/поиграем/'
            'го/погнали/да/го/запускай/поехали',
    'like': 'лайк/принят/принято/класс/клёво/хорошо/отлично/классное/'
            'классный/классная/прикольно/прикольный/прикольная/прикольное/'
            'хорошее/хороший/хорошая/может/отличное/отличный/отличная/'
            'нормально/нормальное/нормальный/интересно/интересный/интересная/'
            'круто/неплохо/да/пойду/понравилась/понравилось/подумаю/вау/'
            'понравился/сделаю/возьму/заметку/заметка/хайпово/нравится/'
            'понравится/хочу/люблю/крутой/крутая/крутое/круть/отпад/вау/ого/нифига/'
            'флекс/хайп/красивая/красивый/красивое/красивые/лайки',
    'help': 'помощь/помоги/подсказка/подскажи/подскажите/help/правила',
    'ability': 'умеешь/можешь/могёшь/могешь',
    'repeat': 'ещё/еще/повтори/повтори-ка/повтор/понял/слышал/услышал/расслышал/прослушал/скажи/а/сказала',
    'exit': 'выход/хватит/пока/свидания/стоп/выйти/выключи/останови/остановить/отмена/закончить/'
            'закончи/отстань/назад/обратно/верни/вернись'
}
for w in WORDS:
    WORDS[w] = tuple(WORDS[w].split('/'))

EMOJI = {
    'new': '💡',
    'top': '🔥',
    'rnd': '🎲',
    'help': '❓',
    'ability': '🌐',
    'pass': '📝',
    'back': '🏠',
    'more': '➡️',
    'repeat': '👂',
    'like': '❤'
}

BUTTONS = {
    State.MENU: (f'{EMOJI["new"]}Новое', f'{EMOJI["top"]}Популярное', f'{EMOJI["rnd"]}Случайное',
                 f'{EMOJI["help"]}Помощь', f'{EMOJI["ability"]}Что ты умеешь?'),
    State.PASS_TEST: ('Александр/Андрей/Илья/Егор/Даниил/Олег',
                      'Анжела/Настя/Яна/Оля/Лена/Вера/Алина/Аня',
                      f'{EMOJI["back"]}Назад'),
    State.CHOOSE_FOUND: (f'{EMOJI["pass"]}Пройти', f'{EMOJI["back"]}Назад', f'{EMOJI["repeat"]}Повтори')
}

BUTTON_NEXT_TEST = f'{EMOJI["more"]}Другой тест'
BUTTON_LIKE = f'{EMOJI["like"]}Лайк'

for choose in State.CHOOSE[:-1]:
    BUTTONS[choose] = (f'{EMOJI["pass"]}Пройти', f'{EMOJI["more"]}Дальше/{EMOJI["more"]}Ещё/{EMOJI["more"]}Далее',
                       f'{EMOJI["back"]}Назад', f'{EMOJI["repeat"]}Повтори')


def txt(string):
    return choice(string)


def btn(string):
    if isinstance(string, tuple):
        return list(map(lambda x: txt(x.split('/')), string))
    return txt(string.split('/')),
