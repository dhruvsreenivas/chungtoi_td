from game import ChungToi
from models import Agent


def play_game(game, agent, adversary_agent):
    player = agent if game.curr_player == 1 else adversary_agent
    while not game.is_terminal()[0]:
        curr_state = game.get_state()
        action = player.select_action(game)
        next_state, reward = game.act(action)
        player.update(curr_state, action, reward, next_state)
        if player == agent:
            player = adversary_agent
        else:
            player = agent


def play_games(num_games, game, agent, adversary_agent):
    for _ in range(num_games):
        play_game(game, agent, adversary_agent)


if __name__ == '__main__':
    NUM_GAMES = 200
    game = ChungToi()
    agent = Agent(gamma=0.99, eps=0.85, alpha=0.001, game=game)
    adversary_agent = Agent(gamma=0.99, eps=0.15, alpha=0.001, game=game)

    play_games(NUM_GAMES, game, agent, adversary_agent)
