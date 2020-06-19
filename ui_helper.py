import os

from base_skill.skill import button
from .strings import btn, BUTTONS


def default_buttons(func):
    def wrapper(req, res, session):
        func(req, res, session)
        if len(res.buttons) == 0:
            res.buttons = [button(x) for x in btn(BUTTONS[session['state']])]
        else:
            for x in btn(BUTTONS[session['state']]):
                res.buttons.append(button(x))

    return wrapper


def save_last_text(func):
    def wrapper(req, res, session):
        func(req, res, session)
        session['last_text'] = res.text

    return wrapper


def normalize_tts(func):
    def wrapper(req, res, session):
        func(req, res, session)
        res.tts = res.text.replace('тест', 'т+эст')
    return wrapper
