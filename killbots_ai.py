import killbots
import numpy

class killbots_ai(killbots.killbots):

    def get_action(self):
        action = -1
        action_possible = range(13)
        for i in range(9):#ON ne verifie que les mouvements directs
            if not self.check_action(i) :
                action_possible.remove(i)
        if self.energy == 0 : action_possible.remove(11)
        else : action_possible.remove(10)

        return numpy.random.choice(action_possible)

    def update_display(self):
        pass


def main():
    a = killbots_ai()
    a.play()
    print a.score

if __name__ == "__main__":
    # execute only if run as a script
    main()
