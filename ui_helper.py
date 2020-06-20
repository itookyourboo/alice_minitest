import os
from random import choice

from base_skill.skill import button, BigImageCard
from .strings import btn, BUTTONS


uni_images = (
    '1652229/d198ef1eb3711123dec9',
    '213044/45c4186ffe6e4082104e',
    '213044/d66b844d27d8fc3cd77d',
    '1652229/4153ac331be307dde553',
    '965417/932b2c855f611eca6a8b',
    '1652229/47c83d85431693b69cda'
)


def get_random_image():
    return choice(uni_images)


def get_card(title, description, image_id=None):
    card = BigImageCard()
    card.title = title
    card.description = description
    card.image_id = image_id if image_id else get_random_image()
    return card


def default_buttons(func):
    def wrapper(req, res, session):
        func(req, res, session)
        if len(res.buttons) == 0:
            res.buttons = [button(x) for x in btn(BUTTONS[session['state']])]
        else:
            for x in btn(BUTTONS[session['state']]):
                res.buttons.append(button(x))

    return wrapper


def save_res(func):
    def wrapper(req, res, session):
        func(req, res, session)
        session['last_card'] = None
        session['last_text'] = None
        session['last_tts'] = None

        if res.card:
            session['last_card'] = res.card.card
        session['last_text'] = res.text
        session['last_tts'] = res.tts

    return wrapper


def normalize_tts(func):
    def wrapper(req, res, session):
        func(req, res, session)
        res.tts = res.text.replace('тест', 'т+эст')
    return wrapper
