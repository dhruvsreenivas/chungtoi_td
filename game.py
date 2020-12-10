class ChungToi:
    def __init__(self):
        self.positions = [0] * 9
        self.orientations = [0] * 9
        self.curr_player = [1, 0]
        self.num_moves_taken = 0

    def reset(self):
        self.positions = [0] * 9
        self.orientations = [0] * 9
        self.curr_player = [1, 0]
        self.num_moves_taken = 0

    def get_state(self):
        return self.positions + self.orientations + self.curr_player

    def get_action_set(self):
        curr_player = 1
        if self.curr_player[1] == 1:
            curr_player = -1

        # if we don't have all the pieces on the board, we must put all of our pieces on board (put on empty space)
        # every action can be encoded as (prev_pos, next_pos, orientation)
        if self.positions.count(curr_player) < 3:
            action_set = []
            for i in range(9):
                if self.positions[i] == 0:
                    action_set.append((None, i, 1))
                    action_set.append((None, i, -1))

            return action_set
        else:
            action_set = []
            locations = []
            for i in range(9):
                if self.positions[i] == self.curr_player:
                    locations.append((i, self.orientations[i]))

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
                            if self.positions[neighbor] == 0:
                                action_set.append((l, neighbor, 1))
                                action_set.append((l, neighbor, -1))
                            else:
                                if neighbor == l+1:
                                    jump_neighbor = l+2
                                    if self.positions[jump_neighbor] == 0:
                                        action_set.append((l, l+2, 1))
                                        action_set.append((l, l+2, -1))
                    elif l % 3 == 2:
                        # right of the row
                        neighbors = [l-1]
                        if l == 2 or l == 8:
                            neighbors.append(5)
                        else:
                            neighbors += [2, 8]
                        for neighbor in neighbors:
                            if self.positions[neighbor] == 0:
                                action_set.append((l, neighbor, 1))
                                action_set.append((l, neighbor, -1))
                            else:
                                if neighbor == l-1:
                                    jump_neighbor = l-2
                                    if self.positions[jump_neighbor] == 0:
                                        action_set.append((l, l-2, 1))
                                        action_set.append((l, l-2, -1))
                    else:
                        neighbors = [l+1, l-1]
                        if l == 1 or l == 7:
                            neighbors.append(4)
                        else:
                            neighbors += [1, 7]
                        for neighbor in neighbors:
                            if self.positions[neighbor] == 0:
                                action_set.append((l, neighbor, 1))
                                action_set.append((l, neighbor, -1))
                            else:
                                # no jumping capability if l = 4
                                if l == 1 and neighbor == 4:
                                    jump_neighbor = 7
                                    if self.positions[jump_neighbor] == 0:
                                        action_set.append(
                                            (l, jump_neighbor, 1))
                                        action_set.append(
                                            (l, jump_neighbor, -1))
                                elif l == 7 and neighbor == 4:
                                    jump_neighbor = 1
                                    if self.positions[jump_neighbor] == 0:
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
                            if self.positions[diag_neighbor] == 0:
                                action_set.append((l, diag_neighbor, 1))
                                action_set.append((l, diag_neighbor, -1))
                    elif l == 0 or l == 2 or l == 6 or l == 8:
                        # corners, we can jump
                        diag_neighbor == 4
                        if self.positions[diag_neighbor] == 0:
                            action_set.append((l, diag_neighbor, 1))
                            action_set.append((l, diag_neighbor, -1))
                        else:
                            jump_diag = 8 - l
                            if self.positions[jump_diag] == 0:
                                action_set.append((l, jump_diag, 1))
                                action_set.append((l, jump_diag, -1))
                    elif l % 2 == 1:
                        # middle of rows, can't jump
                        neighbors == None
                        if l == 3 or l == 5:
                            neighbors == [1, 7]
                        else:
                            neighbors == [3, 5]

                        for diag_neighbor in neighbors:
                            if self.positions[diag_neighbor] == 0:
                                action_set.append((l, diag_neighbor, 1))
                                action_set.append((l, diag_neighbor, -1))

            return action_set

    def next_state(self, action):
        curr_player = 1
        if self.curr_player[1] == 1:
            curr_player = -1

        prev, dest, o = action

        positions = self.positions
        orientations = self.orientations
        curr_player_lst = self.curr_player

        if prev:
            positions[prev] = 0
            orientations[prev] = 0

        positions[dest] = curr_player
        orientations[dest] = o

        # change player
        if self.curr_player == [0, 1]:
            curr_player_lst = [1, 0]
        else:
            curr_player_lst = [0, 1]

        return positions + orientations + curr_player_lst

    def act(self, action):
        assert action in self.get_action_set()

        curr_player = 1
        if self.curr_player[1] == 1:
            curr_player = -1

        prev, dest, o = action

        if prev:
            self.positions[prev] = 0
            self.orientations[prev] = 0

        self.positions[dest] = curr_player
        self.orientations[dest] = o

        # change player
        if self.curr_player == [0, 1]:
            self.curr_player = [1, 0]
        else:
            self.curr_player = [0, 1]

        self.num_moves_taken += 1

    # now we have the game state made, as well as the transition dynamics

    # in order to determine a reward function for this game, it is important to consider terminal states

    # this function determines if the game has ended or not, and outputs the winner if it has ended
    def is_terminal(self):
        for i in range(3):
            # check rows
            if self.positions[3 * i] == self.positions[3 * i + 1] and self.positions[i+1] == self.positions[3 * i + 2] and self.positions[3 * i] != 0:
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

    def reward(self):
        # program should output 1 if current player won in terminal state, -1 if current player lost in terminal state, and 0 otherwise
        curr_player = 1
        if self.curr_player[1] == 1:
            curr_player = -1

        end, winner = self.is_terminal()
        if end:
            if winner == curr_player:
                return 1
            else:
                return -1
        return 0
