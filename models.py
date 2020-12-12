import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random


class Agent:
    def __init__(self, td_lam, alpha, lr, eps):
        self.td_lam = td_lam
        self.alpha = alpha
        self.lr = lr
        self.eps = eps  # this is for epsilon-greedy strategy with respect to value function given by network below

        # value network (make sure to initialize weights like in paper later on)
        self.linear1 = nn.Linear(20, 30, bias=True)
        self.linear2 = nn.Linear(30, 1)
        self.prev_evals = [0]

        self.optimizer = torch.optim.Adam(lr=self.lr)

    def forward(self, state):
        assert len(state) == 20
        state = torch.FloatTensor(state)
        value = F.tanh(2/3 * self.linear1(state)) * 1.7159
        value = self.linear2(value)
        return value

    def initial_state_val(self, game):
        arr = [0] * 20
        arr[18] = 1
        arr = torch.FloatTensor(arr)
        return self.forward(arr)

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
        # append eval
        game.act(action)
        value = self.forward(game.get_state())
        self.prev_evals.append(value)

    # update method uses the TD learning method that Tesauro derived & implemented for TD-Gammon
    # need to fless out the zero case at the start
    def update_value_fn(self):
        disc_loss = 0
        latest_diff = self.prev_evals[-1] - self.prev_evals[-2]
        t = len(self.prev_evals)-1
        for k in range(len(self.prev_evals)-1):
            disc_loss += ((self.td_lam ** (t-k)) * self.prev_evals[k])

        loss = self.alpha * latest_diff * disc_loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
