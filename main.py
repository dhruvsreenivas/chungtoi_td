from game import ChungToi
from agents import QLearningAgent
import numpy as np


def play_game(game, agent, adversary_agent):
    game.reset()
    agent_prev_state = game.get_state()
    agent_prev_action = None
    adv_prev_state = None
    adv_prev_action = None
    while True:
        curr_state = game.get_state()
        # print(curr_state)
        # print(game.get_action_set(curr_state))

        # player 1 moves
        action = agent.select_action()
        next_state, reward_1 = game.act(curr_state, action)
        # print('player 1 moved')
        # game.print_game_state()
        # print('\n\n\n')

        # update previous state, action for agent
        agent_prev_state = curr_state
        agent_prev_action = action

        # player 2 updates
        if adv_prev_state and adv_prev_action:
            adversary_agent.update(
                adv_prev_state, adv_prev_action, -1 * reward_1, next_state)

        # if player 1 finishes the game it has to update its Q table
        if game.is_terminal()[0]:
            agent.update(agent_prev_state, agent_prev_action,
                         reward_1, next_state)
            break

        # player 2 makes a move now
        curr_state = game.get_state()
        # print(curr_state)
        # print(game.get_action_set(curr_state))

        action = adversary_agent.select_action()
        next_state, reward_2 = game.act(curr_state, action)
        # print('player 2 moved')
        # game.print_game_state()
        # print('\n\n\n')

        # update previous state, action for adversary
        adv_prev_state = curr_state
        adv_prev_action = action

        # player 1 updates
        if agent_prev_state and agent_prev_action:
            agent.update(agent_prev_state, agent_prev_action,
                         -1 * reward_2, next_state)

        # if game is over after player 2 move you have to update player 2's Q values
        if game.is_terminal()[0]:
            state = game.get_state()
            adversary_agent.update(
                adv_prev_state, adv_prev_action, reward_2, state)
            break

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
    NUM_GAMES = 50
    game = ChungToi()
    agent = QLearningAgent(gamma=0.99, eps=0.85, alpha=0.01, game=game)
    adversary_agent = QLearningAgent(
        gamma=0.99, eps=0.85, alpha=0.01, game=game)

    p1, p2 = play_games(NUM_GAMES, game, agent, adversary_agent)
    print(p1, p2)
    print(len(agent.q_values))
    values = list(agent.q_values.values())
    print(len(values) - values.count(0))
    print(np.max(values))

    adv_values = list(adversary_agent.q_values.values())
    print(len(adv_values) - adv_values.count(0))
    print(np.max(values))
