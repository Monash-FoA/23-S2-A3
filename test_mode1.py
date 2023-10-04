from unittest import TestCase
from ed_utils.timeout import timeout
from ed_utils.decorators import number, visibility
from random_gen import RandomGen

from island import Island
from mode1 import Mode1Navigator

class Mode1Tests(TestCase):

    def load_basic(self):
        self.a = Island("A", 400, 100)
        self.b = Island("B", 300, 150)
        self.c = Island("C", 100, 5)
        self.d = Island("D", 350, 90)
        self.e = Island("E", 300, 100)
        # Create deepcopies of the islands
        self.islands = [
            Island(self.a.name, self.a.money, self.a.marines),
            Island(self.b.name, self.b.money, self.b.marines),
            Island(self.c.name, self.c.money, self.c.marines),
            Island(self.d.name, self.d.money, self.d.marines),
            Island(self.e.name, self.e.money, self.e.marines),
        ]

    def check_solution(self, islands, starting_crew, solution, optimal):
        current_money = 0
        current_crew = starting_crew
        for island, crew_sent in solution:
            self.assertGreaterEqual(crew_sent, 0)
            # This assertIn is written so that we allow copies with the same properties to be considered equal.
            self.assertIn((island.name, island.money, island.marines), [(i.name, i.money, i.marines) for i in islands])
            current_money += min(island.money * crew_sent / island.marines, island.money)
            current_crew -= crew_sent
            self.assertGreaterEqual(current_crew, 0)
        self.assertFalse(current_money < optimal, "Your island selection is suboptimal!")
        if current_money > optimal:
            raise ValueError("ERROR! You somehow made more money than the intended solution")

    @number("1.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic(self):
        self.load_basic()
        nav = Mode1Navigator(self.islands, 200)
        selected = nav.select_islands()
        expected_money = 865
        # ^ This can be achieved with ^
        # A: 100 Crew
        # B: 0 Crew
        # C: 5 Crew
        # D: 90 Crew
        # E: 5 Crew
        self.check_solution(self.islands, 200, selected, expected_money)
        # So we must be equal :)

    @number("1.2")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_big_crew(self):
        self.load_basic()
        nav = Mode1Navigator(self.islands, 500)
        selected = nav.select_islands()
        expected_money = 1450
        # ^ This can be achieved with ^
        # A: 100 Marines
        # B: 150 Marines
        # C: 5 Marines
        # D: 90 Marines
        # E: 100 Marines
        self.check_solution(self.islands, 500, selected, expected_money)

    @number("1.3")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_no_crew(self):
        self.load_basic()
        nav = Mode1Navigator(self.islands, 0)
        selected = nav.select_islands()
        # If you did return any islands, you shouldn't have sent anyone.
        for island, crew_sent in selected:
            self.assertEqual(crew_sent, 0)

    @number("1.4")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_repeats(self):
        # choice function should not modify the outcome or the islands.
        self.load_basic()
        nav = Mode1Navigator(self.islands, 200)
        selected = nav.select_islands()
        selected_again = nav.select_islands()
        self.check_solution(self.islands, 200, selected, 865)
        self.check_solution(self.islands, 200, selected_again, 865)

    @number("1.5")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_updates(self):
        self.load_basic()
        nav = Mode1Navigator(self.islands, 200)
        selected = nav.select_islands()
        self.check_solution(self.islands, 200, selected, 865)
        # Update Island A to have only 1 marine, rather than 100.
        nav.update_island(self.islands[0], 400, 1)
        # Done for testing \/ so check_solution works.
        self.islands[0].marines = 1
        selected_again = nav.select_islands()
        self.check_solution(self.islands, 200, selected_again, 1158)

    @number("1.6")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_multiple_crew_sizes(self):
        self.load_basic()
        nav = Mode1Navigator(self.islands, 200)
        results = nav.select_islands_from_crew_numbers([0, 200, 500, 300, 40])
        self.assertListEqual(results, [0, 865, 1450, 1160, 240])
