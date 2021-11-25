from const import BIG_BLOCKS, BLOCK_SIZE, BULLET_SPEED,ZOOM_16
class Bullet():
    def __init__(self,posX,posY,direction = 'up'):
        self.pos = {"x" : posX,"y": posY }
        self.direction = direction 
        self.left_up = {"x":self.pos['x'] ,"y":self.pos['y']}
        self.left_down = {"x":self.pos['x'],"y":self.pos['y']+ ZOOM_16['y']}
        self.right_up = {"x":self.pos['x']+ ZOOM_16['x'],"y":self.pos['y'] }
        self.right_down = {"x":self.pos['x']+ ZOOM_16['x'],"y":self.pos['y'] + ZOOM_16['y']}

#rewrite!!!!1
    def check_excplosion(self,map):
        dest_cells = []
        if self.direction == "up":
            if self.check_collision(map,self.left_up) :
                    dest_cells.append(self.left_up)
            if  self.check_collision(map,self.right_up):
                    dest_cells.append(self.right_up)           
        if self.direction == "left":
            if self.check_collision(map,self.left_up) :
                    dest_cells.append(self.left_up)
            if  self.check_collision(map,self.left_down):
                    dest_cells.append(self.left_down)                        
        if self.direction == "down":
            if self.check_collision(map,self.right_down) :
                    dest_cells.append(self.right_down)
            if  self.check_collision(map,self.left_down):
                    dest_cells.append(self.left_down)                                         
        if self.direction == "right":
            if self.check_collision(map,self.right_down) :
                    dest_cells.append(self.right_down)
            if  self.check_collision(map,self.right_up):
                    dest_cells.append(self.right_up)                 
        return dest_cells

    def move_up(self):
        self.pos["y"] = self.pos["y"] - BULLET_SPEED
    def move_down(self):
        self.pos["y"] = self.pos["y"] + BULLET_SPEED
    def move_right(self):
        self.pos["x"] = self.pos["x"] + BULLET_SPEED
    def move_left(self):
        self.pos["x"] = self.pos["x"] - BULLET_SPEED
    
    def move(self):
        if self.direction == "up":
            self.move_up()
        
        if self.direction == "down":
            self.move_down()
        
        if self.direction == "left":
            self.move_left()
        
        if self.direction == "right":
            self.move_right()

    def check_collision(self,map,pos):
        self.left_up = {"x":self.pos['x'] ,"y":self.pos['y']}
        self.left_down = {"x":self.pos['x'],"y":self.pos['y']+ ZOOM_16['y']}
        self.right_up = {"x":self.pos['x']+ ZOOM_16['x'],"y":self.pos['y'] }
        self.right_down = {"x":self.pos['x']+ ZOOM_16['x'],"y":self.pos['y'] + ZOOM_16['y']}
        x = int(pos['x'] // BLOCK_SIZE)
        y = int(pos['y'] // BLOCK_SIZE)
        if y >= BIG_BLOCKS['h'] or y < 0 :
            return False
        if x >= BIG_BLOCKS['w'] or x < 0 :
            return False
        # print(map[y][x])
        if map[y][x] != '.':
            return True