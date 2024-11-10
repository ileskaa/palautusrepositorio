import requests
from player import Player


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2023-24/players"
    response = requests.get(url).json()

    # print("JSON-muotoinen vastaus:")
    # print(response)

    players = []

    for player_dict in response:
        player = Player(player_dict)
        players.append(player)

    players.sort(key=lambda player: player.goals + player.assists, reverse=True)

    print("Players from FIN\n")

    for player in players:
        if player.nationality == 'FIN':
            print(player)


if __name__ == "__main__":
    main()
