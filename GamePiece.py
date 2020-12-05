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

class Target(GamePiece):
    def __init__(self, col, pressed, x, y0, y1, pitch):
        super().__init__(col, pressed, x, y0, y1)
        self.pitch = pitch
        self.color = 'white'

    def __repr__(self):
        return f'{self.col}, ({self.y0}, {self.y1}), {self.pressed}, {self.pitch}'

    def __hash__(self):
        return hash((self.col, self.pressed, self.x, self.y0, self.y1, self.pitch))

class Token(GamePiece):
    def __init__(self, col, pressed, x, y0, y1):
        super().__init__(col, pressed, x, y0, y1)

class Obstacle(GamePiece):
    def __init__(self, col, pressed, x, y0, y1):
        super().__init__(col, pressed, x, y0, y1)

class Attack(GamePiece):
    def __init__(self, col, pressed, x, y0, y1):
        super().__init__(col, pressed, x, y0, y1)