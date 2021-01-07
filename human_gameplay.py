from agents import ValueAgent
import numpy as np
from game import ChungToi
import pandas as pd
import ast


def human_vs_machine(game, agent):
    # human plays against the MACHINE
    first = str(input('Do you want to go first? Y/N\n'))
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
                action = (None, int(action_tup[1]), int(action_tup[2]))
            else:
                action = (int(action_tup[0]), int(
                    action_tup[1]), int(action_tup[2]))
            print("action set", game.get_action_set(s))
            print("action", action)
            if action not in game.get_action_set(s):
                print('You cannot play this action--please choose another one.')
                curr_player = -1
            else:
                _, _ = game.act(s, action)
        else:
            # else agent goes
            action = agent.select_action(game)
            _, _ = game.act(s, action)

        game.print_game_state()
        print()
        num_moves += 1
        curr_player *= -1
        if num_moves == 1000:
            print('game gone on too long--call it a draw')
            break


if __name__ == '__main__':
    game = ChungToi()
    key_df = pd.read_csv('trained_agent_state_vals.csv')
    key_df['States'] = key_df['States'].map(lambda s: ast.literal_eval(s))
    agent = ValueAgent(alpha=0, player_num=1, eps=1, key_lst=list(
        key_df['States']), value_lst=list(key_df['Values']))

    human_vs_machine(game, agent)
