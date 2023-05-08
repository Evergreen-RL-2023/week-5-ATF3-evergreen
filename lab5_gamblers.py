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
p_heads = 0.4 # set probability of heads
gamma = 0.9

class Agent(object):

    def __init__(self):
        self.values = np.zeros(N)


class Environment(object):
    def __init__(self, p_heads=0.4):
        self.p_heads = p_heads

# TODO get the indexing right, next_state can't return > 99
    def step(self, state, action):
        if rnd.random() <= self.p_heads:
            next_state = state + action
        else:
            next_state = state - action

        if next_state >= 99:  # win
            reward = 1
             # next_state = 0  make next state value = 0  TODO
            agent.values[next_state] = 0
            
        elif next_state == 0:  # lose 
            reward = 0
        else:
            reward = 0

        return next_state, reward


def value_iteration(agent, environment, num_iterations):
    for _ in range(num_iterations):
        new_values = np.zeros(N)  # check for index oob
        for state in range(1, N):
            values = []
            for action in range(1, min(state, N - state)+ 1):
                next_state, reward = environment.step(state, action)
                values.append(reward + agent.values[next_state - 1] * gamma)
            new_values[state - 1] = np.mean(values)  # Uniform random policy
        agent.values = new_values


if __name__ == "__main__":
    rnd.seed(42)

    agent = Agent()
    environment = Environment()

    num_iterations = 10000
    value_iteration(agent, environment, num_iterations)

    print("Values after {} iterations:".format(num_iterations))
    for i, value in enumerate(agent.values):
        print("State {}: {:.4f}".format(i, value))