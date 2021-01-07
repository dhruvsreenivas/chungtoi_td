from game import ChungToi, is_terminal, get_all_pos_keys
from agents import ValueAgent
import numpy as np
import matplotlib.pyplot as plt


def play_game(game, agent, adversary_agent, start_player):
    game.reset()
    num_moves = 0
    # print("start game for sure")
    while not game.is_terminal()[0]:
        # player 1 moves first
        # print("player " + str(game.curr_player) + ": will move now")
        # print('game still going on...')
        if game.curr_player == start_player:
            s = game.get_state()
            agent_a = agent.select_action(game)
            n_s, _ = game.act(s, agent_a)
            # update player 1 state val table
            agent.update(s, n_s)
            adversary_agent.update(s, n_s)
        else:
            # now time for player 2 to move
            s = game.get_state()
            adv_a = adversary_agent.select_action(game)
            n_s, _ = game.act(s, adv_a)
            # update player 1 state val table
            adversary_agent.update(s, n_s)
            agent.update(s, n_s)

        num_moves += 1
        if num_moves == 1000:
            return 0

    # print(f'game over--player {game.is_terminal()[1]} won')

    return game.is_terminal()[1]


def play_games(num_games, game, agent, adversary_agent, start_player):
    player_1_wins = 0
    player_2_wins = 0
    draws = 0
    for _ in range(num_games):
        winner = play_game(game, agent, adversary_agent, start_player)
        if winner == 1:
            player_1_wins += 1
        elif winner == -1:
            player_2_wins += 1
        else:
            draws += 1

    return player_1_wins, player_2_wins, draws


if __name__ == '__main__':
    NUM_GAMES = 5000
    key_lst = get_all_pos_keys()
    print("big chungus of a key list downloaded")
    game = ChungToi()
    print("made game")
    agent = ValueAgent(alpha=0.1, player_num=1, eps=0.85, key_lst=key_lst)
    print("vals initialized")
    adversary_agent = ValueAgent(
        alpha=0.1, player_num=-1, eps=0.85, key_lst=key_lst)
    print("starting gameplay...")

    # play NUM_GAMES games with player 1 starting
    p1, p2, d = play_games(NUM_GAMES, game, agent, adversary_agent, 1)
    print(p1, p2, d)

    # then player NUM_GAMES games with player 2 starting
    new_p1, new_p2, new_d = play_games(
        NUM_GAMES, game, agent, adversary_agent, -1)
    print(new_p1, new_p2, new_d)
    print(p1 + new_p1, p2 + new_p2, d + new_d)

    vals = list(agent.state_vals.values())
    l = np.unique(vals)
    print(l)
    print(len(l))

    agent.save_vals('trained_agent_state_vals')
