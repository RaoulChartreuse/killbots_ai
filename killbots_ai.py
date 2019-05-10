import killbots
import numpy
import matplotlib.pyplot as plt
from scipy import stats  
import time

class killbots_ai(killbots.killbots):

    def get_action(self):
        action = -1
        action_possible = list(range(13))
        for i in range(9):#ON ne verifie que les mouvements directs
            if not self.check_action(i) :
                action_possible.remove(i)
        if self.energy == 0 : action_possible.remove(11)
        else : action_possible.remove(10)

        return numpy.random.choice(action_possible)

    def update_display(self):
        pass


    def play_n_games(self, N):
        result = numpy.empty(N , dtype=int)
        for i in range(N):
            self.__init__()
            self.play()
            result[i] = self.score
        return result

def main():
    a = killbots_ai()
    start_time = time.time()  
    res = a.play_n_games(5000)
    interval = time.time() - start_time
    print (interval, "s")
    print ("Moyenne :", numpy.mean(res))

    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    hist=plt.hist(res, numpy.max(res)//5, normed=True)
    ax.set_yscale("log", nonposy='clip')
    plt.xlabel("Score")
    plt.ylabel("Frequence normalizée")
    plt.title("Histogramme")

    #Modelisation f(t) = A_0 exp(-t/tau)
    A0, tau = stats.expon.fit(res)
    
    print ("Fit :", A0, tau )
    xt = plt.xticks()[0]  
    xmin, xmax = min(xt), max(xt)  
    lnspc = numpy.linspace(xmin, xmax, len(res))
    pdf = stats.expon.pdf(lnspc, A0, tau)
    plt.plot(lnspc, pdf, label="Ajustement")

    
    plt.show()

    
if __name__ == "__main__":
    # execute only if run as a script
    main()
