from collections import defaultdict
import numpy as np
from game import is_terminal
import csv
import pandas as pd


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
        return self.q_values[(tuple(state), action)]

    def get_best_action(self):
        s = self.game.get_state()
        action_set = self.game.get_action_set(s)
        q_vals = [self.q_value(s, action) for action in action_set]
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
            raise Exception('No action available to take--game is over')
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
        action_vals = [self.q_value(next_state, a)
                       for a in self.game.get_action_set(next_state)]
        if len(action_vals) > 0:
            next_q = np.max(action_vals)
        else:
            next_q = 0
        self.q_values[(tuple(state), action)] += (self.alpha * (reward +
                                                                self.gamma * next_q - curr_q))
        return self.q_values[(tuple(state), action)]


class ValueAgent:
    def __init__(self, alpha, player_num, eps, key_lst=None):
        self.alpha = alpha
        self.player_num = player_num
        self.eps = eps
        # assigns probability of winning from each of those given states
        self.state_vals = {}
        self.key_lst = key_lst

        for key in key_lst:
            if is_terminal(key)[0]:
                if is_terminal(key)[1] == self.player_num:
                    self.state_vals[key] = 1.0
                else:
                    self.state_vals[key] = 0.0
            else:
                self.state_vals[key] = 1/2
        # have to make sure that the probability of winning from the winning states is 1, losing states is 0, other states is 0.5
        # basically revolves around getting a list of all possible states of the game, and making a dict that assigns the probabilities accordingly

    def reset(self):
        self.state_vals = {}
        for key in self.key_lst:
            if is_terminal(key)[0]:
                if is_terminal(key)[1] == self.player_num:
                    self.state_vals[key] = 1.0
                else:
                    self.state_vals[key] = 0.0
            else:
                self.state_vals[key] = 1/2

    def get_value(self, state):
        return self.state_vals[tuple(state)]

    def get_best_action(self, game):
        s = game.get_state()
        action_set = game.get_action_set(s)

        next_state_vals = [self.state_vals[tuple(
            game.next_state(s, action))] for action in action_set]
        best_state_val = np.max(next_state_vals)
        best_actions = [a for i, a in enumerate(
            action_set) if next_state_vals[i] == best_state_val]
        action_idx = np.random.choice(len(best_actions))
        return best_actions[action_idx]

    def select_action(self, game):
        s = game.get_state()
        action_set = game.get_action_set(s)

        if np.random.uniform() < self.eps:
            # epsilon chance you take the greedy action
            return self.get_best_action(game)
        else:
            return action_set[np.random.choice(len(action_set))]

    def update(self, state, next_state):
        # V(s) <- V(s) + alpha * (V(s') - V(s))
        curr_val = self.state_vals[tuple(state)]
        next_val = self.state_vals[tuple(next_state)]
        # print('prev state val: ' + str(curr_val))
        # print('next state val: ' + str(next_val))
        new_val = curr_val + self.alpha * (next_val - curr_val)
        self.state_vals[tuple(state)] = new_val

    def save_vals(self, filename):
        dictionary = self.state_vals
        df = pd.DataFrame({'States':list(dictionary.keys()),'Values':list(dictionary.values())})
        df.to_csv(f'{filename}.csv', index=False)
