from agents import ValueAgent
import numpy as np
from game import ChungToi
import pandas as pd


def human_vs_machine(game, agent):
    # human plays against the MACHINE
    first = str(input('Do you want to go first? Y/N'))
    if first == 'Y':
        curr_player = 1
    else:
        curr_player = -1
    num_moves = 0
    while not game.is_terminal()[0]:
        s = game.get_state()
        if curr_player == 1:
            action_str = input(
                'Take an action in the game. An action is coded as (prev, next, orientation) where previous is the previous destination of token, next is the next destination, and orientation is the orientation wanted.\n')
            action_tup = tuple(map(str, action_str.split(',')))
            if action_tup[0] == 'None':
                action = (None, int(action[1]), int(action[2]))
            else:
                action = (int(action[0]), int(action[1]), int(action[2]))
            if action not in game.get_action_set(s):
                print('You cannot play this action--please choose another one.')
            else:
                _, _ = game.act(s, action)
        else:
            # else agent goes
            action = agent.select_action(game)
            _, _ = game.act(s, action)

        num_moves += 1
        curr_player *= -1
        if num_moves == 1000:
            print('game gone on too long--call it a draw')
            break


if __name__ == '__main__':
    game = ChungToi()
    keys = pd.read_csv('trained_agent_state_vals.csv')
    key_lst = keys.to_dict()
    print(len(key_lst.items()))
    # agent = ValueAgent(alpha=0, player_num=1, eps=1, key_lst=key_lst)
