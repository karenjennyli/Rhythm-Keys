# each target is one note
class Target(object):
    def __init__(self, col, pressed, x, y0, y1, pitch):
        self.col = col
        self.pressed = False
        self.x = x
        self.y0 = y0
        self.y1 = y1
        self.pitch = pitch

    def __repr__(self):
        return f'{self.col}, ({self.y0}, {self.y1}), {self.pressed}, {self.pitch}'

    def __hash__(self):
        return hash((self.col, self.pressed, self.x, self.y0, self.y1, self.pitch))

    def changeColor(self, color):
        self.color = color

class Token(object):
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

class Obstacle(object):
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