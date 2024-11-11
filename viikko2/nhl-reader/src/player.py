class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict['nationality']
        self.assists = dict['assists']
        self.goals = dict['goals']
        self.team = dict['team']
        self.games = dict['games']
        if "id" in dict:
            self.id = dict['id']

    def __str__(self):
        playerstr = f"{self.name:20} team {self.team} goals {self.goals} assists {self.assists}"
        return playerstr
