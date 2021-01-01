from game import ChungToi
from agents import ValueAgent
import numpy as np


def play_game(game, agent, adversary_agent):
    game.reset()
    print("start game for sure")
    while not game.is_terminal()[0]:
        # player 1 moves first
        print("player " + str(game.curr_player) + ": will move now")
        if game.curr_player == 1:
            s = game.get_state()
            agent_a = agent.select_action(game)
            n_s, _ = game.act(s, agent_a)
            # update player 1 state val table
            agent.update(s, n_s)
        else:
            # now time for player 2 to move
            s = game.get_state()
            adv_a = adversary_agent.select_action(game)
            n_s, _ = game.act(s, adv_a)
            # update player 1 state val table
            adversary_agent.update(s, n_s)

    return game.is_terminal()[1]


def play_games(num_games, game, agent, adversary_agent):
    player_1_wins = 0
    player_2_wins = 0
    for _ in range(num_games):
        winner = play_game(game, agent, adversary_agent)
        if winner == 1:
            player_1_wins += 1
        else:
            player_2_wins += 1

    return player_1_wins, player_2_wins


if __name__ == '__main__':
    NUM_GAMES = 200
    print("1")
    game = ChungToi()
    print("2")
    agent = ValueAgent(alpha=0.01, player_num=1, eps=0.85)
    print("3")
    adversary_agent = ValueAgent(alpha=0.01, player_num=-1, eps=0.85)
    print("starting gameplay...")
    p1, p2 = play_games(NUM_GAMES, game, agent, adversary_agent)
    print(p1, p2)
