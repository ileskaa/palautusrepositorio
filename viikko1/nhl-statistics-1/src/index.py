from statistics_service import StatisticsService


def main():
    # injektoi StatisticsService-oliolle PlayerReader-luokan olio,
    # jolle on annettu konstruktoriparametrina haluttu osoite
    stats = StatisticsService()
    philadelphia_flyers_players = stats.team("PHI")
    top_scorers = stats.top(10)

    print("Philadelphia Flyers:")
    for player in philadelphia_flyers_players:
        print(player)

    print("Top point getters:")
    for player in top_scorers:
        print(player)


if __name__ == "__main__":
    main()
