# PresetGameboard is a subclass of Gameboard that itializes the 
# gameboard pieces (based off of text file rather than midi file)

from music21 import *
import random
from GamePiece import Target, Token, Obstacle, Attack
from Gameboard import Gameboard

# PresetGameboard class
class PresetGameboard(Gameboard):
    def __init__(self, players):
        super().__init__(players)

    # set difficulty of gameboard
    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
        self.maxNotes = difficulty
        self.beatLength *= (self.difficulty + 1) / 3

    # initialize gameboard pieces
    def initGamePieces(self, grid):
        self.targetsHit = 0
        self.noHits = 0
        self.tokensCollected = 0
        self.obstaclesHit = 0
        self.missedTargets = 0
        self.initTargets(grid)
        self.initTokens(grid)
        self.initObstacles(grid)
        if self.players > 1:
            self.initAttacks(grid)
        
    # itialize targets based on grid
    def initTargets(self, grid):
        self.totalTargets = 0
        self.smallestLength = self.targetLength
        self.minY = 0
        self.targetsDict = dict()
        for i in range(self.cols):
            self.targetsDict[i] = []
        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        midiOffset = 60
        for i in range(len(grid[0])):
            for col in grid:
                colList = grid[col]
                msg = colList[i]
                if msg not in self.notes:
                    continue
                elemDuration = 1 / 8 # maybe allow user to choose this in create mode and store it in grid file
                y0 = self.lineY - i / 2 * self.beatLength
                y1 = y0 - elemDuration * self.targetLength - self.pieceTopMargin
                # make sure y0 - y1 < self.targetLength or beatLength? so no overlapping
                if y1 < self.minY:
                    self.minY = y1
                x = col * self.colWidth
                pitch = self.notes.index(msg) + midiOffset
                newTarget = Target(col, False, x, y0, y1, pitch)
                self.targetsDict[col].append(newTarget)
                self.totalTargets += 1

    # initialize tokens based on grid
    def initTokens(self, grid):
        self.tokensDict = dict()
        for i in range(self.cols):
            self.tokensDict[i] = []
        for i in range(len(grid[0])):
            for col in grid:
                colList = grid[col]
                msg = colList[i]
                if msg != 'T':
                    continue
                elemDuration = 1 / 8
                y0 = self.lineY - i * self.beatLength * elemDuration / 2
                y1 = y0 - elemDuration * self.tokenLength - self.pieceTopMargin
                x = col * self.colWidth
                newToken = Token(col, False, x, y0, y1)
                self.tokensDict[col].append(newToken)
    
    # initialize obstacles based on grid
    def initObstacles(self, grid):
        self.obstaclesDict = dict()
        for i in range(self.cols):
            self.obstaclesDict[i] = []
        for i in range(len(grid[0])):
            for col in grid:
                colList = grid[col]
                msg = colList[i]
                if msg != 'O':
                    continue
                elemDuration = 1 / 8
                y0 = self.lineY - i * self.beatLength * elemDuration / 2
                y1 = y0 - elemDuration * self.tokenLength - self.pieceTopMargin
                x = col * self.colWidth
                newObstacle = Obstacle(col, False, x, y0, y1)
                self.obstaclesDict[col].append(newObstacle)
    
    # initialize attacks based on grid
    def initAttacks(self, grid):
        self.attacksDict = dict()
        for i in range(self.cols):
            self.attacksDict[i] = []
        for i in range(len(grid[0])):
            for col in grid:
                colList = grid[col]
                msg = colList[i]
                if msg != '@':
                    continue
                elemDuration = 1 / 8
                y0 = self.lineY - i * self.beatLength * elemDuration / 2
                y1 = y0 - elemDuration * self.tokenLength - self.pieceTopMargin
                x = col * self.colWidth
                newAttack = Attack(col, False, x, y0, y1)
                self.attacksDict[col].append(newAttack)        