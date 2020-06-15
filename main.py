from base_skill.skill import *
from .strings import *
from .state import State
from .test_helper import get_new_test, get_top_test, get_random_test, COUNT


handler = CommandHandler()


def default_buttons(func):
    def wrapper(req, res, session):
        func(req, res, session)
        if len(res.buttons) == 0:
            res.buttons = [button(x) for x in btn(BUTTONS[session['state']])]
        else:
            for x in btn(BUTTONS[session['state']]):
                res.buttons.append(button(x))

    return wrapper


@handler.hello_command
@default_buttons
def hello(req, res, session):
    res.text = txt(TEXT_HELLO)
    session['state'] = State.MENU


@handler.command(words=tkn(WORDS_NEW), states=State.TEST_CALL)
@default_buttons
def test_new(req, res, session):
    show_new_test(req, res, session, intro=True)
    session['state'] = State.CHOOSE_NEW


@handler.command(words=tkn(WORDS_TOP), states=State.TEST_CALL)
@default_buttons
def test_top(req, res, session):
    show_top_test(req, res, session, intro=True)
    session['state'] = State.CHOOSE_TOP


@handler.command(words=tkn(WORDS_RND), states=State.TEST_CALL)
@default_buttons
def test_rnd(req, res, session):
    show_rnd_test(req, res, session, intro=True)
    session['state'] = State.CHOOSE_RND


@handler.command(words=tkn(WORDS_NEXT), states=State.CHOOSE)
@default_buttons
def next_test(req, res, session):
    args = req, res, session, False
    {
        State.CHOOSE_NEW: show_new_test,
        State.CHOOSE_TOP: show_top_test,
        State.CHOOSE_RND: show_rnd_test,
    }[session['state']](*args)


@handler.command(words=tkn(WORDS_PASS), states=State.CHOOSE)
@default_buttons
def enter_the_name(req, res, session):
    res.text = txt(TEXT_ENTER_THE_NAME)
    session['state'] = State.NAME


@handler.undefined_command(states=State.NAME)
@default_buttons
def check_name(req, res, session):
    contains_name = False
    for e in req.entities:
        if e['type'] == 'YANDEX.FIO':
            session['name'] = ' '.join(e['value'][i].capitalize() for i in e['value'])
            contains_name = True
            break

    if not contains_name:
        res.text = txt(TEXT_NO_NAME)
        return

    start_test(req, res, session)


@handler.command(words=tkn(WORDS_EXIT), states=State.CHOOSE + (State.NAME, ))
@default_buttons
def back(req, res, session):
    session['state'] = State.MENU
    res.text = txt(TEXT_BACK)


@handler.command(words=tkn(WORDS_EXIT), states=State.MENU)
def leave_skill(req, res, session):
    res.text = txt(TEXT_BYE)
    res.end_session = True
    session.clear()


@handler.undefined_command(states=State.ALL)
@default_buttons
def ne_ponel(req, res, session):
    res.text = txt(TEXT_NE_PONEL)


def show_new_test(req, res, session, intro=False):
    session['new_idx'] = session.get('new_idx', -1) + 1
    cycled, test = get_new_test(session['new_idx'])
    show_test_base(res, session, test, intro=intro, cycled=cycled)


def show_top_test(req, res, session, intro=False):
    session['top_idx'] = session.get('top_idx', -1) + 1
    cycled, test = get_top_test(session['top_idx'])
    show_test_base(res, session, test, intro=intro, cycled=cycled)


def show_rnd_test(req, res, session, intro=False):
    test = get_random_test()
    show_test_base(res, session, test, intro=intro)


def show_test_base(res, session, test, intro=False, cycled=False):
    intro_text = '' if not intro else txt(TEXT_INTRO)
    if cycled:
        intro_text += txt(TEXT_RESTARTED)

    res.text = f'{intro_text}{test}'
    session['test'] = test


def start_test(req, res, session):
    test = session['test']
    name = session['name']
    res.text = f'{name}\n{test.name}\n{test.intrigue}\n{test.result}'


class MinitestSkill(BaseSkill):
    name = 'minitest_skill'
    command_handler = handler
