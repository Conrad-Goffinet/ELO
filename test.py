import unittest
from Game_and_Player import *

class TestPlayer(unittest.TestCase):
    
    def test_init(self):
        P1 = Player('Conrad')
        self.assertEqual(P1.name, 'Conrad')
        self.assertEqual(P1.get_pelo(), 500)

    def test_pelo_update(self):
        P1 = Player('Conrad')
        P1.update_pelo(5, True, 500)
        self.assertEqual(P1.get_pelo(), 512.5)
        P1.update_pelo(8, True, 650)
        self.assertEqual(round(P1.get_pelo(),2), 540.03)
        P1.update_pelo(2, False, 500)
        self.assertEqual(round(P1.get_pelo(), 2), 517.73)

    def test_pelo_history(self):
        P1 = Player('Conrad')
        P1.update_pelo(5, True, 500)
        P1.update_pelo(8, True, 650)
        P1.update_pelo(2, False, 500)
        self.assertEqual([round(x,2) for x in P1.pelo_history] , [500, 512.5, 540.03, 517.73])

class TestGame(unittest.TestCase):

    def test_init(self):
        P1 = Player('Sweidman')
        P2 = Player('Conrad')
        P3 = Player('Ally')
        P4 = Player('Adriana')
        G = Game(((P1, 4),(P2, 6)), ((P3, 2), (P4, 4)))
        game_stats = {'Sweidman':(4, True, 500, 6), 'Conrad':(6, True, 500, 6),
                      'Ally':(2, False, 500, 10), 'Adriana':(4, False, 500, 10)

        }
        self.assertEqual(G.player_stats, game_stats)

if __name__ == '__main__':
    unittest.main()