import numpy as np
import random as rnd

N = 100  # The goal amount of money, in this case, $100


class Agent(object):

    def __init__(self):
        self.values = np.zeros(N + 1)  # Initialize the value function for each state (0 to N)
        self.policy=np.zeros(N + 1, dtype=int)

    # Compute the policy derived from the value function
    def compute_policy(self):
        policy = np.zeros(N + 1, dtype=int)  # Initialize policy
        for state in range(1, N):  # Iterate through states
            values = []  # Initialize an empty value list
            for action in range(1, min(state, N - state) + 1):  # Iterate through possible actions
                next_state, _ = environment.step(state, action)  # Get the next state given current action
                values.append(agent.values[next_state])  # Calculate the value of the current action
            self.policy[state] = np.argmax(values) + 1  # Choose action that maximizes the value
        # return policy


class Environment(object):
    def __init__(self, p_heads=0.4):
        self.p_heads = p_heads  # Probability of winning (heads)

    def step(self, state, action):
        # Simulate a coin flip with the probability (heads)
        if rnd.random() < self.p_heads:
            next_state = state + action  # If won, add the bet amount to the current state
        else:
            next_state = state - action  # If lost, subtract the bet amount from the current state
            
        if next_state == 100:
            reward = 1  # Gambler reaches $100, reward is 1
            next_state = 0
        elif next_state == 0:
            reward = 0  # Gambler reaches $0, reward is 0
        else:
            reward = 0  # catch anything weird

        return next_state, reward


def value_iteration(agent, environment, num_iterations):
    for _ in range(num_iterations):  # iterations set in main
        new_values = np.zeros(N + 1)  # Initialize new_values for updated value function
        for state in range(1, N):  # Iterate through all states except terminal
            values = []  # Initialize an empty values list

            # Iterate through all actions for a state
            for action in range(1, min(state, N - state) + 1):
                next_state, reward = environment.step(state, action)  # Simulate next state, reward, for current action
                values.append(reward + agent.values[next_state])  # Calculate the current value

            # Update the value function using the maximum of all action values
            new_values[state] = max(values)

        agent.values = new_values  # Update the agent's value function with new_values


# Simulate an episode using the agent's policy
def simulate_episode(agent, environment, initial_state): # this still won't print
    state = initial_state
    while state != 0 and state != 100:
        action = agent.policy[state]  # Get the action from the policy
        # print(f"Wallet balance: {state}, Bet: {action}")  # Print wallet balance and bet
        state, _ = environment.step(state, action)  # Perform the action and update the state
    return state == 100  # Return True if the agent won, False otherwise


if __name__ == "__main__":
    rnd.seed(42)

    agent = Agent()
    environment = Environment()

    num_iterations = 1000
    value_iteration(agent, environment, num_iterations)

    policy = agent.compute_policy()

    initial_state = 50
    state = initial_state
    while state != 0 and state != 100:
        action = policy[state]
        print(f"Wallet balance: {state}, Bet: {action}")
        state, _ = environment.step(state, action)

    print(f"Result: {'Won' if state == 100 else 'Lost'}")