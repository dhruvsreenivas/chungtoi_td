import random


class ChungToi:
    def __init__(self):
        # board description (c, o) in each cell indicates orientation and color of thing in cell (-1 if player 1, 1 if player 2, 0 if no one is there)
        self.board = [([(0, 0)] * 3) for _ in range(3)]
        self.colors = [-1, 1]
        # -1 means diagonally, 1 means aligned with board axes
        self.orientations = [0, 1]

        # GAME STATE STUFF

        # this keeps track of the number of pieces on the board
        # only useful in the beginning when not all pieces are in play
        self.color_pieces_on_board = [0, 0]

        # keeps track of current player
        self.curr_player = -1
        self.player_positions = [[], []]

    def action_set(self):
        # if a player hasn't played all their pieces yet they must put a new piece in play
        idx = 0 if self.curr_player == -1 else 1

        if self.color_pieces_on_board[idx] < 3:
            action_space = []
            # has to put the piece somewhere on the board that isn't taken
            # first part of the tuple is previous location, second part is destination
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == (0, 0):
                        action_space.append((None, ((i, j), -1)))
                        action_space.append((None, ((i, j), 1)))

            return action_space
        else:
            # all pieces are on board, there are only two courses of action
            # either move horizontally, move diagonally, or jump

            for r, c, o in self.player_positions[idx]:
                if o == 1:
                    # horizontal movement/jump
                    action_space = []
                    neighbors = [(r-1, c), (r, c-1), (r+1, c), (r, c+1)]
                    for n in neighbors:
                        if 0 <= n[0] and n[0] <= 2 and 0 <= n[1] and n[1] <= 2 and self.board[n[0]][n[1]] == (0, 0):
                            # can move horizontally there, shouldn't run into out of bounds issues i think
                            action_space.append(((r, c), (n, 1)))
                            action_space.append(((r, c), (n, -1)))
                        else:
                            # have to jump horizontally
                            o_n = ((r + 2 * (n[0] - r), c + 2 * (n[1] - c)))
                            if 0 <= o_n[0] and o_n[0] <= 2 and 0 <= o_n[1] and o_n[1] <= 2 and self.board[o_n[0]][o_n[1]] == (0, 0):
                                # this shouldn't run into any out of bounds issues
                                action_space.append(((r, c), (o_n, 1)))
                                action_space.append(((r, c), (o_n, -1)))

                    return action_space
                else:
                    action_space = []
                    # diagonal
                    neighbors = [(r-1, c-1), (r+1, c+1),
                                 (r-1, c+1), (r-1, c-1)]
                    for n in neighbors:
                        if 0 <= n[0] and n[0] <= 2 and 0 <= n[1] and n[1] <= 2 and self.board[n[0]][n[1]] == (0, 0):
                            action_space.append(((r, c), (n, 1)))
                            action_space.append(((r, c), (n, -1)))
                        else:
                            o_n = ((r + 2 * (n[0] - r), c + 2 * (n[1] - c)))
                            if 0 <= o_n[0] and o_n[0] <= 2 and 0 <= o_n[1] and o_n[1] <= 2 and self.board[o_n[0]][o_n[1]] == (0, 0):
                                action_space.append(((r, c), (o_n, 1)))
                                action_space.append(((r, c), (o_n, -1)))

                    return action_space

    def act(self, action):
        # action: (current_loc, (destination, orientation))
        # assume here that action is in the game state's action_space (we assert it here)
        assert action in self.action_set()

        current_loc, dest_orient = action

        idx = 0 if self.curr_player == -1 else 1

        # clear out old player position
        self.board[current_loc[0]][current_loc[1]] = (0, 0)
        for tup in self.player_positions[idx]:
            if tup[0] == current_loc[0] and tup[1] == current_loc[1]:
                self.player_positions.remove(tup)
                break

        # put token at destination with new orientation
        self.board[dest_orient[0][0]][dest_orient[0][1]] = (
            self.curr_player, dest_orient[1])
        self.player_positions.append(
            (dest_orient[0][0], dest_orient[0][1], dest_orient[1]))

        # change player
        self.curr_player *= -1

    # At this point (if everything works correctly), we have the game setup, the action set for each given state, and the method for executing a particular action

    # one thing we can do is identify the terminal states here in this game, which is when the game officially ends
    def is_terminal(self):
        board = self.board
        # we just check that either a row, a col or a diagonal has been filled up and all colors are the same
        for i in range(3):
            if board[i][0][0] == board[i][1][0] and board[i][1][0] == board[i][2][0] and board[i][0][0] != 0:
                return (True, board[i][0][0])
        for i in range(3):
            if board[0][i][0] == board[1][i][0] and board[1][i][0] == board[2][i][0] and board[0][i][0] != 0:
                return (True, board[0][i][0])
        if board[0][0][0] == board[1][1][0] and board[0][0][0] == board[2][2][0] and board[0][0][0] != 0:
            return (True, board[0][0][0])
        elif board[0][2][0] == board[1][1][0] and board[0][2][0] == board[2][0][0] and board[0][2][0] != 0:
            return (True, board[2][0][0])
        return False

    # with this we can define a reward function for the game state, which is 0 if the game isn't done, 1 if the game is won by the state's current player, and -1 otherwise
    def reward(self):
        s = self.is_terminal()
        if s[0]:
            winner = s[1]
            if winner == self.curr_player:
                return 1
            else:
                return -1
        return 0
