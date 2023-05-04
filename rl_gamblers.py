'''
template: Richard Weiss, May 2023
The Gamblers Problem (gambler's ruin)
start with x dollars and bet on each round until
either the gambler reaches 0 (reward 0) or 100 (reward 1)

implement uniform random policy
'''
import numpy as np
import random as rnd

N = 100


class Agent(object):

    '''
        initialize the state
    '''
    def __init__(self):
        self.state = N/2
        self.values = np.zeros(N)

        
    def set_state(self, s):
        self.state = s

    def choose_action(self):
        return rnd.randrange(1, self.state + 1)

class Environment(object):
    # initialize agent


        

if __name__ == '__main__':
    rnd.seed(42)

    # create an Agent 
    
    # exploring starts
    for i in range(N):
        

    # print values
