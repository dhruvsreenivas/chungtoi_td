from game import ChungToi
from models import Agent

game = ChungToi()
agent = Agent(gamma=0.99, eps=0.85, alpha=0.0012)
adversary_agent = Agent(gamma=0.99, eps=0.15, alpha=0.0012)


def play_game(game):
    player = agent if game.curr_player == 1 else adversary_agent
    while not game.is_terminal()[0]:
        action = player.select_action(game)
        player.act(action)
        player.update_value_fn()
        player = adversary_agent if player == agent else agent


def play_games(num_games):
    for _ in range(num_games):
        play_game(game)
