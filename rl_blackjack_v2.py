import random

#  This is not the correct instruction set, unsure where I got this
'    RL lab 5 Spring 2023. Andrew Fiore'
'    Program a Monte Carlo solution to Blackjack. '
'    Create classes for agent(policy), Environment (includes dealer, deck of cards), '
'        and the state of the agent (includes a list of cards). '
'    Part 1 is to program a default policy and use Monte Carlo to estimate value of each state given policy. '
'    You should be able to program exploring starts to evaluate the policy. '
'    Since it is episodic, you do not need to have a discount factor.'

# Everything is random in this version, not best approach to start values


class Agent:
    def __init__(self):
        self.policy = self.default_policy

# Initial policy
    @staticmethod
    def default_policy(state):
        return 'stick' if state.player_sum >= 20 else 'hit'


class State:
    def __init__(self, player_sum, dealer_card, usable_ace):
        self.player_sum = player_sum
        self.dealer_card = dealer_card
        self.usable_ace = usable_ace


class Environment:
    def __init__(self):
        self.deck = [i for i in range(1, 11)] + [10, 10, 10]
        self.dealer = None
        self.agent = None

    def draw_card(self):
        return random.choice(self.deck)

    @staticmethod
    def is_bust(total):
        return total > 21

    def dealer_turn(self):
        while True:
            card = self.draw_card()
            if self.dealer < 17:
                self.dealer += card
                if self.is_bust(self.dealer):
                    return True
            else:
                break
        return False

    def run_episode(self, agent, initial_state, initial_action):
        self.agent = agent
        self.dealer = initial_state.dealer_card

        state = initial_state
        action = initial_action

        player_bust = False
        dealer_bust = False

        states_actions_visited = [(state, action)]

        while action == 'hit':  # should handle counting ace as 1 or 11
            card = self.draw_card()
            if state.usable_ace and state.player_sum + card > 21:  # convoluted test for ace
                state = State(state.player_sum + card - 10, state.dealer_card, False) 
            else:
                state = State(state.player_sum + card, state.dealer_card, state.usable_ace)
            if self.is_bust(state.player_sum):
                player_bust = True
                break
            action = self.agent.policy(state)
            states_actions_visited.append((state, action))

        if not player_bust:
            dealer_bust = self.dealer_turn()

        reward = 0  # value logic
        if player_bust:
            reward = -1
        elif dealer_bust or state.player_sum > self.dealer:
            reward = 1
        elif state.player_sum == self.dealer:
            reward = 0
        else:
            reward = -1

        return states_actions_visited, reward


def monte_carlo_with_exploring_starts(agent, env, num_episodes):
    returns_sum = {}
    returns_count = {}
    state_values = {}

    #  this has problems, try draw_card instead of picking random start value
    for _ in range(num_episodes):
        player_sum = random.choice(range(12, 22))  # starting card range
        dealer_card = random.choice(range(1, 12))  # starting card range
        usable_ace = random.choice([True, False])  # agent have usable ace?
        initial_state = State(player_sum, dealer_card, usable_ace)
        initial_action = random.choice(['hit', 'stick'])  # exploring starts

        states_actions_visited, reward = env.run_episode(agent, initial_state, initial_action)

        for state, action in states_actions_visited:
            key = (state.player_sum, state.dealer_card, state.usable_ace, action)
            if key not in returns_sum:
                returns_sum[key] = 0
            if key not in returns_count:
                returns_count[key] = 0
            returns_sum[key] += reward
            returns_count[key] += 1
            state_key = (state.player_sum, state.dealer_card, state.usable_ace)
            if state_key not in state_values:
                state_values[state_key] = 0
            state_values[state_key] = returns_sum[key] / returns_count[key]

    return state_values


if __name__ == "__main__":
    num_episodes = 100000
    agent = Agent()
    env = Environment()
    state_values = monte_carlo_with_exploring_starts(agent, env, num_episodes)

    for key, value in state_values.items():
        player_sum, dealer_card, usable_ace = key
        print(f"Player sum: {player_sum}, Dealer card: {dealer_card}, Usable Ace: {usable_ace}, State value: {value:.2f}")

