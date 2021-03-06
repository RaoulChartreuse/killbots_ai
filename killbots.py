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
    _mouv = [ "0 : up left",
              "1 :  up",
              "2 : up right",
              "3 : left",
              "4 : do nothing",
              "5 : right",
              "6 : down left",
              "7 : down",
              "8 : down right",
              "9 : wait",
              "10 : teleport",
              "11 : teleport safely",
              "12 : do nothing "
    ]
    
    _max_energy = 12
    _bot_points = 5
    _fastbot_points = 10
    _energy_points = 5
    _initial_bot = 8
    _initial_fastbot = -2

    def __init__(self, row = 16, col = 16):
        self.hx = row // 2
        self.hy = col // 2
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
        self.energy = 50
        self.N_bot = self._initial_bot
        self.N_fbot = self._initial_fastbot
        self.populate()
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
        
        while(self.is_in_bord(self.hx+x,self.hy+y)
              and  self.land[self.hx+x][self.hy+y] == 4):
            x += mx
            y += my
        if (self.is_in_bord(self.hx+x, self.hy+y)):
            return True

        return False
            
    def populate(self):
        self.land = numpy.zeros((self.row, self.col),
                                dtype=numpy.uint8)
        self.land[self.row//2][self.col//2] = 1
        self.hx = self.row // 2
        self.hy = self.col // 2
        
        for _ in range(self.N_bot):
            x,y = self.empty_rnd_cell()
            self.land[x][y] = 2
        for _ in range(self.N_fbot):
            x,y = self.empty_rnd_cell()
            self.land[x][y] = 3
        self.N_bot += 2
        self.N_fbot += 2


    def action(self, action):
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
        12 = do nothing 
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

        elif action == 11 and self.energy>0 :
            self.energy -= 1
            x,y = self.teleport_safely()
            self.land[self.hx][self.hy] = 0
            self.hx = x
            self.hy = y
            self.land[x][y] = 1
        elif action == 9:
            return self.wait()
        
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
                    self.score += self._energy_points
                
            while ( abs(x) > 0 or abs(y) > 0):
                self.land[self.hx+x][self.hy+y] = self.land[self.hx+x-mx][self.hy+y-my]
                x -= mx
                y -= my

            
            self.land[self.hx][self.hy] = 0
            self.hx += mx
            self.hy += my


        
        self.move_bot()
        self.move_bot(True)

        if self.isDead :
            return 0
        else :
            if self.count_bot() == 0 :
                return 2

            return 1
  

    
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


        for xy in bot_xy:
            mx = xy[0] + numpy.sign(self.hx-xy[0])
            my = xy[1] + numpy.sign(self.hy-xy[1])
                      
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

    def teleport_safely(self):
        """
        Comme dans le code original on choisi un depart puis on verifie pour chaque case si elle est safe
        """
        x_start = numpy.random.randint(self.row)
        y_start = numpy.random.randint(self.col)

        x,y = x_start, y_start
        
        while True:
            #Incermentation
            if x < self.row -1 :
                x += 1
            else:
                x = 0
                if y < self.col -1:
                    y += 1
                else :
                    y = 0

            #Test :
            if self.safe_teleport(x, y):
                return x, y
            if x == x_start and y == y_start:
                return self.hx, self.hy #Pas de teleportation

    def safe_teleport(self, x, y):
        """The search of safe_teleport spot is not factorized.
        This is done on purpose to not hide the logic
        """
        #On regarde si la casse est vide :
        #Ainsi on ne se teleporte pas a la meme position
        if self.land[x][y] !=0 : return False

        #On regarde 'a 1 case de distance si il n'y a pas de bot
        if x>0 : 
            if self.land[x-1][y] == 2 or self.land[x-1][y] == 3 : return False
            if y>0 :
                if self.land[x-1][y-1] == 2 or self.land[x-1][y-1] == 3 : return False
            if y < self.col -1:
                if self.land[x-1][y+1] == 2 or self.land[x-1][y+1] == 3 : return False
        if y>0 :
            if self.land[x][y-1] == 2 or self.land[x][y-1] == 3 : return False
        if y < self.col -1:
                if self.land[x][y+1] == 2 or self.land[x][y+1] == 3 : return False
        if x< self.row - 1:
            if self.land[x+1][y] == 2 or self.land[x+1][y] == 3 : return False
            if y>0 :
                if self.land[x+1][y-1] == 2 or self.land[x+1][y-1] == 3 : return False
            if y < self.col -1:
                if self.land[x+1][y+1] == 2 or self.land[x+1][y+1] == 3 : return False


        #On regarde 'a 2 cases si il n'y a pas de fast bot
        #Pour les detail regarder le code source a engine.cpp fonction : bool Killbots::Engine::moveIsSafe
        #On verifier les coins:
        if x>0+1 and y>0+1:
            if self.land[x-1][y-1] == 0 and self.land[x-2][y-2] == 3 :return False
        if x>0+1 and y< self.col -2:
            if self.land[x-1][y+1] == 0 and self.land[x-2][y+2] == 3 :return False
        if x< self.row - 2 and y>0+1:
            if self.land[x+1][y-1] == 0 and self.land[x+2][y-2] == 3 :return False
        if x< self.row - 2 and y< self.col -2:
            if self.land[x+1][y+1] == 0 and self.land[x+2][y+2] == 3 :return False
        #On verifie les cotees:
        # il faut que la case adjasente soit vide sinon le danger est deja detecte ou il s'agit d'un junk qui protegge
        # Si il  y a un fastbot et au moins un autre robot (lent ou rapide) ils vont se collisioner
        if x> 0+1 and self.land[x-1][y]==0:
            robot=0
            fbot=0
            if y>0:
                if self.land[x-2][y-1] == 3 : fbot +=1
                if self.land[x-2][y-1] == 2 : robot +=1
            if self.land[x-2][y] == 3 : fbot +=1
            if self.land[x-2][y] == 2 : robot +=1          
            if y < self.col -1 :
                if self.land[x-2][y+1] == 3 : fbot +=1
                if self.land[x-2][y+1] == 2 : robot +=1
            if fbot ==1 and robot ==0 : return False
        if x < self.row -2 and self.land[x+1][y]==0:
            robot=0
            fbot=0
            if y>0:
                if self.land[x+2][y-1] == 3 : fbot +=1
                if self.land[x+2][y-1] == 2 : robot +=1
            if self.land[x+2][y] == 3 : fbot +=1
            if self.land[x+2][y] == 2 : robot +=1          
            if y < self.col -1 :
                if self.land[x+2][y+1] == 3 : fbot +=1
                if self.land[x+2][y+1] == 2 : robot +=1
            if fbot ==1 and robot ==0 : return False
                
        if y> 0+1 and self.land[x][y-1]==0:
            robot=0
            fbot=0
            if x>0:
                if self.land[x-1][y-2] == 3 : fbot +=1
                if self.land[x-1][y-2] == 2 : robot +=1
            if self.land[x][y-2] == 3 : fbot +=1
            if self.land[x][y-2] == 2 : robot +=1          
            if x < self.row -1 :
                if self.land[x+1][y-2] == 3 : fbot +=1
                if self.land[x+1][y-2] == 2 : robot +=1
            if fbot ==1 and robot ==0 : return False
        if y < self.col -2 and self.land[x][y+1]==0:
            robot=0
            fbot=0
            if x>0:
                if self.land[x-1][y+2] == 3 : fbot +=1
                if self.land[x-1][y+2] == 2 : robot +=1
            if self.land[x][y+2] == 3 : fbot +=1
            if self.land[x][y+2] == 2 : robot +=1          
            if x < self.col -1 :
                if self.land[x+1][y+2] == 3 : fbot +=1
                if self.land[x+1][y+2] == 2 : robot +=1
            if fbot ==1 and robot ==0 : return False
        return True

    def count_bot(self):
        n=0
        n+= numpy.count_nonzero( numpy.where( self.land == 2,1, 0))
        n+= numpy.count_nonzero( numpy.where( self.land == 3,1, 0))
        return n
    
    def wait(self):
        N_bot_initial = self.count_bot()
        while True:
            self.move_bot()
            self.move_bot(True)        
            if self.isDead : return 0
            N_bot = self.count_bot()
            if N_bot == 0:
                break
        self.energy = max(self._max_energy, self.energy+N_bot_initial)
        return 2 #Possiblement 2


    def check_action(self, action):
        if ((isUp(action)  and self.hx == 0 )
            or (isDown(action) and self.hx == self.row-1)
            or (isLeft(action) and action<9 and self.hy == 0 )
            or (isRight(action) and action<9 and self.hy == self.col-1)
        ) : return False
        
        mx=0
        if isUp(action) : mx=-1
        if isDown(action) : mx = 1
        my=0
        if isLeft(action) : my = -1
        if isRight(action) : my = 1
        if self.land[self.hx+mx][self.hy+my]==4: return True
        return self.safe_teleport(self.hx+mx, self.hy+my )
        
    
    def get_action(self):
        print("----------------------------")
        print("Action :")
        action = -1
        action_possible = list(range(13))
        for i in range(9):#ON ne verifie que les mouvements directs
            if not self.check_action(i) :
                action_possible.remove(i)
        if self.energy == 0 : action_possible.remove(11)
        while action_possible.count(action) !=1 :
            for i in action_possible: print(self._mouv[i])
            
            action = int(input("Action ?"))
        return action

    def update_display(self):
        print ("_____________________________")
        print (self.land)
        print ("Score : ", self.score, "  | Energy :", self.energy)
        print ("-----------------------------")
    
    def play(self):
        self.update_display()
        while not(self.isDead):
            if self.action(self.get_action()) == 2:
                self.populate()
            self.update_display()

"""
class killbots_ai(killbots):

    def get_action(self):
        return numpy.random.randint(0, 13)
"""        
        
#Fonction de test
def map_push1(a):
    a.land = numpy.zeros((a.row, a.col), dtype=numpy.uint8)
    a.land[a.row/2][a.col/2] = 1
    a.hx = a.row / 2
    a.hy = a.col / 2
    a.land[6][7] = 2
    a.land[6][9] = 2
    a.land[0][8] = 2   

def map_teleport(a):
    a.land = numpy.zeros((a.row, a.col), dtype=numpy.uint8)
    a.land[a.row/2][a.col/2] = 1
    a.hx = a.row / 2
    a.hy = a.col / 2
    a.land[6][7] = 2
    a.land[6][9] = 2
    a.land[0][8] = 2
    a.land[1][1] = 3
    a.land[2][5] = 3
    
def main():
    a = killbots()
    #a = killbots_ai()
    #    map_teleport(a)
    a.play()

if __name__ == "__main__":
    # execute only if run as a script
    main()
