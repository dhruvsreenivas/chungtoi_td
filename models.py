import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random


class Agent:
    def __init__(self, td_lam, lr, eps):
        self.td_lam = td_lam
        self.lr = lr
        self.eps = eps  # this is for epsilon-greedy strategy with respect to value function given by network below

        # value network (make sure to initialize weights like in paper later on)
        self.linear1 = nn.Linear(20, 30, bias=True)
        self.linear2 = nn.Linear(30, 1)
        self.loss = 0

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

    # do the action and legit change the state of the game
    def act(self, game, action):
        # take current value evaluation of state and add it to past value evaluations
        value = self.forward(game.get_state())
        self.loss *= self.td_lam
        self.loss += value
        game.act(action)

    # update method uses the TD learning method that Tesauro used to learn TD-Gammon
    def update_value_fn(self):
        # every time you have a loss, you multiply the current loss value by lambda and add Y_t
        self.optimizer.zero_grad()
        self.loss.backward()
        self.optimizer.step()
