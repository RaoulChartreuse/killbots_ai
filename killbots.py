import numpy #I am using numpy to avoid the ugly array in python


class killbots:
    """PLay a game of killbots
    """
    _max_energy = 12

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
        self.energy = 0
        self.populate(8)
        
        

    def empty_rnd_cell(self) :
        x,y=-1,-1
        while 1:
            x = numpy.random.randint(self.row)
            y = numpy.random.randint(self.col)
            if self.land[x][y]==0 : break
        return x,y

    
    def populate(self, N_bot):
        self.land = numpy.zeros((self.row, self.col),
                                dtype=numpy.uint8)
        self.land[self.row/2][self.col/2] = 1
        self.hx = row / 2
        self.hy = col / 2
        
        for _ in range(N_bot):
            x,y = self.empty_rnd_cell()
            self.land[x][y] = 2
        #Fastbot plus tard


    def play(self, action):
        """Play a round of game, need an action
        Return 1 if hero is still alive
        Return 0 if hero is dead
        Return -1 if the move is 
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
        pass

        
        
        


a = killbots()
print a.land
