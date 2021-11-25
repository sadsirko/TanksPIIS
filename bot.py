import random

class Bot:
    def __init__(self,bot_arr) :
        self.bot_arr = bot_arr
    def random_move(self,map,bul_arr):
        for bot in self.bot_arr:
            rand_move  = random.randint(0,10)
            if rand_move == 0:
                bot.move_up(map)
            if rand_move == 1:
                bot.move_right(map)
            if rand_move == 2:
                bot.move_down(map)
            if rand_move == 3:
                bot.move_left(map)
            if rand_move == 4:
                res = bot.fire(bul_arr)
                if res != False:
                    bul_arr = res  
        return bul_arr
        