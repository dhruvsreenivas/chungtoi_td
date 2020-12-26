from collections import defaultdict
import numpy as np


class QLearningAgent:
    # pretty much based off of https://github.com/kamenbliznashki/sutton_barto/blob/master/agents.py

    def __init__(self, gamma, alpha, eps, game):
        # Q learning agent
        self.gamma = gamma  # discount factor
        self.alpha = alpha  # learning rate/Bellman error weight parameter
        self.eps = eps  # eps-greedy parameter
        # will keep track of q values of all (s, a) encountered
        self.q_values = defaultdict(float)
        self.game = game

    def reset(self):
        self.q_values = defaultdict(float)
        self.num_updates_done = 0

    def q_value(self, state, action):
        return self.q_values[(state, action)]

    def get_best_action(self):
        s = self.game.get_state()
        action_set = self.game.get_action_set(s)
        q_vals = [self.q_values[(s, action)] for action in action_set]
        best_q = np.max(q_vals)
        # will have a list of actions where estimated Q value is largest
        best_actions = [a for i, a in enumerate(
            action_set) if q_vals[i] == best_q]
        idx = np.random.choice(len(best_actions))
        action = best_actions[idx]
        return action

    def select_action(self):
        action_set = self.game.get_action_set(self.game.get_state())
        if action_set == []:
            return None
        else:
            if np.random.uniform() < self.eps:
                return self.get_best_action()
            else:
                # return any random action in action_set
                idx = np.random.choice(len(action_set))
                return action_set[idx]

    def update(self, state, action, reward, next_state):
        # Q(s, a) += (r + gamma * max_a(Q(s', a)) - Q(s, a)), will return new Q value
        curr_q = self.q_value(state, action)
        next_q = np.max([self.q_values[(next_state, a)]
                         for a in self.game.get_action_set(next_state)])
        self.q_values[(state, action)] += (self.alpha * (reward +
                                                         self.gamma * next_q - curr_q))
        return self.q_values[(state, action)]
