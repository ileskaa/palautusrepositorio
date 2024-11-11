import requests
from rich.prompt import Prompt
from player import Player
from rich.console import Console
from rich.table import Table


class PlayerReader:
    def __init__(self, url):
        self.url = url

    def get_players(self):
        response = requests.get(self.url).json()
        players = []
        for player_dict in response:
            player = Player(player_dict)
            players.append(player)
        return players


class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality):
        players = self.reader.get_players()
        filter_obj = filter(lambda player: player.nationality == nationality, players)
        filtered_players = list(filter_obj)
        filtered_players.sort(key=lambda player: player.goals + player.assists, reverse=True)
        return filtered_players


def print_table(nationality, season, players):
    title = f"[i]Top scorers of {nationality} season {season}[/i]"
    table = Table(title=title)

    table.add_column("name", style="cyan", no_wrap=True)
    table.add_column("team", style="magenta")
    table.add_column("goals", justify="right", style="green")
    table.add_column("assists", justify="right", style="green")
    table.add_column("points", justify="right", style="green")

    for player in players:
        points = str(player.goals + player.assists)
        table.add_row(player.name, player.team, str(player.goals), str(player.assists), points)

    console = Console()
    console.print(table)


def main():
    seasons = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
    season = Prompt.ask("Select season", choices=seasons)
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    nationality_map = map(lambda player: player.nationality, reader.get_players())
    nationalities = list(set(nationality_map))

    while True:
        nationality = Prompt.ask("Select nationality", choices=nationalities)
        players = stats.top_scorers_by_nationality(nationality)
        print_table(nationality, season, players)


if __name__ == "__main__":
    main()
