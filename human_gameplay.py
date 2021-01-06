from agents import ValueAgent
import numpy as np
from game import ChungToi


def human_vs_machine(game, agent):
    # human plays against the MACHINE
    first = str(input('Do you want to go first? Y/N'))
    if first == 'Y':
        while not game.is_terminal()[0]:
            action = tuple(input('Take an action in the game. An action is coded as (prev, next, orientation) where previous is the previous destination of token, next is the next destination, and orientation is the orientation wanted.'))
            if action not in game.get_action_set(game.get_state()):
                print('You cannot play this action--please choose another one.')
