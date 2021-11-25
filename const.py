BANNED_BLOCKS=["+","@","#",'-']
SCREEN_SIZE = (416, 416)
FPS = 10
PATH_SPRITE = "sprites/sprites.png"
PATH_LEVEL="lvl/"
BLOCKS ={"h":56,"w":52}
BIG_BLOCKS = {"h":26,"w":26}
BLOCK_SIZE = 16
ZOOM_32 = {'x':32,'y':32}
ZOOM_16 = {'x':16,'y':16}
BULLET_SPEED = 8    
COOLDOWN = 0.5

ELEMENT_POS = {
    'P1':{'x1' : 0,'x' : 13,'y1':0,'y':13},
    'P':{'x1' : 32,'x' : 16,'y1':0,'y':16},
    'A':{'x1' : 48,'x' : 16,'y1':0,'y':16},
    'C':{'x1' : 64,'x' : 16,'y1':0,'y':16},
    'D':{'x1' : 80,'x' : 16,'y1':0,'y':16},
    'BASE':{'x1' : 32,'x' : 16,'y1':16,'y':16},
    'BULLET':{'x1' : 72,'x' : 8,'y1':72,'y':8}
}

class Color:
    BLACK = (4, 4, 4)
    YELLOW_BLACK = (250, 240, 190)
    LIGHT_BLACK = (70, 70, 70)
    LIGHTER_BLACK = (30, 30, 30)
    WHITE = (245, 245, 245)
    A_BIT_YELLOW_WHITE = (233, 233, 233)
    WHITE_WITH_RED = (245, 180, 180)
    LIGHT_RED = (250, 97, 87)
    GREEN = (35, 124, 69)
