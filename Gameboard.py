from music21 import *
import random
from gamePieces import Target, Token, Obstacle, Attack

class Gameboard(object):
    def __init__(self, players):
        self.score = 100
        self.players = players

    def setKeysDict(self, keysDict):
        self.keysDict = keysDict
    
    def initBoardDimensions(self, index, width, height):
        self.width, self.height = width, height
        self.offset = self.width * index
        self.bottomMargin = 100
        self.lineY = self.height - self.bottomMargin
        self.cols = 5
        self.colWidth = self.width / self.cols
        self.beatLength = 100

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
        self.maxNotes = difficulty
        self.beatLength *= (self.difficulty + 1) / 3
    
    def initScroll(self, timeInterval):
        self.scrollY = 0
        self.dy = self.beatLength * 10 / timeInterval

    def setScroll(self, dt):
        self.scrollY = self.dy * dt * 100
    
    def initGamePieceDimensions(self):
        self.pieceTopMargin = 20
        self.pieceSideMargin = self.colWidth / 8
        self.targetLength = 100
        self.tokenLength = 50

    def initGamePieces(self, partsNotes):
        self.targetsHit = 0
        self.noHits = 0
        self.tokensCollected = 0
        self.obstaclesHit = 0
        self.missedTargets = 0
        self.initTargets(partsNotes)
        self.totalTokens = 20
        self.initTokens()
        self.totalObstacles = self.totalTargets // 10
        self.initObstacles()
        if self.players > 1:
            self.totalAttacks = 100
            self.initAttacks()
        
    def initTargets(self, partsNotes):
        self.totalTargets = 0
        self.smallestLength = self.targetLength
        self.minY = 0
        self.targetsDict = dict()
        for i in range(self.cols):
            self.targetsDict[i] = []
        
        for partNotes in partsNotes:
            for msg in partNotes:
                notes = []
                if isinstance(msg, note.Note):
                    notes = [msg]
                elif isinstance(msg, chord.Chord):
                    notes = list(msg.notes)
                elemOffset = msg.offset
                for elem in notes:
                    elemDuration = elem.duration.quarterLength
                    y0 = self.lineY - elemOffset * self.beatLength
                    y1 = y0 - elemDuration * self.targetLength - self.pieceTopMargin
                    while y1 > y0:
                        y1 -= 1
                    if y1 < self.minY:
                        self.minY = y1
                    if y0 - y1 < self.smallestLength:
                        self.smallestLength = y0 - y1
                    elemMidi = elem.pitch.midi
                    col = elemMidi % self.cols
                    x = col * self.colWidth
                    if self.placeValid(col, y0, y1, self.targetsDict):
                        newTarget = Target(col, False, x, y0, y1, elemMidi)
                        self.targetsDict[col].append(newTarget)
                        self.totalTargets += 1

    def initTokens(self):
        self.tokensDict = dict()
        for i in range(self.cols):
            self.tokensDict[i] = []
        count = 0
        while count < self.totalTokens:
            col = random.randint(0, self.cols - 1)
            y1 = random.randint(int(self.minY), self.lineY - self.tokenLength) + self.pieceTopMargin
            y0 = y1 + self.tokenLength - self.pieceTopMargin
            x = col * self.colWidth
            # if (self.placeValid(col, y0, y1, self.tokensDict) and
            #     self.placeValid(col, y0, y1, self.targetsDict)):
            if self.placeValid(col, y0, y1, self.tokensDict):
                newToken = Token(col, False, x, y0, y1)
                self.tokensDict[col].append(newToken)
                count += 1
    
    def initObstacles(self):
        self.obstaclesDict = dict()
        for i in range(self.cols):
            self.obstaclesDict[i] = []
        count = 0
        while count < self.totalObstacles:
            col = random.randint(0, self.cols - 1)
            targetList = self.targetsDict[col]
            if targetList == []:
                continue
            targetIndex = random.randint(0, len(targetList) - 1)
            target = targetList.pop(targetIndex)
            x, y0, y1 = target.x, target.y0, target.y1
            newObstacle = Obstacle(col, False, x, y0, y1)
            self.obstaclesDict[col].append(newObstacle)
            count += 1
    
    def initAttacks(self):
        self.keysDisabled = False
        self.attacksDict = dict()
        for i in range(self.cols):
            self.attacksDict[i] = []
        count = 0
        while count < self.totalAttacks:
            col = random.randint(0, self.cols - 1)
            y1 = random.randint(int(self.minY), self.lineY - self.tokenLength) + self.pieceTopMargin
            y0 = y1 + self.tokenLength - self.pieceTopMargin
            x = col * self.colWidth
            if (self.placeValid(col, y0, y1, self.attacksDict) and
                self.placeValid(col, y0, y1, self.tokensDict)):
                newAttack = Attack(col, False, x, y0, y1)
                self.attacksDict[col].append(newAttack)
                count += 1

    def placeValid(self, col, y0, y1, piecesDict):
        colsList = [i for i in range(self.cols)]
        colsList.remove(col)
        random.shuffle(colsList)
        for i in range(self.maxNotes - 1):
            colsList.pop()
        colsList.append(col)
        for col in colsList:
            piecesList = piecesDict[col]
            for target in piecesList:
                y2, y3 = target.y0, target.y1
                if self.verticallyIntersecting(y0, y1, y2, y3):
                    return False
        return True

    def verticallyIntersecting(self, y0, y1, y2, y3):
        return not (y0 <= y3 or y1 >= y2)

    def checkAllPressedPieces(self, col):
        y0 = self.lineY
        y1 = self.lineY - self.smallestLength
        hitTarget = self.checkPressedPiece(self.targetsDict[col], y0, y1)
        hitToken = self.checkPressedPiece(self.tokensDict[col], y0, y1)
        hitObstacle = self.checkPressedPiece(self.obstaclesDict[col], y0, y1)
        if hitTarget:   self.targetsHit += 1
        else:           self.noHits += 1
        if hitToken:    self.tokensCollected += 1
        if hitObstacle: self.obstaclesHit += 1

    def checkPressedPiece(self, colList, y0, y1):
        hitPiece = False
        for piece in colList:
            y2, y3 = piece.y0 + self.scrollY, piece.y1 + self.scrollY
            if self.verticallyIntersecting(y0, y1, y2, y3) and not piece.pressed:
                piece.pressed = True
                hitPiece = True
                break
        return hitPiece