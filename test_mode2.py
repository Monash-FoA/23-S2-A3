from unittest import TestCase
from ed_utils.timeout import timeout
from ed_utils.decorators import number, visibility
from random_gen import RandomGen

from island import Island
from mode2 import Mode2Navigator

class Mode2Tests(TestCase):

    def load_basic(self):
        self.a = Island("A", 400, 100)
        self.b = Island("B", 300, 150)
        self.c = Island("C", 100, 5)
        self.d = Island("D", 350, 90)
        self.e = Island("E", 300, 100)
        self.islands = [
            self.a, self.b, self.c, self.d, self.e
        ]

    @number("2.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_day(self):
        self.load_basic()

        # Used later
        cur_marines = {
            island.name: island.marines
            for island in self.islands
        }
        cur_money = {
            island.name: island.money
            for island in self.islands
        }

        nav = Mode2Navigator(8)
        nav.add_islands(self.islands)
        results = nav.simulate_day(100)
        # The first pirate makes 400 gold by going to Island A and sending 100 their crew.
        # Final score: 400
        # The second pirate makes 350 gold by going to Island D and sending 90 of their crew.
        # Final score: 20 + 350 = 370
        # The third pirate makes 300 gold by going to Island E and sending 100 of their crew.
        # Final score: 300
        # The fourth pirate makes 100 gold by going to Island C and sending 5 of their crew.
        # Final score: 190 + 100 = 290
        # The fifth, sixth, seventh, eighth pirate can do a number of different things but the best score they end up with is 200.
        expected_scores = [400, 370, 300, 290, 200, 200, 200, 200]
        for (island, sent_crew), expected in zip(results, expected_scores):
            if island is None:
                self.assertEqual(2 * 100, expected)
                continue
            money = cur_money[island.name]
            marines = cur_marines[island.name]
            if marines == 0:
                received = money
            else:
                received = min(money, money * sent_crew / marines)
            # Update Island
            cur_money[island.name] = money - received
            cur_marines[island.name] = max(0, marines - sent_crew)
            # Score
            score = 2 * (100 - sent_crew) + received
            self.assertEqual(score, expected)

    @number("2.2")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_add_again(self):
        self.load_basic()

        # Used later
        cur_marines = {
            island.name: island.marines
            for island in self.islands
        }
        cur_money = {
            island.name: island.money
            for island in self.islands
        }

        nav = Mode2Navigator(3)
        nav.add_islands(self.islands)
        results_1 = nav.simulate_day(100)
        # Same first 3 decisions as test 2.1
        expected_1 = [400, 370, 300]
        for (island, sent_crew), expected in zip(results_1, expected_1):
            if island is None:
                self.assertEqual(2 * 100, expected)
                continue
            money = cur_money[island.name]
            marines = cur_marines[island.name]
            if marines == 0:
                received = money
            else:
                received = min(money, money * sent_crew / marines)
            # Update Island
            cur_money[island.name] = money - received
            cur_marines[island.name] = max(0, marines - sent_crew)
            # Score
            score = 2 * (100 - sent_crew) + received
            self.assertEqual(score, expected)
        nav.add_islands([Island("F", 900, 150)])
        cur_marines["F"] = 150
        cur_money["F"] = 900
        results_2 = nav.simulate_day(100)
        # The first 2 pirates on this day can plunder island F, after which the same decisions as in test 2.1 continue
        expected_2 = [600, 400, 290]
        for (island, sent_crew), expected in zip(results_2, expected_2):
            if island is None:
                self.assertEqual(2 * 100, expected)
                continue
            money = cur_money[island.name]
            marines = cur_marines[island.name]
            if marines == 0:
                received = money
            else:
                received = min(money, money * sent_crew / marines)
            # Update Island
            cur_money[island.name] = money - received
            cur_marines[island.name] = max(0, marines - sent_crew)
            # Score
            score = 2 * (100 - sent_crew) + received
            self.assertEqual(score, expected)
