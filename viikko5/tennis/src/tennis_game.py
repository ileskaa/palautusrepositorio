class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0
        self.score = ""

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1_points = self.player1_points + 1
        else:
            self.player2_points = self.player2_points + 1

    def get_tied_score(self):
        if self.player1_points == 0:
            self.score = "Love-All"
        elif self.player1_points == 1:
            self.score = "Fifteen-All"
        elif self.player1_points == 2:
            self.score = "Thirty-All"
        else:
            self.score = "Deuce"

    def get_advantage_scoring(self):
        difference = self.player1_points - self. player2_points

        advantage_player1 = difference == 1
        advantage_player2 = difference == -1
        win_player1 = difference >= 2

        if advantage_player1:
            self.score = "Advantage " + self.player1_name
        elif advantage_player2:
            self.score = "Advantage " + self.player2_name
        elif win_player1:
            self.score = "Win for player1"
        else:
            self.score = "Win for player2"

    def add_call_to_score(self, points):
        if points == 0:
            self.score = self.score + "Love"
        elif points == 1:
            self.score = self.score + "Fifteen"
        elif points == 2:
            self.score = self.score + "Thirty"
        elif points == 3:
            self.score = self.score + "Forty"

    def set_player_score(self, player_name):
        points = 0

        if player_name == self.player1_name:
            points = self.player1_points
        elif player_name == self.player2_name:
            self.score = self.score + "-"
            points = self.player2_points

        self.add_call_to_score(points)

    def get_regular_uneven_score(self):
        for player_name in [self.player1_name, self.player2_name]:
            self.set_player_score(player_name)

    def get_score(self):
        tie = self.player1_points == self.player2_points
        advantage_scoring = self.player1_points >= 4 or self.player2_points >= 4

        if tie:
            self.get_tied_score()
        elif advantage_scoring:
            self.get_advantage_scoring()
        else:
            self.get_regular_uneven_score()

        return self.score
