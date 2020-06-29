import os
from random import choice

from base_skill.skill import button, BigImageCard
from .strings import btn, BUTTONS

uni_images = (
    '1540737/419a8f88c59d0e72fa41',
    '1540737/d7aa47c0cf2ba485cf53',
    '213044/d66b844d27d8fc3cd77d',
    '1652229/d198ef1eb3711123dec9',
    '1652229/4153ac331be307dde553',
    '213044/45c4186ffe6e4082104e'
)

SOUNDS = {
    'harp': '<speaker audio="alice-music-harp-1.opus">',
    'drum_1': '<speaker audio="alice-music-drums-1.opus">',
    'drum_2': '<speaker audio="alice-music-drums-2.opus">',
    'gong': '<speaker audio="alice-music-gong-1.opus">',
    'drum_loop_1': '<speaker audio="alice-music-drum-loop-1.opus">'
}
sounds = list(SOUNDS.values())


def get_random_image():
    return choice(uni_images)


def get_random_sound():
    return choice(sounds)


def get_card(title, description, image_id=None):
    card = BigImageCard()
    card.title = title
    card.description = description
    card.image_id = image_id if image_id else get_random_image()
    return card


def get_image_id(test_id, result_index):
    return IMAGES.get((test_id, result_index + 1), get_random_image())


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


def normalize_tts(res):
    res.tts = res.tts\
        .replace('тест', 'т+эст')\
        .replace('Тест', 'Т+эст')\
        .replace('Гааааааляяяяяяяяя', 'Га а а аля')


IMAGES = {(0, 1): '1540737/d027c1e7161bb26c044c', (0, 2): '1652229/29b84e9d0f4f2705d2d1',
          (0, 3): '965417/6c722d64e402a8b85a77', (0, 4): '1030494/1c46a741d08e68eccbf7',
          (0, 5): '213044/4f8f18c03639f4a76346', (0, 6): '1540737/3509d3e72ff024a5e8ee',
          (0, 7): '1540737/57df05543e813bee2bdf', (0, 8): '1030494/196a9ddd883c402827d8',
          (10, 1): '1652229/37ec12be4e8c316eb7b1', (10, 2): '1652229/d266d096cc5ce017cb5d',
          (10, 3): '1533899/e28278add85b5887e5de', (10, 4): '1540737/059f95dbfc9cb303beb6',
          (11, 1): '1540737/7ac664f7d2c520e7d80d', (11, 2): '1652229/5de6091560ddebf102a6',
          (11, 3): '1652229/83e8e07cbc3368d473a1', (11, 4): '1652229/9604d36f2eec88e4dbf6',
          (12, 1): '1030494/8f524a9541ae80daaea0', (12, 2): '1030494/b8d586ffebb535c133a5',
          (12, 3): '1540737/d3fc95ee2e7e4a1af080', (12, 4): '937455/acbd69e4cd40f858bb3d',
          (13, 1): '1540737/6aaf049fae2987241d58', (13, 2): '937455/c6d1ee10b16ba623fd05',
          (13, 3): '1030494/fab864e8d3d0e02b338a', (13, 4): '1030494/7b24e7c59361500887ea',
          (14, 1): '937455/5a3aa529aa109ad1b3c9', (14, 2): '1540737/c989edc8480b9151a8f5',
          (14, 3): '1652229/d9e9b28204b042669eb0', (14, 4): '965417/b74367c0589408d69b22',
          (15, 1): '937455/e7deaea279af547085a4', (15, 2): '1652229/e6098af2e5ec818ed33f',
          (15, 3): '213044/c91970d5455c4cef283e', (15, 4): '965417/7b752a92ee70466c9cb2',
          (16, 1): '937455/8a34ea14ebab2fce0ef5', (16, 3): '1540737/b5475f70fc734ac965e9',
          (16, 4): '1652229/e382d461540f627f34a4', (17, 1): '1533899/dc240ee1c6a2a629bbfe',
          (17, 2): '1656841/1f28a4169ab92b3a2373', (17, 3): '937455/5cb09fd527371cb9cf2a',
          (17, 4): '937455/30c30a6a699b36f08744', (18, 1): '1533899/c74a6dd9eca351b2d58d',
          (18, 2): '1652229/1cc977b831146a4261ef', (18, 3): '1652229/d30c730b8d785773faaf',
          (18, 4): '937455/aeddded162ee3185b8d9', (19, 1): '937455/8651ca838f7bfec049ad',
          (19, 2): '965417/1de37d0c5c74dabc74e8', (19, 3): '213044/a8d3c92cb6de3c0856db',
          (19, 4): '1030494/8717b91cd3eb33d292d6', (1, 1): '1030494/c6659fa92b21c31968d3',
          (1, 2): '1030494/ac620dc6f1609065a108', (1, 3): '937455/8e5c26d83b9068239dfc',
          (1, 4): '1030494/b6f68eb1c86470d9c76b', (1, 5): '937455/58c021649423bfdf98fe',
          (1, 6): '213044/4221119dedcfa0903267', (1, 7): '1652229/9f4c5c80470b95862b9a',
          (1, 8): '937455/0534dcefb9303da5c210', (20, 1): '937455/29bd13684179c03ba718',
          (20, 2): '213044/19f6899e5bce5e72beb0', (20, 3): '937455/6755ba1f6f5620d2ef30',
          (20, 4): '1540737/8ab2c3bc4e615df58459', (20, 5): '213044/842ec3de82f6d911bac9',
          (20, 6): '937455/166afd997eb84b7767d7', ('21', '1'): '965417/48ccca1a9fb84ccdc06f',
          (21, 1): '965417/48ccca1a9fb84ccdc06f', (21, 2): '965417/92f4d414217b4cab9168',
          (21, 3): '965417/96281a065afd831ee459', (21, 4): '1540737/634010bc4f7b12523b05',
          (21, 5): '1652229/02c88c361234c223ba18', (22, 1): '1030494/f99f17f38c1f034c533f',
          (22, 2): '1030494/dc96daca034a093a4f4a', (22, 3): '1030494/34c4b22276d2a39be665',
          (22, 4): '1030494/180947f6f003805317e6', (23, 1): '1652229/bd76f4ef33582c0b7acd',
          (23, 2): '1540737/85b7897ab044a0c1847e', (23, 3): '1652229/7903800328d8e8d93d0a',
          (23, 4): '213044/ccb0d185281565c70147', (24, 1): '213044/a08be33c2882c66640ce',
          (24, 2): '213044/1282cea811f80b41c193', (24, 3): '1540737/4970f781f3841a28525b',
          (24, 4): '213044/c74bb55b120f41177a1e', (24, 5): '1030494/abd9305f94121d607400',
          (25, 1): '1030494/6a9441a4a5e41f8b30a2', (25, 2): '1030494/b3c5c51f423840a11179',
          (25, 3): '1540737/7a990471940872c0bda2', (25, 4): '1540737/fa4f50b03c4b1afccede',
          (25, 5): '1540737/f8035a85ed565b71fd2a', (2, 1): '937455/2e89bcea8f80f5264cfe',
          (2, 2): '937455/da5eef242fc5ba711b75', (2, 3): '1030494/484abdf85f61aa9a5ac2',
          (2, 4): '1030494/599b1b024d54b415fc52', (2, 5): '1030494/d042abe5e2429fc8ba8f',
          (2, 6): '1652229/5393dcb164f34860a116', (3, 1): '1652229/2590561977a2b783dcf2',
          (3, 2): '937455/cadb89b178406c4c9c4a', (3, 3): '1652229/074cda02c243b7a95ad3',
          (3, 4): '1652229/cdf7973545943bf2c9fd', (4, 1): '1540737/829e837a97201215f0d0',
          (4, 2): '1030494/5adf1ce614657e62829e', (4, 3): '965417/d0a1435f493f4a4e4121',
          (4, 4): '1652229/efd66484f2f23c601791', (5, 1): '1540737/1d3a906f4a93c10edfc6',
          (5, 2): '1030494/e434c0d0a4b2ca3afb46', (5, 3): '937455/098d6833517fa5564fa2',
          (5, 4): '965417/06f97283b4d08e913fc2', (6, 1): '937455/939f240365804311a4d5',
          (6, 2): '1533899/0362f02383a5eb7dfc9b', (6, 3): '213044/05354738fcc523107e79',
          (6, 4): '937455/c7b40a4921c0b0ab78ad', (7, 1): '1652229/b10b7973e4e838f4619d',
          (7, 2): '965417/24a293042dd3e4f5b029', (7, 3): '937455/4840a204e6a1ce71e751',
          (7, 4): '1652229/d71e664b4f94e8df621d', (8, 1): '1540737/29dc8a54bd8590b74a9a',
          (8, 2): '1652229/2278f5c019eef032af94', (8, 3): '1540737/4b1ef9913511bc800cc9',
          (8, 4): '1652229/17c9c1fb72c879c5b3b4', (9, 1): '1540737/2276fe7e13f58b206a14',
          (9, 2): '965417/efee881a0df5645923e2', (9, 3): '1540737/bdeaf11c33a2f057d047',
          (9, 4): '1652229/f0bc3530a63e4013a51d'}
