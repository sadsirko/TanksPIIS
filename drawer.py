# from bullet import Bullet
from os import setpriority
import pygame as pg
from const import BIG_BLOCKS, Color, PATH_SPRITE , BLOCK_SIZE,ZOOM_32,ZOOM_16
from const import ELEMENT_POS  

class Drawer:
    def __init__(self, screen):
        self.screen = screen  
        self.sprite = pg.image.load(PATH_SPRITE)

    def set_direction(self,img,dir = 'up'):
        if dir == "up":
            return img
        if dir == "right":
            return pg.transform.rotate(img,270)
        if dir == "down":
            return pg.transform.rotate(img,180)
        if dir == "left":
            return pg.transform.rotate(img,90)

    def get_from_sprite(self,coord,zoom,direction = "up"):
        obj = self.sprite.subsurface(coord['x1'], coord['y1'], coord['x'], coord['y'])
        big_obj = pg.transform.scale(obj,(zoom["x"],zoom["y"]))  
        directed_obj = self.set_direction(big_obj,direction)
        return directed_obj

    def draw_bullet(self,bul):
        bullett = self.get_from_sprite(ELEMENT_POS["BULLET"],ZOOM_16,bul.direction)
        self.screen.blit(bullett,(bul.pos['x'] ,bul.pos['y'] ))

    def draw_way_rect(self,pos,color,alg):
        cl = (0,0,0)
        if alg == "dfs":
            cl = (235, 107 + color * 50, 58)
        if alg == "bfs":
            cl = (35, 104 + color * 50, 69 )
        if alg == 'ucs':
            cl = (178, 104 + color * 50, 178 )
        pg.draw.rect(self.screen,  cl, 
                 (pos['x'] * BLOCK_SIZE, pos['y'] * BLOCK_SIZE, BLOCK_SIZE * 2, BLOCK_SIZE * 2))

    def draw_full_way(self,way,color,alg):
        for i in way:
            self.draw_way_rect(i,color,alg)
    
    def draw_all_ways(self,arr_ways,alg):
        color_tone = 0
        for i in arr_ways:
            self.draw_full_way(i,color_tone,alg)
            color_tone = color_tone + 1

    def draw_wall(self,pos):
        sprite_pos={'x1' : 48,'x' : 8,'y1':64,'y':8}
        zoom = {'x':16,'y':16}
        my_obj = self.get_from_sprite(sprite_pos,zoom)
        self.screen.blit(my_obj,(pos['x'],pos['y']))

    def draw_strong_wall(self,pos):
        sprite_pos={'x1' : 48,'x' : 8,'y1':72,'y':8}
        zoom = {'x':16,'y':16}
        my_obj = self.get_from_sprite(sprite_pos,zoom)
        self.screen.blit(my_obj,(pos['x'],pos['y']))
        
    def draw_right_obj(self,obj,pos):
        if obj == "#":
            self.draw_wall(pos)
        if obj == "@":
            self.draw_strong_wall(pos)

    def draw_all_tanks(self,arr):
        for tank in arr:
            my_tank = self.get_from_sprite(ELEMENT_POS[tank.name],ZOOM_32,tank.direction)
            my_tank_rect = my_tank.get_rect()
            my_tank_rect.center = (tank.pos['x'] * BLOCK_SIZE + ZOOM_16['x'],tank.pos['y'] * BLOCK_SIZE + ZOOM_16['y'])
            self.screen.blit(my_tank,my_tank_rect)
#change tank dir via not drawing at all mb

    def draw_map(self,map):
        pos = {"x":0,"y":0}
        count_y = 0
        for line in map:
            count_x = 0
            for el in line:
                pos = {"x":count_x * BLOCK_SIZE,"y": count_y * BLOCK_SIZE}
                self.draw_right_obj(el,pos)
                count_x = count_x + 1
            count_y = count_y + 1
            
    def draw_back(self):
        self.screen.fill((0, 0, 0))



