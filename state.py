from enum import Enum


class State(Enum):
    MENU = 0
    CHOOSE_TOP = 1
    CHOOSE_NEW = 2
    CHOOSE_RND = 3
    PASS_TEST = 4


State.ALL = tuple(State)
State.CHOOSE = State.CHOOSE_TOP, State.CHOOSE_RND, State.CHOOSE_NEW
State.TEST_CALL = State.MENU, State.CHOOSE_TOP, State.CHOOSE_RND, State.CHOOSE_NEW
