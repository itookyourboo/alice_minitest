from base_skill.skill import *
from .strings import *
from .state import State
from .test_helper import get_new_test, get_top_test, get_random_test, add_wtf, try_to_find_test, morph_words
from .ui_helper import default_buttons, save_last_text, normalize_tts


handler = CommandHandler()


@handler.hello_command
@save_last_text
@normalize_tts
@default_buttons
def hello(req, res, session):
    res.text = txt(TEXT_HELLO)
    session['state'] = State.MENU


@handler.undefined_command(states=State.MENU)
@save_last_text
@default_buttons
def find_test(req, res, session):
    test = try_to_find_test(req.text)
    if test:
        res.text = txt(TEXT_FOUND_1).format(test.name, test.description)
        session['test'] = test
        session['state'] = State.CHOOSE_FOUND
    else:
        res.text = txt(TEXT_NOT_FOUND)


@handler.command(words=tkn(WORDS_NEW), states=State.TEST_CALL)
@save_last_text
@default_buttons
def test_new(req, res, session):
    show_new_test(req, res, session, intro=True)
    session['state'] = State.CHOOSE_NEW


@handler.command(words=tkn(WORDS_TOP), states=State.TEST_CALL)
@save_last_text
@default_buttons
def test_top(req, res, session):
    show_top_test(req, res, session, intro=True)
    session['state'] = State.CHOOSE_TOP


@handler.command(words=tkn(WORDS_RND), states=State.TEST_CALL)
@save_last_text
@default_buttons
def test_rnd(req, res, session):
    show_rnd_test(req, res, session, intro=True)
    session['state'] = State.CHOOSE_RND


@handler.command(words=tkn(WORDS_NEXT), states=State.CHOOSE)
@save_last_text
@default_buttons
def next_test(req, res, session):
    args = req, res, session, False
    {
        State.CHOOSE_NEW: show_new_test,
        State.CHOOSE_TOP: show_top_test,
        State.CHOOSE_RND: show_rnd_test,
        State.CHOOSE_FOUND: exit_found_test
    }[session['state']](*args)


@handler.command(words=tkn(WORDS_PASS), states=State.CHOOSE)
@save_last_text
@default_buttons
def enter_the_name(req, res, session):
    res.text = txt(TEXT_ENTER_THE_NAME)
    session['state'] = State.PASS_TEST


@handler.undefined_command(states=State.PASS_TEST)
@save_last_text
@default_buttons
def check_name(req, res, session):
    contains_name = False
    for e in req.entities:
        if e['type'] == 'YANDEX.FIO':
            session['name'] = ' '.join(e['value'][i].capitalize() for i in e['value'])
            contains_name = True
            break

    if contains_name or 'name' in session and any(x in req.tokens for x in tkn(WORDS_PASS)):
        start_test(req, res, session)
    else:
        res.text = txt(TEXT_NO_NAME)


@handler.command(words=tkn(WORDS_LIKE), states=State.PASS_TEST)
@save_last_text
@default_buttons
def like(req, res, session):
    test = session['test']
    if test.liked(req.user_id):
        res.text = txt(TEXT_ALREADY_LIKED)
    else:
        test.like(req.user_id)
        res.text = txt(TEXT_HAVE_LIKED)


@handler.command(words=tkn(WORDS_EXIT), states=State.CHOOSE + (State.PASS_TEST,))
@save_last_text
@default_buttons
def back(req, res, session):
    session['state'] = State.MENU
    res.text = txt(TEXT_BACK)


@handler.command(words=tkn(WORDS_HELP), states=State.ALL)
@save_last_text
@default_buttons
def help_(req, res, session):
    res.text = txt(TEXT_HELP[session['state']])


@handler.command(words=tkn(WORDS_ABILITY), states=State.ALL)
@save_last_text
@default_buttons
def ability_(req, res, session):
    res.text = txt(TEXT_ABILITY)


@handler.command(words=tkn(WORDS_EXIT), states=State.MENU)
def leave_skill(req, res, session):
    res.text = txt(TEXT_BYE)
    res.end_session = True
    session.clear()


@handler.command(words=tkn(WORDS_REPEAT), states=State.ALL)
@save_last_text
@default_buttons
def repeat(req, res, session):
    res.text = session['last_text']


@handler.undefined_command(states=State.ALL)
@save_last_text
@normalize_tts
@default_buttons
def ne_ponel(req, res, session):
    res.text = txt(TEXT_NE_PONEL)
    add_wtf(f'{session["state"]}: {req.text}')


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


def exit_found_test(req, res, session, intro=False):
    session['state'] = State.MENU
    res.text = txt(TEXT_BACK)


def show_test_base(res, session, test, intro=False, cycled=False):
    intro_text = '' if not intro else txt(TEXT_INTRO)
    if cycled:
        intro_text += txt(TEXT_RESTARTED)

    res.text = f'{intro_text}{test}'
    session['test'] = test


PAUSE = 'sil <[250]>'


def start_test(req, res, session):
    test = session['test']
    name = session['name']
    intrigue, result = test.intrigue, test.result
    res.text = f'{name}\n{test.name}\n{intrigue}\n{result}\n{txt(TEXT_END_TEST)}'
    res.tts = f'{name} {PAUSE}\n{test.name} {PAUSE}\n{intrigue}\n' \
              f'{snd(SOUNDS_INTRIGUE)}\n{result} {PAUSE}\n{txt(TEXT_END_TEST)}'
    if not test.liked(req.user_id):
        res.buttons = [button(BUTTON_LIKE)]


class MinitestSkill(BaseSkill):
    name = 'minitest_skill'
    command_handler = handler
