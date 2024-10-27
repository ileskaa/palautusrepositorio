import unittest
from statistics_service import StatisticsService
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
        best = self.stats.top(1)
        name = best[0].name
        self.assertEqual(name, "Gretzky")
