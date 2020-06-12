from base_skill.skill import *
from .strings import *
from .state import State


handler = CommandHandler()


@handler.hello_command
def hello(req, res, session):
    res.text = txt(TEXT_HELLO)
    session['state'] = State.MENU


@handler.undefined_command(states=State.ALL)
def ne_ponel(req, res, session):
    res.text = txt(TEXT_NE_PONEL)


class MinitestSkill(BaseSkill):
    name = 'minitest_skill'
    command_handler = handler
