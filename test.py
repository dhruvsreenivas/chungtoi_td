import unittest
import game


class TestChungToi(unittest.TestCase):
    def test_one_move(self):
        ct = game.ChungToi()
        ct.act(ct.get_state(), (None, 0, 1))
        terminal, _ = ct.is_terminal()
        self.assertFalse(terminal)

    def test_legal_moves(self):
        ct = game.ChungToi()
        ct.act(ct.get_state(), (None, 0, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 2, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 3, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 4, -1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 5, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 6, 1))
        terminal, winner = ct.is_terminal()
        self.assertTrue(terminal)
        self.assertEqual(winner, -1)

    def test_vertical_jump(self):
        ct = game.ChungToi()
        ct.act(ct.get_state(), (None, 0, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 2, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 3, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 4, -1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 5, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 7, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (0, 6, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (2, 1, 1))
        terminal, winner = ct.is_terminal()
        self.assertTrue(terminal)
        self.assertEqual(winner, -1)

    def test_diagonal_jump(self):
        ct = game.ChungToi()
        ct.act(ct.get_state(), (None, 0, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 2, -1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 3, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 4, -1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 5, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 7, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (0, 1, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (2, 6, -1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (5, 2, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (4, 8, 1))
        terminal, winner = ct.is_terminal()
        self.assertTrue(terminal)
        self.assertEqual(winner, -1)

    def test_orientation_switch(self):
        ct = game.ChungToi()
        ct.act(ct.get_state(), (None, 0, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 2, -1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 3, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 4, -1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 5, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (None, 7, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (0, 1, 1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (2, 6, -1))
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (5, 5, -1))  # orientation shift
        terminal, winner = ct.is_terminal()
        self.assertFalse(terminal)
        ct.act(ct.get_state(), (4, 8, 1))
        terminal, winner = ct.is_terminal()
        self.assertTrue(terminal)
        self.assertEqual(winner, -1)

    def test_illegal_action_set_move(self):
        ct = game.ChungToi()
        ct.act(ct.get_state(), (None, 0, 1))
        try:
            ct.act(ct.get_state(), (None, 0, 1))
        except AssertionError:
            pass
        else:
            self.fail('Did not see AssertionError')

    def test_multiple_moves(self):
        ct = game.ChungToi()
        ct.act(ct.get_state(), (None, 0, 1))
        ct.act(ct.get_state(), (None, 1, -1))
        ct.act(ct.get_state(), (None, 4, 1))
        try:
            ct.act(ct.get_state(), (None, 0, -1))
        except AssertionError:
            pass
        else:
            self.fail('Did not see AssertionError')

    def test_next_state_first_lookahead(self):
        ct = game.ChungToi()
        key = ct.next_state(ct.get_state(), (None, 0, 1))
        self.assertEqual(key, [1, 0, 0, 0, 0, 0, 0, 0,
                               0, 1, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_next_state_move_lookahead(self):
        ct = game.ChungToi()
        ct.act(ct.get_state(), (None, 0, 1))
        key = ct.next_state(ct.get_state(), (None, 2, -1))
        self.assertEqual(key, [1, 0, -1, 0, 0, 0, 0, 0,
                               0, 1, 0, -1, 0, 0, 0, 0, 0, 0])

    def test_next_state_two_move_lookahead(self):
        ct = game.ChungToi()
        ct.act(ct.get_state(), (None, 0, 1))
        ct.act(ct.get_state(), (None, 2, -1))
        key = ct.next_state(ct.get_state(), (None, 4, -1))
        self.assertEqual(key, [1, 0, -1, 0, 1, 0, 0, 0,
                               0, 1, 0, -1, 0, -1, 0, 0, 0, 0])

    def test_next_state_key_error(self):
        ct = game.ChungToi()
        ct.act(ct.get_state(), (None, 5, 1))
        ct.act(ct.get_state(), (None, 0, -1))
        key = ct.next_state(ct.get_state(), (None, 1, 1))
        self.assertEqual(key, [-1, 1, 0, 0, 0, 1, 0, 0,
                               0, -1, 1, 0, 0, 0, 1, 0, 0, 0])


if __name__ == '__main__':
    unittest.main()
