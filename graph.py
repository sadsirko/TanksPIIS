
from sys import path
from const import BANNED_BLOCKS,BIG_BLOCKS, PATH_LEVEL

class Graph_creator:
    def __init__(self,map,player,enemy):
        self.graph = []
        self.map = map
        self.checked = []
        self.start = player
        self.queue = []
        #start point also in path
        self.path = []
        self.len = []
        self.aims = [player]
        self.enemy = enemy
        self.build_way = []
        self.result = []

    def compare_to_pos(self,pos_1,pos_2):
        if pos_1['x'] == pos_2['x'] and pos_1['y'] == pos_2['y']:
            return True
        return False

    def is_already_in(self,element,arr):
        for i in arr:
            if self.compare_to_pos(i,element):
                return True
        return False

    def is_tank_near(self,pos):
        #check up
        if pos['y'] > 1 and  pos['x'] < BIG_BLOCKS['w'] - 1 :
            if self.map[pos['y'] - 1][pos['x'] + 1] == "+": 
                return {"y":pos['y'] - 1,"x": pos['x'] + 1}
            if self.map[pos['y'] -1 ][pos['x']] == "+":
                return {"y":pos['y'] - 1,"x": pos['x']}

        #check right
        if pos['x'] < BIG_BLOCKS['w'] - 2 and pos['y'] < BIG_BLOCKS['h'] - 2:
            if self.map[pos['y']][pos['x'] + 2] == "+": 
                return { "y":pos['y'],"x": pos['x'] + 2}
            if self.map[pos['y'] + 1][pos['x'] + 2] == "+":
                return { "y":pos['y'] + 1,"x": pos['x'] + 2}

        #check down
        if pos['y'] < BIG_BLOCKS['h'] - 3 and pos['x'] < BIG_BLOCKS['w'] - 2:
            if self.map[pos['y'] + 2][pos['x']] == '+':
                return { "y":pos['y'] + 2, "x": pos['x']}
            if self.map[pos['y'] + 2][pos['x'] + 1] == '+':
                return {"y":pos['y'] + 2, "x": pos['x'] + 1}

        #check left
        if pos['x'] > 1 and pos['y'] < BIG_BLOCKS['h'] - 1:
            if self.map[pos['y']][pos['x'] - 2] == '+':
                return { "y":pos['y'],"x": pos['x'] - 2} 
            if self.map[pos['y'] + 1][pos['x'] - 2] == '+':
                return {"y":pos['y'] + 1,"x": pos['x'] - 2}
        return False

    def from_pos_to_num(self, pos):
        return pos['y'] * BIG_BLOCKS['h'] + pos['x']

    def from_num_to_pos(self,num):
        return {'y': num // BIG_BLOCKS['h'], 'x' : num % BIG_BLOCKS['h']}

    def is_already_checked(self,pos):
        if len(self.path[pos['y']][pos['x']]) > 0:
            return True
        return False

    def is_already_checked_ucf(self,pos):
        for i in self.checked:
            if self.compare_to_pos(pos,i):
                return True
        return False

    def initial_pathes(self):
        for i in range(0, BIG_BLOCKS['w']):
            self.path.append([])
            self.len.append([])
            for j in range(0, BIG_BLOCKS['h']):
                self.path[i].append([])
                self.len[i].append([])

    def check_move_up(self,pos):
        x = pos['x']
        y = pos['y']
        if y - 1 >= 0:
            a = self.map[y-1][x+1]
            b = self.map[y-1][x]
            if not(a in BANNED_BLOCKS or b in BANNED_BLOCKS):
                return {'x': x, "y" : y - 1}
        return False

    def check_move_down(self,pos):
        x = pos['x']
        y = pos['y']
        if y + 2 < BIG_BLOCKS['h']:
            a = self.map[y+2][x+1]
            b = self.map[y+2][x]
            if not(a in BANNED_BLOCKS or b in BANNED_BLOCKS):
                return {'x': x, "y" : y + 1}
        return False

    def check_move_right(self,pos):
        x = pos['x']
        y = pos['y']
        if x + 2 < BIG_BLOCKS['w']:
            a = self.map[y][x + 2]
            b = self.map[y + 1][x + 2]
            if not(a in BANNED_BLOCKS or b in BANNED_BLOCKS):
                return {'x': x + 1, "y" : y}
        return False

    def check_move_left(self,pos):
        x = pos['x']
        y = pos['y']
        if x - 1  >= 0:
            # print(y,x)
            a = self.map[y][x - 1]
            b = self.map[y + 1][x - 1]
            if not(a in BANNED_BLOCKS or b in BANNED_BLOCKS):
                return {'x': x - 1, "y" : y}
        return False

    def check_move(self,check,cur):
        if check is not False:
            if not self.is_already_checked(check):
                # print(self.path[check['y']][check['x']])
                self.queue.append(check) 
                self.path[check['y']][check['x']].append(self.queue[0])
                self.path[check['y']][check['x']] = self.path[check['y']][check['x']] + self.path[cur['y']][cur['x']]
                
                tank = self.is_tank_near({'x': check['x'],'y':check['y']})
                if tank is not False:
                    if not self.is_already_in(tank,self.aims):
                        self.aims.append(tank)
                        self.build_way.append(check)

    def check_move_dfs(self,check,cur):
        # if not self.is_already_checked(check):
            # print(self.path[check['y']][check['x']])
            self.queue.append(check) 
            self.path[check['y']][check['x']].append(self.queue[len(self.queue) - 1])
            self.path[check['y']][check['x']] = self.path[check['y']][check['x']] + self.path[cur['y']][cur['x']]
            
            tank = self.is_tank_near({'x': check['x'],'y':check['y']})
            if tank is not False:
                #check if it was alredy checked
                if not self.is_already_in(tank,self.aims):
                    self.aims.append(tank)
                    self.build_way.append(check)

    def check_move_ucs(self,check,cur):
        #if move is acceseble
        if check is not False:
            if not self.is_already_checked_ucf(check):
                # print(self.path[check['y']][check['x']])
                self.queue.append(check) 
                if len(self.path[check['y']][check['x']]) - 1 > len(self.path[cur['y']][cur['x']]):
                    self.path[check['y']][check['x']] = []
                    self.path[check['y']][check['x']].append(self.queue[0])
                    self.path[check['y']][check['x']] = self.path[check['y']][check['x']] + self.path[cur['y']][cur['x']]
                
                    tank = self.is_tank_near({'x': check['x'],'y':check['y']})
                    if tank is not False:
                        if not self.is_already_in(tank,self.aims):
                            self.aims.append(tank)
                            self.build_way.append(check)
    

    def BFS_algorithm(self):
        self.result = []
        self.build_way = []
        self.checked = []
        self.path = []
        self.len = []
        self.build_way = []
        self.result = []
        self.initial_pathes()

        #set start position
        self.queue.append(self.start)
        while(len(self.queue) > 0):
            cur = self.queue[0] 
            # print(self.queue,"queue")
            check = self.check_move_left(cur)
            self.check_move(check, cur)

            check = self.check_move_up(cur)
            self.check_move(check, cur)
                    
            check = self.check_move_right(cur)
            self.check_move(check, cur)

            check = self.check_move_down(cur)
            self.check_move(check, cur)

            self.queue.remove(self.queue[0])
        countx = 0
        county = 0
        for i in self.path:
            for j in i:
                self.len[county][countx] = len(j)
                countx = countx + 1
            countx = 0
            county = county + 1
        for i in self.build_way:
            self.result.append(self.path[i['y']][i['x']])
        return self.result

    def DFS_algorithm(self):
        self.result = []
        self.build_way = []
        self.checked = []
        self.path = []
        self.len = []
        self.build_way = []
        self.result = []
        self.initial_pathes()
        self.queue.append(self.start)
        while(len(self.queue) > 0):
            # print(self.queue)
            cur = self.queue[len(self.queue) - 1] 
            check_up = self.check_move_up(cur)
            if check_up is not False and not self.is_already_checked(check_up):
                    self.check_move_dfs(check_up, cur)
            else:    
                check_left = self.check_move_left(cur)
                if check_left is not False and not self.is_already_checked(check_left):
                        self.check_move_dfs(check_left, cur)
                else:            
                    check_right = self.check_move_right(cur)
                    if check_right is not False and not self.is_already_checked(check_right):
                            self.check_move_dfs(check_right, cur)
                    else:
                        check_down = self.check_move_down(cur)
                        if check_down is not False and not self.is_already_checked(check_down):
                                self.check_move_dfs(check_down, cur)
                        else:
                            self.queue.pop()
        countx = 0
        county = 0
        for i in self.path:
            for j in i:
                self.len[county][countx] = len(j)
                countx = countx + 1
            countx = 0
            county = county + 1
        # for k in self.len:
        #     print(k)
        # print(self.build_way)

        for i in self.build_way:
            self.result.append(self.path[i['y']][i['x']])
        # print(self.result)
        
        return self.result

    def UCS_algorithm(self):
        def get_nearest_from_que():
            min = 1000000
            el_num = 0
            for i in self.queue:
                if len(self.path[i['y']][i['x']]) < min :
                    min = len(self.path[i['y']][i['x']])
                    min_el = el_num
                el_num = el_num + 1
            return min_el
        #what we reurn
        self.result = []
        #cells near aims
        self.build_way = []

        self.checked = []
        
        self.path = []
        
        self.len = []
        self.build_way = []
        self.result = []
        self.initial_pathes()
    
        #set start position
        self.queue.append(self.start)
        while(len(self.queue) > 0):
            cur_el = get_nearest_from_que()
            cur = self.queue[cur_el]
            # print(self.queue,"queue")
            check = self.check_move_left(cur)
            self.check_move(check, cur)

            check = self.check_move_up(cur)
            self.check_move(check, cur)
                    
            check = self.check_move_right(cur)
            self.check_move(check, cur)

            check = self.check_move_down(cur)
            self.check_move(check, cur)
            self.checked.append(cur)
            self.queue.pop(cur_el)

        countx = 0
        county = 0
        for i in self.path:
            for j in i:
                self.len[county][countx] = len(j)
                countx = countx + 1
            countx = 0
            county = county + 1
        for i in self.build_way:
            self.result.append(self.path[i['y']][i['x']])
        return self.result