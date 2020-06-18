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
