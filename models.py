from collections import defaultdict
import numpy as np


class Agent:
    # pretty much based off of https://github.com/kamenbliznashki/sutton_barto/blob/master/agents.py

    def __init__(self, gamma, alpha, eps, game):
        # Q learning agent
        self.gamma = gamma  # discount factor
        self.alpha = alpha  # learning rate/Bellman error weight parameter
        self.eps = eps  # eps-greedy parameter
        # will keep track of q values of all (s, a) encountered
        self.q_values = defaultdict(float)
        self.num_updates_done = 0
        self.game = game

    def reset(self):
        self.q_values = defaultdict(float)
        self.num_updates_done = 0

    def q_value(self, state, action):
        return self.q_values[(state, action)]

    def get_best_action(self):
        s = self.game.get_state()
        action_set = self.game.get_action_set()
        q_vals = [self.q_values[(s, action)] for action in action_set]
        best_q = np.max(q_vals)
        # will have a list of actions where estimated Q value is largest
        best_actions = [a for i, a in enumerate(
            action_set) if q_vals[i] == best_q]
        idx = np.random.choice(len(best_actions))
        action = best_actions[idx]
        return action

    def select_action(self):
        action_set = self.game.get_action_set()
        if action_set == []:
            return None
        else:
            return self.get_best_action()

    def comp_q_value(self, action):
        # will compute action value given current game state (in self.game) and current best action using bellman approximation
        next_state, reward = self.game.next_state(action)
        return reward + self.gamma * self.comp_value(next_state)

    def comp_value(self, state):
        best_action = self.get_best_action()
        if not best_action:
            return None
        else:
            return self.comp_q_value(best_action)

    def update(self, state, action, reward, next_state):
        # Q(s, a) += (r + gamma * max_a(Q(s', a)) - Q(s, a)), will return new Q value
        curr_q = self.q_value(state, action)
        next_q = self.comp_value(next_state)
        self.q_values[(state, action)] += self.alpha * (reward +
                                                        self.gamma * next_q - curr_q)
        self.num_updates_done += 1
        return self.q_values[(state, action)]
