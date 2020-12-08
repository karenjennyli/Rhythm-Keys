# Score class for storing the information of the scoreboard

class Score(object):
    scoreboard = []

    @staticmethod
    # referenced for sorting:
    # https://www.techiedelight.com/sort-list-of-objects-by-multiple-attributes-python/
    def assignPlaces():
        Score.scoreboard.sort(key=lambda x: (-x.score, -x.difficulty, x. song, x.player))
        for i in range(len(Score.scoreboard)):
            score = Score.scoreboard[i]
            score.place = i + 1
            score.attributes[0] = score.place

    def __init__(self, player, score, song, difficulty):
        self.player = player
        self.score = score
        self.song = song
        self.difficulty = difficulty
        self.place = -1
        self.attributes = [self.place, self.player, self.score, self.difficulty, self.song]
        Score.scoreboard.append(self)
        Score.assignPlaces()

    def __repr__(self):
        return f'{self.place}: {self.score}, {self.player}, {self.difficulty}, {self.song}'