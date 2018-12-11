import numpy #I am using numpy to avoid the ugly array in python

def isUp(action):
    return action < 3

def isDown(action):
    return action>=6 and action<9

def isLeft(action):
    return action%3 == 0 and action<9

def isRight(action):
    return action%3 == 2 and action<9
    
class killbots:
    """PLay a game of killbots
    """
    _max_energy = 12
    _bot_points = 5
    _fastbot_points = 10
    _energy_points = 5

    def __init__(self, row = 16, col = 16, graph = True):
        self.hx = row / 2
        self.hy = col / 2
        self.row = row
        self.col = col
        #Codage de la map
        # 0 vide
        # 1 hero
        # 2 bot
        # 3 fast bot
        # 4 junk

        self.round = 1
        self.score = 0
        self.energy = 5
        self.populate(8)
        self.isDead = False
        

    def empty_rnd_cell(self) :
        x,y=-1,-1
        while 1:
            x = numpy.random.randint(self.row)
            y = numpy.random.randint(self.col)
            if self.land[x][y]==0 : break
        return x,y


    def is_in_bord(self, x,y):
        if ( x >= 0
             and x < self.row
             and y >= 0
             and y < self.col) :
            return True
        return False

    def can_push(self, action):
        mx=0
        if isUp(action) : mx=-1
        if isDown(action) : mx = 1
        my=0
        if isLeft(action) : my = -1
        if isRight(action) : my = 1
        x,y = mx, my
        
        while(self.land[self.hx+x][self.hy+y] == 4
              and  self.is_in_bord(self.hx+x,self.hy+y)):
            x += mx
            y += my
        if (self.is_in_bord(self.hx+x, self.hy+y)):
            return True

        return False
            
    def populate(self, N_bot):
        self.land = numpy.zeros((self.row, self.col),
                                dtype=numpy.uint8)
        self.land[self.row/2][self.col/2] = 1
        self.hx = self.row / 2
        self.hy = self.col / 2
        
        for _ in range(N_bot):
            x,y = self.empty_rnd_cell()
            self.land[x][y] = 2
        #Fastbot plus tard


    def play(self, action):
        """Play a round of game, need an action
        Return 1 if hero is still alive
        Return 0 if hero is dead
        Return -1 if the move is illegal
        Action code :
        0 = up left 
        1 = up
        2 = up right
        3 = left
        4 = do nothing
        5 = right
        6 = down left
        7 = down
        8 = down right
        9 = wait
        10 = teleport
        11 = teleport safely
        """

        #Bounded move
        if ((isUp(action)  and self.hx == 0 )
            or (isDown(action) and self.hx == self.row-1)
            or (isLeft(action) and action<9 and self.hy == 0 )
            or (isRight(action) and action<9 and self.hy == self.col-1)
            ) : return -1

        if action == 10 :
            x,y = self.empty_rnd_cell()
            self.land[self.hx][self.hy] = 0
            self.hx = x
            self.hy = y
            self.land[x][y] = 1
        
        mx=0
        if isUp(action) : mx=-1
        if isDown(action) : mx = 1
        my=0
        if isLeft(action) : my = -1
        if isRight(action) : my = 1
        if ( self.land[self.hx + mx][self.hy + my] == 0):
            self.land[self.hx][self.hy] = 0
            self.hx += mx
            self.hy += my
            self.land[self.hx][self.hy] = 1
        elif ( self.land[self.hx + mx][self.hy + my] == 4
               and self.can_push(action)):
            #Check and manage pushing the junk

            x,y = mx, my
        
            while(self.land[self.hx+x][self.hy+y] == 4
                  and  self.is_in_bord(self.hx+x,self.hy+y)):
                x += mx
                y += my
            if (self.land[self.hx+x][self.hy+y] == 2 or self.land[self.hx+x][self.hy+y] == 4):
                if self.energy< self._max_energy == 12:
                    self.energy += 1
                else :
                    self.score += _energy_points
                
            while ( abs(x) > 0 or abs(y) > 0):
                self.land[self.hx+x][self.hy+y] = self.land[self.hx+x-mx][self.hy+y-my]
                x -= mx
                y -= my

            
            self.land[self.hx][self.hy] = 0
            self.hx += mx
            self.hy += my


        
        self.move_bot()
        
        if self.isDead : return 0
        else :return 1
  

    
    def move_bot(self, is_fastbot = False):
        """
        """
        bot = 2
        if is_fastbot : bot = 3 

        bot_xy = numpy.argwhere(self.land == bot)

        keep_item = numpy.argwhere( numpy.logical_and(self.land != bot,self.land > 0))
        new_land  = numpy.zeros((self.row, self.col),
                                dtype=numpy.uint8)
        for xy in keep_item :
            new_land[xy[0]][xy[1]] = self.land[xy[0]][xy[1]]

        print new_land
        print bot_xy
        for xy in bot_xy:
            print xy, xy[0], xy[1], "  :",
            mx = xy[0] + numpy.sign(self.hx-xy[0])
            my = xy[1] + numpy.sign(self.hy-xy[1])
            print mx, " , ", my 
                      
            if new_land[mx][my] > 0 :
                if new_land[mx][my] == 1 :
                    self.isDead = True
                else :
                    #score
                    if new_land[mx][my] == 2 : self.score += self._bot_points
                    if new_land[mx][my] == 3 : self.score += self._fastbot_points
                    if is_fastbot : self.score +=  self._fastbot_points
                    else : self.score += self._bot_points
                    
                new_land[mx][my] = 4

                
            else :
                new_land[mx][my] = bot
        self.land = numpy.copy(new_land)     
        

#Fonction de test
def map_push1(a):
    a.land = numpy.zeros((a.row, a.col), dtype=numpy.uint8)
    a.land[a.row/2][a.col/2] = 1
    a.hx = a.row / 2
    a.hy = a.col / 2
    a.land[6][7] = 2
    a.land[6][9] = 2
    a.land[0][8] = 2   

def main():
    a = killbots()
    #map_push1(a)
    print a.land
    while not(a.isDead):
        print "----------------------------"
        print "Action :"
        action = input("Action ?")
        a.play(action)    
        print a.land
        print "Score : ", a.score, "  | Energy :", a.energy

if __name__ == "__main__":
    # execute only if run as a script
    main()
