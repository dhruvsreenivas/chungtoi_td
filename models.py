import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random


class Agent:
    def __init__(self, gamma, td_lam, lr, eps):
        self.gamma = gamma
        self.td_lam = td_lam
        self.lr = lr
        self.eps = eps  # this is for epsilon-greedy strategy with respect to value function given by network below

        # value network (make sure to initialize weights like in paper later on)
        self.linear1 = nn.Linear(20, 30, bias=True)
        self.linear2 = nn.Linear(30, 1)

        self.optimizer = torch.optim.Adam(lr=self.lr)

    def forward(self, state):
        assert len(state) == 20
        state = torch.FloatTensor(state)
        value = F.tanh(2/3 * self.linear1(state)) * 1.7159
        value = self.linear2(value)
        return value

    def select_action(self, game):
        # epsilon greedy
        action_set = game.get_action_set()
        p = random.uniform(0, 1)
        if p <= self.eps:
            # take greedy action (action that leads to largest valued state)
            best_action = action_set[0]
            best_value = -1 * float('inf')
            for a in action_set:
                next_state = game.next_state(a)
                value = self.forward(next_state)
                if value > best_value:
                    best_value = value
                    best_action = a

            return best_action
        else:
            # take random action
            return random.choice(action_set)

    # now we need to write the function to update the value network
