import random


class Agent:
    def __init__(self):
        self.policy = self.default_policy
        self.value_function = {}

    def default_policy(self, state):
        if state.get_value() < 20:
            return "hit"
        else:
            return "stick"


class Environment:
    def __init__(self):
        self.agent = Agent()
        self.dealer = State()
        self.deck = [i for i in range(1, 11)] + [10, 10, 10]  # 1-9 and three 10s representing face cards

    def deal_card(self):
        return random.choice(self.deck)

    def play(self, agent_state, action):  # figure out why this runs to 30
        if action == "hit":
            agent_state.add_card(self.deal_card())
            if agent_state.is_busted():
                return -1
        else:
            while self.dealer.get_value() < 17:
                self.dealer.add_card(self.deal_card())
                if self.dealer.is_busted():
                    return 1
            if agent_state.get_value() > self.dealer.get_value():
                return 1
            elif agent_state.get_value() == self.dealer.get_value():
                return 0
            else:
                return -1
        #  return None


class State:
    def __init__(self, cards=None):
        self.cards = cards if cards else []

    def add_card(self, card):
        self.cards.append(card)

    def is_busted(self):  # might be simpler to do this check inline
        return self.get_value() > 21

    def get_value(self):
        value = sum(self.cards)
        num_aces = self.cards.count(1)
        while num_aces > 0 and value <= 11:
            value += 10
            num_aces -= 1
        return value


def monte_carlo(num_episodes, agent, env):
    returns = {}
    for _ in range(num_episodes):
        agent_state = State([env.deal_card(), env.deal_card()])
        dealer_card = env.deal_card()
        env.dealer = State([dealer_card])
        action = random.choice(["hit", "stick"])  # random exploring

        episode = [(agent_state, action)]
        reward = None
        while reward is None:
            reward = env.play(agent_state, action)
            if reward is None:
                action = agent.policy(agent_state)
                episode.append((agent_state, action))
                agent_state.add_card(env.deal_card())  # add new card to agent's hand

                if agent_state.is_busted():  # check if agent's hand value exceeds 21
                    reward = -1  # agent loses the game
                    break  # end episode

        # update value for state-action
        for state, action in episode:
            state_key = (state.get_value(), dealer_card, action)
            if state_key not in returns:
                returns[state_key] = []
            returns[state_key].append(reward)

            if state_key not in agent.value_function:
                agent.value_function[state_key] = 0
            agent.value_function[state_key] = sum(returns[state_key]) / len(returns[state_key])


if __name__ == "__main__":
    num_episodes = 500000
    env = Environment()
    monte_carlo(num_episodes, env.agent, env)

    for state_key in sorted(env.agent.value_function.keys()):
        print(f"State (A Hand, D Hand, H/S): {state_key}, Value: {env.agent.value_function[state_key]:.2f}")