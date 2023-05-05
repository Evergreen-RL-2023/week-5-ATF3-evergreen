'''
Reinforcement Learning, Spring 2023: Andrew Fiore

template: Richard Weiss, May 2023 - Instructor

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
        self.state = N // 2
        self.values = np.zeros(N + 1)

    def set_state(self, s):
        self.state = s

    def choose_action(self):
        return rnd.randrange(1, min(self.state, N - self.state) + 1)

class Environment(object):

    def __init__(self, p_heads=0.4):
        self.p_heads = p_heads

    def step(self, state, action):
        if rnd.random() < self.p_heads:
            next_state = state + action
        else:
            next_state = state - action
        reward = 1 if next_state == N else 0
        return next_state, reward

def exploring_starts(agent, environment, num_episodes):
    for _ in range(num_episodes):
        agent.set_state(rnd.randint(1, N - 1))
        while 0 < agent.state < N:
            action = agent.choose_action()
            next_state, reward = environment.step(agent.state, action)
            agent.values[agent.state] += 0.5 * (reward + agent.values[next_state] - agent.values[agent.state])
            agent.state = next_state

if __name__ == '__main__':
    rnd.seed(42)

    # create an Agent
    agent = Agent()

    # create an Environment
    environment = Environment()

     # exploring starts
    num_episodes = 1000
    exploring_starts(agent, environment, num_episodes)

    # print values
    print(agent.values[1:-1])