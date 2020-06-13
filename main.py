from base_skill.skill import *
from .strings import *
from .state import State
from .test_helper import get_new_test, get_top_test, get_random_test, COUNT


handler = CommandHandler()


@handler.hello_command
def hello(req, res, session):
    res.text = txt(TEXT_HELLO)
    session['state'] = State.MENU


@handler.command(words=tkn(WORDS_NEW), states=State.TEST_CALL)
def test_new(req, res, session):
    show_new_test(req, res, session, intro=True)
    session['state'] = State.CHOOSE_NEW


@handler.command(words=tkn(WORDS_TOP), states=State.TEST_CALL)
def test_top(req, res, session):
    show_top_test(req, res, session, intro=True)
    session['state'] = State.CHOOSE_TOP


@handler.command(words=tkn(WORDS_RND), states=State.TEST_CALL)
def test_rnd(req, res, session):
    show_rnd_test(req, res, session, intro=True)
    session['state'] = State.CHOOSE_RND


@handler.command(words=tkn(WORDS_PASS), states=State.CHOOSE)
def next_test(req, res, session):
    args = req, res, session, False
    {
        State.CHOOSE_NEW: show_new_test,
        State.CHOOSE_TOP: show_top_test,
        State.CHOOSE_RND: show_rnd_test,
    }[session['state']](*args)


@handler.undefined_command(states=State.ALL)
def ne_ponel(req, res, session):
    res.text = txt(TEXT_NE_PONEL)


def show_new_test(req, res, session, intro=False):
    session['new_idx'] = (session.get('new_idx', -1) + 1) % COUNT
    cycled, test = get_new_test(session['new_idx'])
    show_test_base(res, session, test, intro=intro, cycled=cycled)


def show_top_test(req, res, session, intro=False):
    session['top_idx'] = (session.get('top_idx', -1) + 1) % COUNT
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


class MinitestSkill(BaseSkill):
    name = 'minitest_skill'
    command_handler = handler
