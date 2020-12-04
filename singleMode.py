from cmu_112_graphics import *
from music21 import *
import pygame, time, random
import homeMode, multiMode, createMode, scoreMode
from gamePieces import Target, Token, Obstacle
from Gameboard import Gameboard

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

class singleMode(Mode):
    def appStarted(mode):
        mode.activated = True
        mode.readyToPlay = False
        mode.playing = False
        mode.timerDelay = 1
        mode.initKeysHeld()
        mode.initButtonDimensions()
        mode.getNumberOfPlayers()
        if mode.players == None:
            return
        else:
            mode.disabledTime = 5
        mode.initGameboards(mode.players)
        mode.initMusic()
        if mode.midi == None or not mode.partsSet:
            return
        mode.initDifficulty()
        if mode.difficulty == None:
            return
        mode.initScrolling()
        mode.initGamePiecesAllBoards()

    def modeDeactivated(mode):
        try:
            pygame.mixer.music.stop()
            pygame.quit()
        except:
            return

    def modeActivated(mode):
        try:
            if mode.activated and mode.playing:
                pygame.mixer.music.stop()
                pygame.quit()
        except:
            mode.appStarted()
        # mode.appStarted()

    def getNumberOfPlayers(mode):
        mode.players = None
        while not (isinstance(mode.players, int) and 1 <= mode.players <= 3):
            playersString = mode.getUserInput("Enter number of players (1-3).")
            if playersString == None:
                return
            try:
                mode.players = int(playersString)
            except:
                continue

    def initGameboards(mode, players):
        keyDicts = []
        keyDict0 = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4}
        keyDict1 = {'6': 0, '7': 1, '8': 2, '9': 3, '0': 4}
        keyDict2 = {'z': 0, 'x': 1, 'c': 2, 'v': 3, 'b': 4}
        keyDicts.extend([keyDict0, keyDict1, keyDict2])
        mode.gameboards = []
        for i in range(mode.players):
            newBoard = Gameboard(mode.players)
            newBoard.initBoardDimensions(i, mode.width / mode.players, mode.height)
            newBoard.setKeysDict(keyDicts[i])
            mode.gameboards.append(newBoard)

    def initDifficulty(mode):
        mode.difficulty = None
        levels = {1, 2, 3, 4, 5}
        while not (isinstance(mode.difficulty, int) and mode.difficulty in levels):
            difficultyString = mode.getUserInput("Enter difficulty level from 1-5.")
            if difficultyString == None:
                return
            try:
                mode.difficulty = int(difficultyString)
            except:
                continue
        for i in range(mode.players):
            gameboard = mode.gameboards[i]
            gameboard.setDifficulty(mode.difficulty)

    def initScrolling(mode):
        for i in range(mode.players):
            gameboard = mode.gameboards[i]
            gameboard.initScroll(mode.timeInterval)
        
    def initGamePiecesAllBoards(mode):
        for gameboard in mode.gameboards:
            gameboard.initGamePieceDimensions()
            gameboard.initGamePieces(mode.partsNotes)
        mode.readyToPlay = True

    def initButtonDimensions(mode):
        mode.numberOfButtons = 5
        mode.buttonWidth = 60
        mode.buttonHeight = 30
        mode.by0, mode.by1 = 0, mode.buttonHeight
        mode.buttonCoordinates = []
        for i in range(mode.numberOfButtons):
            x0 = i * mode.buttonWidth
            x1 = x0 + mode.buttonWidth
            mode.buttonCoordinates.append((x0, x1))
        mode.buttonLabels = ['Home', 'Single', 'Multi', 'Create', 'Score']

    def initMusic(mode):
        mode.loadMusic()
        if mode.midi == None:
            return
        mode.getScoreInfo()
        mode.getScorePart()

    def initKeysHeld(mode):
        mode.keysHeld = set()
        mode.keyReleasedTimes = dict()
        mode.releaseWaitTime = 0.1

    def loadMusic(mode):
        pygame.init()
        mode.midi = None
        musicSet = False
        while mode.midi == None or not musicSet:
            mode.midi = mode.getUserInput("Enter midi file's path.")
            if mode.midi == None:
                return
            try:
                pygame.mixer.music.load(mode.midi)
                musicSet = True
            except:
                musicSet = False
                continue

    # extract necessary info from midi file using music21
    def getScoreInfo(mode):
        mode.musicScore = converter.parse(mode.midi)
        mode.allNotes = mode.musicScore.recurse().notesAndRests.stream()
        try:
            mode.timeSignature = mode.musicScore.recurse().getElementsByClass(meter.TimeSignature)[0]
            mode.musicScoreTempo = mode.musicScore.recurse().getElementsByClass(tempo.MetronomeMark)[0]
            mode.quarterLength = mode.musicScoreTempo.referent.quarterLength
            mode.bpm = mode.musicScoreTempo.number
        except:
            mode.quarterLength = 1 # should this be one?
            mode.bpm = 120
        mode.timeInterval = 60 * 1000 / mode.bpm # 60s * 1000ms / bpm = ms/beat, time between each note

    # select music part
    def getScorePart(mode):
        parts = mode.musicScore.parts
        mode.partsSet = False
        for i in range(len(parts)):
            part = parts[i]
            if part.partName == None:
                print(f'{i}: This part has no name.')
            else:
                print(f'{i}: {part.partName}')
        
        invalid = False

        while not mode.partsSet:
            inputString = mode.getUserInput('Enter part numbers separated by a comma.')
            if inputString == None:
                return
            try:
                inputList = inputString.split(',')
                partIndices = []
                for elem in inputList:
                    partIndex = int(elem)
                    if 0 <= partIndex < len(parts) and partIndex not in partIndices:
                        partIndices.append(partIndex)
                    else:
                        invalid = True
            except:
                continue
            if not invalid:
                mode.partsSet = True
        mode.partsNotes = []
        for index in partIndices:
            mode.partsNotes.append(parts[index].flat)
        mode.partsSet = True

    def keyPressed(mode, event):
        if event.key in mode.keyReleasedTimes:
            mode.keyReleasedTimes.pop(event.key)
        mode.keysHeld.add(event.key)

        if event.key == 'p' and not mode.playing:
            mode.playing = True
            pygame.mixer.music.play()
            mode.startTime = time.time()
            return

        attackersIndices = set()
        for i in range(len(mode.gameboards)):
            gameboard = mode.gameboards[i]
            if event.key in gameboard.keysDict and not gameboard.keysDisabled:
                col = gameboard.keysDict[event.key]
                gameboard.checkAllPressedPieces(col)
                if mode.players > 1 and gameboard.checkPressedAttack(col):
                    attackersIndices.add(i)
        if mode.players > 1 and attackersIndices != set():
            mode.disableKeysAttack(attackersIndices)

    def disableKeysAttack(mode, attackersIndices):
        disabledStartTime = time.time()
        for i in range(len(mode.gameboards)):
            if i not in attackersIndices:
                gameboard = mode.gameboards[i]
                gameboard.keysDisabled = True
                gameboard.disabledStartTime = disabledStartTime

    def keyReleased(mode, event):
        if event.key in mode.keysHeld:
            mode.keyReleasedTimes[event.key] = time.time()

    def timerFired(mode):
        mode.checkKeys()
        if mode.readyToPlay and mode.playing:
            mode.scroll()
        if mode.playing and mode.players > 1:
            mode.checkDisabledBoards()
        if mode.playing and mode.gameboards[0].minY + mode.gameboards[0].scrollY >= mode.gameboards[0].height:
            mode.playing = False

    def checkDisabledBoards(mode):
        currentTime = time.time()
        for gameboard in mode.gameboards:
            if gameboard.disabledStartTime != None and currentTime - gameboard.disabledStartTime > mode.disabledTime:
                gameboard.disabledStartTime = None
                gameboard.keysDisabled = False

    def checkKeys(mode):
        releasedKeys = set()
        for key in mode.keyReleasedTimes:
            if time.time() - mode.keyReleasedTimes[key] > mode.releaseWaitTime:
                releasedKeys.add(key)
        for key in releasedKeys:
            mode.keyReleasedTimes.pop(key)
            mode.keysHeld.remove(key)
    
    def scroll(mode):
        dt = time.time() - mode.startTime
        for gameboard in mode.gameboards:
            gameboard.setScroll(dt)

    def mousePressed(mode, event):
        x, y = event.x, event.y
        mode.checkPressedButtons(x, y)
        
    def checkPressedButtons(mode, x, y):
        mode.modesList = [mode.app.homeMode, mode.app.singleMode, mode.app.multiMode, mode.app.createMode, mode.app.scoreMode]
        y0, y1 = mode.by0, mode.by1
        for i in range(mode.numberOfButtons):
            x0, x1 = mode.buttonCoordinates[i]
            if x0 < x < x1 and y0 < y < y1:
                if i == 1:
                    mode.appStarted()
                    return
                mode.app.setActiveMode(mode.modesList[i])

    def drawGameboards(mode, canvas):
        for gameboard in mode.gameboards:
            mode.drawTargets(canvas, gameboard)
            mode.drawTokens(canvas, gameboard)
            mode.drawObstacles(canvas, gameboard)
            if mode.players > 1:
                mode.drawAttacks(canvas, gameboard)
                mode.drawAttackMessages(canvas, gameboard)
            mode.drawStrikeLine(canvas, gameboard)
            mode.drawStats(canvas, gameboard)
            x = gameboard.offset + gameboard.width
            y0, y1 = 0, mode.height
            canvas.create_line(x, y0, x, y1)

    def drawTargets(mode, canvas, gameboard):
        targetsDict = gameboard.targetsDict
        for col in targetsDict:
            for target in targetsDict[col]:
                x0 = target.x + gameboard.pieceSideMargin + gameboard.offset
                x1 = x0 + gameboard.colWidth - 2 * gameboard.pieceSideMargin
                y0 = target.y0 + gameboard.scrollY
                y1 = target.y1 + gameboard.scrollY
                if y1 > gameboard.height or y0 < 0:
                    continue
                if y1 > gameboard.lineY and not target.pressed and target.color != 'red':
                    target.color = 'red'
                    gameboard.missedTargets += 1 # FIX THIS IT'S NOT WORKING
                elif target.pressed:
                    target.color = 'green'
                canvas.create_rectangle(x0, y0, x1, y1, fill=target.color)

    def drawTokens(mode, canvas, gameboard):
        tokensDict = gameboard.tokensDict
        for col in tokensDict:
            for token in tokensDict[col]:
                x0 = token.x + gameboard.pieceSideMargin + gameboard.offset
                x1 = x0 + gameboard.colWidth - 2 * gameboard.pieceSideMargin
                y0 = token.y0 + gameboard.scrollY
                y1 = token.y1 + gameboard.scrollY
                if y1 > gameboard.height or y0 < 0:
                    continue
                if token.pressed:
                    color = 'green'
                else:
                    color = 'gold'
                canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def drawObstacles(mode, canvas, gameboard):
        obstaclesDict = gameboard.obstaclesDict
        for col in obstaclesDict:
            for obstacle in gameboard.obstaclesDict[col]:
                x0 = obstacle.x + gameboard.pieceSideMargin + gameboard.offset
                x1 = x0 + gameboard.colWidth - 2 * gameboard.pieceSideMargin
                y0 = obstacle.y0 + gameboard.scrollY
                y1 = obstacle.y1 + gameboard.scrollY
                if y1 > gameboard.height or y0 < 0:
                    continue
                if obstacle.pressed:
                    color = 'red'
                else:
                    color = 'black'
                canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def drawAttacks(mode, canvas, gameboard):
        attacksDict = gameboard.attacksDict
        for col in attacksDict:
            for attack in attacksDict[col]:
                x0 = attack.x + gameboard.pieceSideMargin + gameboard.offset
                x1 = x0 + gameboard.colWidth - 2 * gameboard.pieceSideMargin
                y0 = attack.y0 + gameboard.scrollY
                y1 = attack.y1 + gameboard.scrollY
                if y1 > gameboard.height or y0 < 0:
                    continue
                if attack.pressed:
                    color = 'green'
                else:
                    color = 'purple'
                canvas.create_rectangle(x0, y0, x1, y1, fill=color)
    
    def drawAttackMessages(mode, canvas, gameboard):
        if gameboard.keysDisabled:
            x0 = gameboard.offset
            x1 = x0 + gameboard.width
            y0 = gameboard.lineY
            y1 = mode.height
            canvas.create_rectangle(x0, y0, x1, y1, fill='yellow')
            textX = (2 * gameboard.offset + gameboard.width) / 2
            textY = (gameboard.lineY + gameboard.height) / 2
            timeLeft = int(mode.disabledTime - (time.time() - gameboard.disabledStartTime)) + 1
            canvas.create_text(textX, textY, text=f'Keys disabled for {timeLeft} more seconds!')

    def drawStrikeLine(mode, canvas, gameboard):
        canvas.create_line(gameboard.offset, gameboard.lineY, gameboard.width + gameboard.offset, gameboard.lineY,
                        width=5)
        if gameboard.keysDisabled:
            return
        for key in gameboard.keysDict:
            col = gameboard.keysDict[key]
            keyX = (col + 1 / 2) * gameboard.colWidth + gameboard.offset
            keyY = (gameboard.lineY + gameboard.height) / 2
            canvas.create_text(keyX, keyY, text=key)
            if key in mode.keysHeld:
                x0 = col * gameboard.colWidth + gameboard.offset
                x1 = x0 + gameboard.colWidth
                y0 = gameboard.lineY - gameboard.smallestLength
                y1 = gameboard.lineY
                canvas.create_rectangle(x0, y0, x1, y1, fill='gray')

    def drawStats(mode, canvas, gameboard):
        mode.boxWidth, mode.boxHeight = 125, mode.buttonHeight * 5
        x0 = gameboard.offset + gameboard.width - mode.boxWidth + 10
        x1 = gameboard.offset + gameboard.width
        y0 = mode.buttonHeight
        y1 = y0 + mode.boxHeight
        canvas.create_rectangle(x0, y0, x1, y1, fill='yellow')
        canvas.create_text(x0, y0, text=f'Targets Hit: {gameboard.targetsHit}', anchor='nw')
        canvas.create_text(x0, y0 + mode.buttonHeight, text=f'Tokens: {gameboard.tokensCollected}', anchor='nw')
        canvas.create_text(x0, y0 + mode.buttonHeight * 2, text=f'Obstacles: {gameboard.obstaclesHit}', anchor='nw')
        canvas.create_text(x0, y0 + mode.buttonHeight * 3, text=f'Missed: {gameboard.missedTargets}', anchor='nw')
        canvas.create_text(x0, y0 + mode.buttonHeight * 4, text=f'No hits: {gameboard.noHits}', anchor='nw')

    def drawButtons(mode, canvas):
        for i in range(mode.numberOfButtons):
            x0, x1 = mode.buttonCoordinates[i]
            y0, y1 = mode.by0, mode.by1
            canvas.create_rectangle(x0, y0, x1, y1, fill='white')
            textX, textY = (x0 + x1) / 2, (y0 + y1) / 2
            canvas.create_text(textX, textY, text=mode.buttonLabels[i])

    def redrawAll(mode, canvas):
        if mode.readyToPlay:
            mode.drawGameboards(canvas)
        mode.drawButtons(canvas)