# contains GamePiece class, Target, Token, Obstacle, and Attack subclasses
# they are types of gamepieces that are a part of a gameboard

# Gamepiece class
colors = ['maroon',
          'violet red',
          'red',
          'orange red',
          'orange',
          'goldenrod',
          'lime green',
          'forest green',
          'turquoise',
          'deep sky blue',
          'dodger blue',
          'purple']

class GamePiece(object):
    def __init__(self, col, pressed, x, y0, y1):
        self.col = col
        self.pressed = False
        self.x = x
        self.y0 = y0
        self.y1 = y1

    def __repr__(self):
        return f'{self.col}, ({self.y0}, {self.y1}), {self.pressed}'

    def __hash__(self):
        return hash((self.col, self.pressed, self.x, self.y0, self.y1))

# Target class
class Target(GamePiece):
    def __init__(self, col, pressed, x, y0, y1, pitch):
        super().__init__(col, pressed, x, y0, y1)
        self.pitch = pitch
        self.color = colors[pitch % len(colors)] # color based on note's pitch
        self.missed = False

    def __repr__(self):
        return f'{self.col}, ({self.y0}, {self.y1}), {self.pressed}, {self.pitch}'

    def __hash__(self):
        return hash((self.col, self.pressed, self.x, self.y0, self.y1, self.pitch))

# Token class
class Token(GamePiece):
    def __init__(self, col, pressed, x, y0, y1):
        super().__init__(col, pressed, x, y0, y1)

# Obstacle class
class Obstacle(GamePiece):
    def __init__(self, col, pressed, x, y0, y1):
        super().__init__(col, pressed, x, y0, y1)

# Attack class
class Attack(GamePiece):
    def __init__(self, col, pressed, x, y0, y1):
        super().__init__(col, pressed, x, y0, y1)