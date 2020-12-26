from termcolor import colored
import pyglet
# from pyglet import shapes


class ChungToi:
    def __init__(self):
        self.positions = [0] * 9
        self.orientations = [0] * 9
        self.curr_player = 1
        self.num_moves_taken = 0

    def reset(self):
        self.positions = [0] * 9
        self.orientations = [0] * 9
        self.curr_player = 1
        self.num_moves_taken = 0

    def get_state(self):
        return self.positions + self.orientations

    def get_action_set(self, state):
        positions = state[:9]
        orientations = state[9:]
        # if we don't have a state, replace state (positions, orientations) with self.positions + self.orientations (in case we need to switch back later)

        # if game has already ended, there are no actions to be done
        if self.is_terminal()[0]:
            return []

        # if we don't have all the pieces on the board, we must put all of our pieces on board (put on empty space)
        # every action can be encoded as (prev_pos, next_pos, orientation)
        if positions.count(self.curr_player) < 3:
            action_set = []
            for i in range(9):
                if positions[i] == 0:
                    action_set.append((None, i, 1))
                    action_set.append((None, i, -1))

            return action_set
        else:
            action_set = []
            locations = []
            for i in range(9):
                if positions[i] == self.curr_player:
                    locations.append((i, orientations[i]))

            # can change orientation in place and be considered a move
            for l, o in locations:
                action_set.append((l, l, -1 * o))

            # check horizontal ([0, 1, 2], [3, 4, 5], [6, 7, 8])
            for l, o in locations:
                # cardinal orientation is required
                if o == 1:
                    if l % 3 == 0:
                        # left of the row
                        neighbors = [l+1]
                        if l == 0 or l == 6:
                            neighbors.append(3)
                        else:
                            neighbors += [0, 6]
                        for neighbor in neighbors:
                            if positions[neighbor] == 0:
                                action_set.append((l, neighbor, 1))
                                action_set.append((l, neighbor, -1))
                            else:
                                if neighbor == l+1:
                                    jump_neighbor = l+2
                                    if positions[jump_neighbor] == 0:
                                        # is a horizontal jump
                                        action_set.append((l, l+2, 1))
                                        action_set.append((l, l+2, -1))
                                elif l == 0 and neighbor == 3:
                                    jump_neighbor = 6
                                    if positions[jump_neighbor] == 0:
                                        # is a vertical jump
                                        action_set.append(
                                            (l, jump_neighbor, 1))
                                        action_set.append(
                                            (l, jump_neighbor, -1))
                                elif l == 6 and neighbor == 3:
                                    jump_neighbor = 0
                                    if positions[jump_neighbor] == 0:
                                        # is a horizontal jump
                                        action_set.append(
                                            (l, jump_neighbor, 1))
                                        action_set.append(
                                            (l, jump_neighbor, -1))
                    elif l % 3 == 2:
                        # right of the row
                        neighbors = [l-1]
                        if l == 2 or l == 8:
                            neighbors.append(5)
                        else:
                            neighbors += [2, 8]
                        for neighbor in neighbors:
                            if positions[neighbor] == 0:
                                action_set.append((l, neighbor, 1))
                                action_set.append((l, neighbor, -1))
                            else:
                                if neighbor == l-1:
                                    jump_neighbor = l-2
                                    if positions[jump_neighbor] == 0:
                                        # also a horizontal jump
                                        action_set.append((l, l-2, 1))
                                        action_set.append((l, l-2, -1))
                                elif l == 2 and neighbor == 5:
                                    jump_neighbor = 8
                                    if positions[jump_neighbor] == 0:
                                        # is a vertical jump
                                        action_set.append(
                                            (l, jump_neighbor, 1))
                                        action_set.append(
                                            (l, jump_neighbor, -1))
                                elif l == 8 and neighbor == 5:
                                    jump_neighbor = 2
                                    if positions[jump_neighbor] == 0:
                                        # is a horizontal jump
                                        action_set.append(
                                            (l, jump_neighbor, 1))
                                        action_set.append(
                                            (l, jump_neighbor, -1))
                    else:
                        neighbors = [l+1, l-1]
                        if l == 1 or l == 7:
                            neighbors.append(4)
                        else:
                            neighbors += [1, 7]
                        for neighbor in neighbors:
                            if positions[neighbor] == 0:
                                action_set.append((l, neighbor, 1))
                                action_set.append((l, neighbor, -1))
                            else:
                                # no jumping capability if l = 4
                                if l == 1 and neighbor == 4:
                                    jump_neighbor = 7
                                    if positions[jump_neighbor] == 0:
                                        action_set.append(
                                            (l, jump_neighbor, 1))
                                        action_set.append(
                                            (l, jump_neighbor, -1))
                                elif l == 7 and neighbor == 4:
                                    jump_neighbor = 1
                                    if positions[jump_neighbor] == 0:
                                        action_set.append(
                                            (l, jump_neighbor, 1))
                                        action_set.append(
                                            (l, jump_neighbor, -1))
                else:
                    # now we look at diagonals
                    if l == 4:
                        # right in middle, can't jump
                        diag_neighbors = [0, 2, 6, 8]
                        for diag_neighbor in diag_neighbors:
                            if positions[diag_neighbor] == 0:
                                action_set.append((l, diag_neighbor, 1))
                                action_set.append((l, diag_neighbor, -1))
                    elif l == 0 or l == 2 or l == 6 or l == 8:
                        # corners, we can jump
                        d_neighbor = 4
                        if positions[d_neighbor] == 0:
                            action_set.append((l, d_neighbor, 1))
                            action_set.append((l, d_neighbor, -1))
                        else:
                            jump_diag = 8 - l
                            if positions[jump_diag] == 0:
                                action_set.append((l, jump_diag, 1))
                                action_set.append((l, jump_diag, -1))
                    elif l % 2 == 1:
                        # middle of rows, can't jump
                        neighbors == None
                        if l == 3 or l == 5:
                            neighbors = [1, 7]
                        else:
                            neighbors = [3, 5]

                        for diag_neighbor in neighbors:
                            if positions[diag_neighbor] == 0:
                                action_set.append((l, diag_neighbor, 1))
                                action_set.append((l, diag_neighbor, -1))

            return action_set

    def act(self, state, action):
        assert action in self.get_action_set(state)

        prev, dest, o = action

        if prev != None:
            self.positions[prev] = 0
            self.orientations[prev] = 0

        self.positions[dest] = self.curr_player
        self.orientations[dest] = o
        self.num_moves_taken += 1

        # check winning state
        end, winner = self.is_terminal()
        if end:
            if winner == self.curr_player:
                if self.curr_player == 1:
                    print('Player ' + str(self.curr_player) + ' won!')
                else:
                    print('Other player won!')
                reward = 1
            else:
                reward = -1
        else:
            reward = 0

        # after that we change current player
        self.curr_player *= -1

        return self.get_state(), reward

    # now we have the game state made, as well as the transition dynamics

    # in order to determine a reward function for this game, it is important to consider terminal states

    # this function determines if the game has ended or not, and outputs the winner if it has ended
    def is_terminal(self):
        for i in range(3):
            # check rows
            if self.positions[3 * i] == self.positions[3 * i + 1] and self.positions[3 * i + 1] == self.positions[3 * i + 2] and self.positions[3 * i] != 0:
                return (True, self.positions[3 * i])
            elif self.positions[i] == self.positions[i + 3] and self.positions[i+3] == self.positions[i+6] and self.positions[i] != 0:
                # columns show winner
                return (True, self.positions[i])

        # diagonal check
        if self.positions[0] == self.positions[4] and self.positions[4] == self.positions[8] and self.positions[0] != 0:
            return (True, self.positions[0])
        elif self.positions[2] == self.positions[4] and self.positions[4] == self.positions[6] and self.positions[2] != 0:
            return (True, self.positions[2])

        return (False, None)

    # Finally, we need a way to visualize the game
    def print_game_state(self):
        player_1_color = 'red'
        player_2_color = 'blue'
        for row in range(3):
            row_str = ''
            for j in range(3):
                if self.positions[3 * row + j] == 0:
                    if j == 2:
                        row_str += ' '
                    else:
                        row_str += ' | '
                elif self.positions[3 * row + j] == 1:
                    if j == 2:
                        if self.orientations[3 * row + j] == 1:
                            # coordinate aligned
                            row_str += (colored('+', player_1_color))
                        else:
                            row_str += (colored('X', player_1_color))
                    else:
                        if self.orientations[3 * row + j] == 1:
                            row_str += (colored('+', player_1_color) + ' | ')
                        else:
                            row_str += (colored('X', player_1_color) + ' | ')
                else:
                    if j == 2:
                        if self.orientations[3 * row + j] == 1:
                            # coordinate aligned
                            row_str += (colored('+', player_2_color))
                        else:
                            row_str += (colored('X', player_2_color))
                    else:
                        if self.orientations[3 * row + j] == 1:
                            row_str += (colored('+', player_2_color) + ' | ')
                        else:
                            row_str += (colored('X', player_2_color) + ' | ')

            if row < 2:
                print(row_str)
                print('--------')
            else:
                print(row_str)

    # def render(self):
    #     window = pyglet.window.Window(600, 600, 'Chung Toi')
    #     window.set_minimum_size(300, 300)
    #     batch = pyglet.graphics.Batch()

    #     # define all shapes that we want to draw in
    #     # the normal horizontal and vertical lines for the game
    #     horiz_line_1 = shapes.Line(
    #         50, 150, 550, 150, width=3, color=(0, 0, 0), batch=batch)
    #     horiz_line_2 = shapes.Line(
    #         50, 350, 550, 350, width=3, color=(0, 0, 0), batch=batch)
    #     vert_line_1 = shapes.Line(
    #         150, 50, 150, 550, width=3, color=(0, 0, 0), batch=batch)
    #     vert_line_2 = shapes.Line(
    #         350, 50, 350, 550, width=3, color=(0, 0, 0), batch=batch)

    #     radius = 75
    #     centers_dict = {}
    #     centers_dict[0] = [50, 450]
    #     centers_dict[1] = [250, 450]
    #     centers_dict[2] = [450, 450]
    #     centers_dict[3] = [50, 250]
    #     centers_dict[4] = [250, 250]
    #     centers_dict[5] = [450, 250]
    #     centers_dict[6] = [50, 50]
    #     centers_dict[7] = [250, 50]
    #     centers_dict[8] = [450, 50]

    #     for idx in range(9):
    #         center = centers_dict[idx]
    #         if self.positions[idx] == 1:
    #             # red player
    #             red = (255, 0, 0)
    #             # centers in order are (50, 450), (250, 450), (450, 450), (50, 250), (250, 250), (450, 250), (50, 50), (250, 50), (450, 50)
    #             # rough estimate, subject to change
    #             if self.orientations[idx] == 1:
    #                 line1 = shapes.Line(
    #                     center[0], center[1] - radius, center[0], center[1] + radius, width=3, color=red, batch=batch)
    #                 line2 = shapes.Line(
    #                     center[0] - radius, center[1], center[0] + radius, center[1], width=3, color=red, batch=batch)
    #             else:
    #                 line1 = shapes.Line(
    #                     center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius, width=3, color=red, batch=batch)
    #                 line2 = shapes.Line(
    #                     center[0] - radius, center[1] + radius, center[0] + radius, center[1] - radius, width=3, color=red, batch=batch)

    #         else:
    #             blue = (0, 0, 255)
    #             if self.orientations[idx] == 1:
    #                 line1 = shapes.Line(
    #                     center[0], center[1] - radius, center[0], center[1] + radius, width=3, color=blue, batch=batch)
    #                 line2 = shapes.Line(
    #                     center[0] - radius, center[1], center[0] + radius, center[1], width=3, color=blue, batch=batch)
    #             else:
    #                 line1 = shapes.Line(
    #                     center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius, width=3, color=blue, batch=batch)
    #                 line2 = shapes.Line(
    #                     center[0] - radius, center[1] + radius, center[0] + radius, center[1] - radius, width=3, color=blue, batch=batch)

    #         window.clear()
    #         batch.draw()
