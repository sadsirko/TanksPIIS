from pygame.constants import TIMER_RESOLUTION
from const import BANNED_BLOCKS,BIG_BLOCKS,BLOCK_SIZE, COOLDOWN, ZOOM_16
import time
from bullet import Bullet

class Tank:
    def __init__(self,name,pos_x,pos_y,direction = 'up',hp = 4):
        self.pos = {"x" : pos_x,"y": pos_y }
        self.direction = direction  
        self.hp = hp
        self.name = name
        self.last_fire = time.time() - COOLDOWN - 1 

    def set_tank(self,map):
        x = self.pos['x']
        y = self.pos['y']
        # print(x,y)
        map[y+1][x] = "-"
        map[y+1][x+1] = "-"
        map[y][x+1] = "-"
        map[y][x] = "+"
        return map

    def unset_tank(self,map):
        x = self.pos['x']
        y = self.pos['y']
        map[y+1][x] = "."
        map[y+1][x+1] = "."
        map[y][x+1] = "."
        map[y][x] = "."
        return map

    def move_up(self,map):
        self.direction = "up"
        x = self.pos['x']
        y = self.pos['y']
        if y - 1 >= 0:
            a = map[y-1][x+1]
            b = map[y-1][x]
            if not(a in BANNED_BLOCKS or b in BANNED_BLOCKS):
                self.pos["y"] = y - 1
                map[y - 1][x] = '+'
                map[y - 1][x + 1] = '-'
                map[y][x] = '-'
                map[y + 1][x + 1] = '.'
                map[y + 1][x] = '.'

        return map

    def move_down(self,map):
        self.direction = "down"
        x = self.pos['x']
        y = self.pos['y']
        if y + 2 < BIG_BLOCKS['h']:
            a = map[y+2][x+1]
            b = map[y+2][x]
            if not(a in BANNED_BLOCKS or b in BANNED_BLOCKS):
                self.pos["y"] = y + 1
                map[y + 1][x] = '+'
                map[y + 2][x + 1] = '-'
                map[y + 2][x] = '-'
                map[y][x] = '.'
                map[y][x + 1] = '.'
                # for i in map:
                #     print(i)
        return map

    def move_right(self,map):
        self.direction = "right"
        x = self.pos['x']
        y = self.pos['y']
        if x + 2 < BIG_BLOCKS['w']:
            a = map[y][x + 2]
            b = map[y + 1][x + 2]
            if not(a in BANNED_BLOCKS or b in BANNED_BLOCKS):
                self.pos["x"] = x + 1
                map[y][x + 1] = '+'
                map[y][x + 2] = '-'
                map[y + 1][x + 2] = '-'
                map[y][x] = '.'
                map[y + 1][x] = '.'
                # for i in map:
                    # print(i)        
        return map
         
    def move_left(self,map):
        self.direction = "left"
        x = self.pos['x']
        y = self.pos['y']
        if x - 1  >= 0:
            a = map[y][x - 1]
            b = map[y + 1][x - 1]
            if not(a in BANNED_BLOCKS or b in BANNED_BLOCKS):
                self.pos["x"] = x - 1
                map[y][x - 1] = '+'
                map[y + 1][x - 1] = '-'
                map[y][x] = '-'
                map[y + 1][x + 1] = '.'
                map[y][x + 1] = '.'
                # for i in map:
                    # print(i)        
        return map

    def fire(self,bul_arr):
        if time.time() < self.last_fire + COOLDOWN:
            return False
        x_cord = self.pos['x'] * BLOCK_SIZE
        y_cord = self.pos['y'] * BLOCK_SIZE
        if self.direction == "up":
            pos_x = x_cord + BLOCK_SIZE / 2 - 2
            pos_y = y_cord - BLOCK_SIZE / 8
        if self.direction == "down":
            pos_x = x_cord + BLOCK_SIZE / 2
            pos_y = y_cord + BLOCK_SIZE
        if self.direction == "left":
            pos_x = x_cord - BLOCK_SIZE / 8
            pos_y = y_cord + BLOCK_SIZE / 2
        if self.direction == "right":
            pos_x = x_cord + BLOCK_SIZE
            pos_y = y_cord + BLOCK_SIZE / 2
        self.last_fire = time.time()
        info = {'pos_x':pos_x,'pos_y':pos_y, 
        "direction":self.direction}
        bul = Bullet(info['pos_x'],info['pos_y'],info["direction"])
        bul_arr.append(bul)
        return bul_arr

    