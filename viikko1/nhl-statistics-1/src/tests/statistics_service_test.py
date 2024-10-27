import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

players = [
    Player("Semenko", "EDM", 4, 12),
    Player("Lemieux", "PIT", 45, 54),
    Player("Kurri",   "EDM", 37, 53),
    Player("Yzerman", "DET", 42, 56),
    Player("Gretzky", "EDM", 35, 89)
]


class PlayerReaderStub:
    def get_players(self):
        return players


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_konstruktori_asettaa_pelaajat(self):
        self.stats._players = players

    def test_haku_toimii_oikein(self):
        loytyy = self.stats.search("Kurri")
        self.assertEqual(loytyy.team, "EDM")
        self.assertEqual(loytyy.goals, 37)
        self.assertEqual(loytyy.assists, 53)
        ei_loydy = self.stats.search("Kuri")
        self.assertEqual(ei_loydy, None)

    def test_palauttaa_joukkueen_pelaajat(self):
        pittsburgh = self.stats.team("PIT")
        name = pittsburgh[0].name
        self.assertEqual(name, "Lemieux")

    def test_palauttaa_parhaan_pelaajan(self):
        best_points = self.stats.top(1, SortBy.POINTS)[0]
        self.assertEqual(best_points.name, "Gretzky")
        most_goals = self.stats.top(1, SortBy.GOALS)[0]
        self.assertEqual(most_goals.name, "Lemieux")
        most_assists = self.stats.top(1, SortBy.ASSISTS)[0]
        self.assertEqual(most_assists.name, "Gretzky")
