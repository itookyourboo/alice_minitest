import logging

from base_skill.skill import CommandHandler, BaseSkill, button
from .strings import TEXT, WORDS, BUTTON_LIKE, BUTTON_NEXT_TEST, txt, HELP
from .state import State
from .test_helper import get_new_test, get_top_test, get_random_test, add_wtf, try_to_find_test
from .ui_helper import default_buttons, save_res, normalize_tts, get_card, get_image_id, get_random_sound


handler = CommandHandler()


@handler.hello_command
@save_res
@default_buttons
def hello(req, res, session):
    res.tts = f"{txt(TEXT['hello'])}\n{txt(TEXT['can_search'])}"
    res.text = txt(TEXT['hello'])
    session['state'] = State.MENU
    normalize_tts(res)


@handler.undefined_command(states=State.MENU)
@save_res
@default_buttons
def find_test(req, res, session):
    test = try_to_find_test(req.text)
    if test:
        res.text = txt(TEXT['found_1']).format(test.name, test.description)
        session['test'] = test
        session['state'] = State.CHOOSE_FOUND
    else:
        res.text = txt(TEXT['not_found'])
    normalize_tts(res)


@handler.command(words=WORDS['new'], states=State.TEST_CALL)
@save_res
@default_buttons
def test_new(req, res, session):
    show_new_test(req, res, session, intro=True)
    session['state'] = State.CHOOSE_NEW
    normalize_tts(res)


@handler.command(words=WORDS['top'], states=State.TEST_CALL)
@save_res
@default_buttons
def test_top(req, res, session):
    show_top_test(req, res, session, intro=True)
    session['state'] = State.CHOOSE_TOP
    normalize_tts(res)


@handler.command(words=WORDS['rnd'], states=State.TEST_CALL)
@save_res
@default_buttons
def test_rnd(req, res, session):
    show_rnd_test(req, res, session, intro=True)
    session['state'] = State.CHOOSE_RND
    normalize_tts(res)


@handler.command(words=WORDS['next'], states=State.CHOOSE + (State.PASS_TEST,))
@save_res
@default_buttons
def next_test(req, res, session):
    args = req, res, session, False
    {
        State.CHOOSE_NEW: show_new_test,
        State.CHOOSE_TOP: show_top_test,
        State.CHOOSE_RND: show_rnd_test,
        State.CHOOSE_FOUND: exit_found_test,
        State.PASS_TEST: show_rnd_test
    }[session['state']](*args)
    normalize_tts(res)


@handler.command(words=WORDS['pass'], states=State.CHOOSE)
@save_res
@default_buttons
def enter_the_name(req, res, session):
    res.text = txt(TEXT['enter_name'])
    session['state'] = State.PASS_TEST
    normalize_tts(res)


@handler.undefined_command(states=State.CHOOSE + (State.PASS_TEST,))
@save_res
@default_buttons
def check_name(req, res, session):
    contains_name = False
    for e in req.entities:
        if e['type'] == 'YANDEX.FIO':
            session['name'] = ' '.join(e['value'][i].capitalize() for i in e['value'])
            contains_name = True
            break

    if contains_name or 'name' in session and any(x in req.tokens for x in WORDS['pass']):
        start_test(req, res, session)
    else:
        res.text = txt(TEXT['no_name'])

    normalize_tts(res)


@handler.command(words=WORDS['like'], states=State.PASS_TEST)
@save_res
@default_buttons
def like(req, res, session):
    test = session['test']
    if test.liked(req.user_id):
        res.text = f"{txt(TEXT['already_liked'])}\n{txt(TEXT['end_test'])}"
    else:
        test.like(req.user_id)
        res.text = f"{txt(TEXT['thanks'])}\n{txt(TEXT['end_test'])}"

    res.buttons = [button(BUTTON_NEXT_TEST)]
    normalize_tts(res)


@handler.command(words=WORDS['exit'], states=State.CHOOSE + (State.PASS_TEST,))
@save_res
@default_buttons
def back(req, res, session):
    session['state'] = State.MENU
    res.text = txt(TEXT['back'])
    normalize_tts(res)


@handler.command(words=WORDS['help'], states=State.ALL)
@save_res
@default_buttons
def help_(req, res, session):
    res.text = HELP[session['state']]
    normalize_tts(res)


@handler.command(words=WORDS['ability'], states=State.ALL)
@save_res
@default_buttons
def ability_(req, res, session):
    res.text = txt(TEXT['ability'])
    normalize_tts(res)


@handler.command(words=WORDS['exit'], states=State.MENU)
def leave_skill(req, res, session):
    res.text = txt(TEXT['bye'])
    res.end_session = True
    session.clear()


@handler.command(words=WORDS['repeat'], states=State.ALL)
@save_res
@default_buttons
def repeat(req, res, session):
    res.text = session.get('last_text', txt(TEXT['ne_ponel']))
    res.tts = session.get('last_tts', res.text)
    res.card = session.get('last_card')
    normalize_tts(res)


@handler.undefined_command(states=State.ALL)
@save_res
@default_buttons
def ne_ponel(req, res, session):
    res.text = txt(TEXT['ne_ponel'])
    add_wtf(f'{session["state"]}: {req.text}')
    normalize_tts(res)


def show_new_test(req, res, session, intro=False):
    session['new_idx'] = session.get('new_idx', -1) + 1
    cycled, test = get_new_test(session['new_idx'])
    show_test_base(res, session, test, intro=intro, cycled=cycled)


def show_top_test(req, res, session, intro=False):
    session['top_idx'] = session.get('top_idx', -1) + 1
    cycled, test = get_top_test(session['top_idx'])
    show_test_base(res, session, test, intro=intro, cycled=cycled)


def show_rnd_test(req, res, session, intro=False):
    session['state'] = State.CHOOSE_RND
    test = get_random_test()
    show_test_base(res, session, test, intro=intro)


def exit_found_test(req, res, session, intro=False):
    session['state'] = State.MENU
    res.text = txt(TEXT['back'])


def show_test_base(res, session, test, intro=False, cycled=False):
    intro_text = '' if not intro else txt(TEXT['intro'])
    if cycled:
        intro_text += txt(TEXT['restarted'])

    res.tts = f'{test}{intro_text}'
    res.text = f'{test}'
    session['test'] = test


PAUSE = 'sil <[250]>'


def start_test(req, res, session):
    test = session['test']
    name = session['name']
    intrigue, result = test.intrigue, test.result
    res.tts = f'{name} {PAUSE}\n' \
              f'{test.name} {PAUSE}\n' \
              f'{intrigue}\n' \
              f'{get_random_sound()}\n' \
              f'{result} {PAUSE}\n' \
              f'{txt(TEXT["end_test"])}'
    res.text = f'{name}\n' \
               f'{test.name}\n' \
               f'{intrigue}\n' \
               f'{result}\n' \
               f'{txt(TEXT["end_test"])}'
    res.card = get_card(test.name, result,
                        image_id=get_image_id(test.id, test.results.index(result)))
    if not test.liked(req.user_id):
        res.buttons = [button(BUTTON_LIKE), button(BUTTON_NEXT_TEST)]
    else:
        res.buttons = [button(BUTTON_NEXT_TEST)]


class MinitestSkill(BaseSkill):
    name = 'minitest_skill'
    command_handler = handler

    def log(self, req, res, session):
        logging.info(f'USR: {req.user_id[:5]}\n'
                     f'REQ: {req.text}\n'
                     f'RES: {res.text}\n'
                     f'------------------')
