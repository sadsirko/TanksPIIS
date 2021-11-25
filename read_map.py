from const import BLOCKS,PATH_LEVEL,BIG_BLOCKS
import random

class Read_map:
    def __init__(self):
        self.map = []
        self.enemy = []        
    def create_map(self):
        for i in range(int(BIG_BLOCKS["w"])):
            self.map.append([])

    def read_map(self, lvl):
        self.create_map()
        f = open(PATH_LEVEL + lvl + ".txt","r")
        lines = f.readlines()
        i = 0
        for line in lines:
            for element in line:
                if (element != '\n') & (i < int(BIG_BLOCKS['w'])):
                    self.map[i].append( element)
                if i == BIG_BLOCKS['w']:
                    self.enemy.append(element)
            i = i + 1 
        
        
    def generate_map(self):
        self.create_map()
        counter_line = 0
        for j in self.map:
            for i in range(0,BIG_BLOCKS["w"]):
                if counter_line > 1 and counter_line < int(BIG_BLOCKS['h']) - 2:
                    block = random.randint(0,25)
                    if block > 15 and block < 19:
                        j.append('#')
                    elif block > 24:
                        j.append('@')
                    else:
                        j.append('.')
                else:
                    j.append('.')
            counter_line = counter_line + 1
        for i in self.map:
            print(i) 