
import pygame as pg
from const import BLOCK_SIZE, SCREEN_SIZE, Color, FPS
from drawer import Drawer
from read_map import Read_map
from tank import Tank
import sys
from bot import Bot
from graph import Graph_creator


class GameController:
    def __init__(self):
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()
        self.screen.fill(Color.BLACK)
        self.drw = Drawer(self.screen)
        self.player = {"dir": "up"}
        self.map = Read_map()
        self.lvl = 1
        self.tank_arr={}
        self.bull_arr={}
        self.bull_gr = pg.sprite.Group()
        self.tank_gr = pg.sprite.Group()
        self.algorithm = "bfs"
        self.tank_stack_en = [Tank('A',0,0),Tank('C',10,0),Tank('D',14,0)]
        self.tank_stack = [Tank('P1',9,24,'up'),Tank('P1',9,24,'up')]
    def set_tanks(self,arr_pl,arr_bot,map):
        for pl in arr_pl:
            map = pl.set_tank(map)
            self.tank_gr.add()
        for bot in arr_bot:
            map = bot.set_tank(map)
        return map   

    def set_all_bullets(self):
        for i in self.bull_arr['player_fire']:
            #num of blocks damaged
            damaged_blocks = i.check_excplosion(self.map.map)
            if len(damaged_blocks) >= 1:
                for block in damaged_blocks:
                    self.destruction(block)
                self.bull_arr['player_fire'].remove(i)
            else:
                i.move()
                self.drw.draw_bullet(i)
    
        for i in self.bull_arr['enemy_fire']:
            #num of blocks damaged
            damaged_blocks = i.check_excplosion(self.map.map)
            if len(damaged_blocks) >= 1:
                for block in damaged_blocks:
                    self.destruction_bot(block)
                self.bull_arr['enemy_fire'].remove(i)
            else:
                i.move()
                self.drw.draw_bullet(i)        

    def destruction(self,pos):
        x = int(pos['x'] // BLOCK_SIZE)
        y = int(pos['y']// BLOCK_SIZE)
        cell = self.map.map[y][x]
        if  cell == "#":
            self.map.map[y][x] = '.'

        if cell == "+" or cell == "-":
            tank_en = self.check_what_enemy_tank({"x":x,"y":y}) 
            if tank_en != False:
                tank_en.unset_tank(self.map.map)
                self.tank_arr["enemy_arr"].remove(tank_en) 
    
    def destruction_bot(self,pos):
        x = int(pos['x'] // BLOCK_SIZE)
        y = int(pos['y']// BLOCK_SIZE)
        cell = self.map.map[y][x]
        if  cell == "#":
            self.map.map[y][x] = '.'

        if cell == "+" or cell == "-":
            tank_en = self.check_what_player_tank({"x":x,"y":y}) 
            if tank_en != False:
                tank_en.unset_tank(self.map.map)
                self.tank_arr["player_1"].remove(tank_en) 
    
    def compare_pos(self,pos1,pos2):
        if pos1['x'] == pos2['x'] and pos1['y'] == pos2['y']:
            return True
        return False
        #find what tank is here 

    def check_what_enemy_tank(self,pos):
        for tank in self.tank_arr['enemy_arr']:
            l_d = {"x" : tank.pos['x'],"y": tank.pos['y'] + 1 }
            r_d = {"x" : tank.pos['x'] + 1,"y": tank.pos['y'] + 1 }
            r_u = {"x" : tank.pos['x'] + 1,"y": tank.pos['y']}
            l_u = tank.pos
            l_d_b = self.compare_pos(pos,l_d)
            r_d_b = self.compare_pos(pos,r_d)
            l_u_b = self.compare_pos(pos,l_u)
            r_u_b = self.compare_pos(pos,r_u)
            if l_d_b or r_d_b or l_u_b or r_u_b:
                return tank
        return False
   
    def check_what_player_tank(self,pos):
        for tank in self.tank_arr['player_1']:
            l_d = {"x" : tank.pos['x'],"y": tank.pos['y'] + 1 }
            r_d = {"x" : tank.pos['x'] + 1,"y": tank.pos['y'] + 1 }
            r_u = {"x" : tank.pos['x'] + 1,"y": tank.pos['y']}
            l_u = tank.pos
            l_d_b = self.compare_pos(pos,l_d)
            r_d_b = self.compare_pos(pos,r_d)
            l_u_b = self.compare_pos(pos,l_u)
            r_u_b = self.compare_pos(pos,r_u)
            if l_d_b or r_d_b or l_u_b or r_u_b:
                return tank
        return False
            
    def change_alg(self):
        if self.algorithm == "bfs":
            self.algorithm = "dfs"
        else:
            self.algorithm = "bfs"

    def run_alg(self,graph):
        # print(self.algorithm)
        if self.algorithm == "dfs":
            # print(graph.DFS_algorithm())
            self.drw.draw_all_ways(graph.DFS_algorithm(),'dfs')
        else:
            # print(graph.BFS_algorithm())
            self.drw.draw_all_ways(graph.BFS_algorithm(),'bfs')

    def refil_tanks(self):
        if len(self.tank_arr['enemy_arr']) <3 and len(self.tank_stack_en)>0:
            self.tank_arr['enemy_arr'].append(self.tank_stack_en.pop())

        if len(self.tank_arr['player_1']) <1 and len(self.tank_stack)>0:
            self.tank_arr['player_1'].append(self.tank_stack.pop())


    def game_loop(self):

        # self.map.read_map(str(self.lvl))
        self.map.generate_map()
        
        self.tank_arr={
            'player_1': [Tank('P1',9,24,'up')],
            'enemy_arr':[Tank('A',5,0),Tank('C',12,0),Tank('D',16,0)]
            }
        self.bull_arr={'enemy_fire':[],'player_fire':[]}
        #set on map    
        self.map.map = self.set_tanks(self.tank_arr["player_1"],self.tank_arr["enemy_arr"],self.map.map)    
        
        bot_tanks = Bot(self.tank_arr["enemy_arr"])
        while True:
            self.refil_tanks()
            graph = Graph_creator(self.map.map, self.tank_arr['player_1'][0].pos,self.tank_arr["enemy_arr"])
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.drw.draw_back()
            if self.algorithm == "dfs":
                self.drw.draw_all_ways(graph.DFS_algorithm(),'dfs')
            else:
                self.drw.draw_all_ways(graph.BFS_algorithm(),'bfs')

            self.bull_arr["enemy_fire"] = bot_tanks.random_move(self.map.map, self.bull_arr["enemy_fire"])
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.map.map = self.tank_arr["player_1"][0].move_left(self.map.map)
                elif event.key == pg.K_RIGHT:
                    self.map.map = self.tank_arr["player_1"][0].move_right(self.map.map)
                elif event.key == pg.K_UP:
                    self.map.map = self.tank_arr["player_1"][0].move_up(self.map.map)
                elif event.key == pg.K_DOWN:
                    self.map.map = self.tank_arr["player_1"][0].move_down(self.map.map)
                if event.key == pg.K_RSHIFT:
                    self.change_alg()
                elif event.key == pg.K_LSHIFT:
                    res = self.tank_arr["player_1"][0].fire(self.bull_arr["player_fire"])              
                    if res != False:
                        self.bull_arr["player_fire"] = res  


            self.drw.draw_map(self.map.map)
            self.drw.draw_all_tanks(self.tank_arr['player_1'])
            self.drw.draw_all_tanks(self.tank_arr['enemy_arr'])
            self.set_all_bullets()
            pg.display.update()
            self.clock.tick(FPS)
       
if __name__ == '__main__':
    game = GameController()
    game.game_loop()