from cmu_112_graphics import *
from music21 import *
import pygame, time, random, os
import HomeMode
from GamePiece import Target, Token, Obstacle
from Gameboard import Gameboard
from Score import Score

class PlayMode(Mode):
    def appStarted(mode):
        mode.initBackground()
        mode.getSongOptions()
        mode.activated = True
        mode.readyToPlay = False
        mode.displayParts = False
        mode.playing = False
        mode.gameOver = False
        mode.timerDelay = 1
        mode.displayEndScores = False
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
        if pygame.mixer.get_init() == None:
            return
        pygame.mixer.music.stop()
        pygame.quit()

    # how to make sure this isn't called when it's the first time the mode is activated?
    def modeActivated(mode):
        mode.appStarted()

    def getNumberOfPlayers(mode):
        mode.players = None
        while not (isinstance(mode.players, int) and 1 <= mode.players <= 4):
            playersString = mode.getUserInput("Enter number of players (up to 4).")
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
        keyDict3 = {'n': 0, 'm': 1, ',': 2, '.': 3, '/': 4}
        keyDicts.extend([keyDict0, keyDict1, keyDict2, keyDict3])
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
        mode.buttonWidth = mode.buttonHeight = 40
        mode.bx0 = 10
        mode.bx1 = mode.bx0 + mode.buttonWidth
        mode.by0 = 10
        mode.by1 = mode.by0 + mode.buttonHeight
        # https://www.flaticon.com/
        mode.homeButton = mode.loadImage("home.png")

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
        index = None
        while index == None or index not in range(len(mode.filesInFolder)):
            inputString = mode.getUserInput("Enter song number.")
            if inputString == None:
                return
            try:
                index = int(inputString)
            except:
                continue
        mode.midi = 'music/' + mode.filesInFolder[index]
        pygame.mixer.music.load(mode.midi)

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
        mode.parts = mode.musicScore.parts
        mode.partsSet = False
        mode.displayParts = True
        invalid = False
        while not mode.partsSet:
            invalid = False
            inputString = mode.getUserInput('Enter part numbers separated by a comma.')
            if inputString == None:
                return
            try:
                inputList = inputString.split(',')
                partIndices = []
                for elem in inputList:
                    partIndex = int(elem)
                    if 0 <= partIndex < len(mode.parts) and partIndex not in partIndices:
                        partIndices.append(partIndex)

                    else:
                        invalid = True
            except:
                continue
            if not invalid:
                mode.partsSet = True
        mode.partsNotes = []
        for index in partIndices:
            mode.partsNotes.append(mode.parts[index].flat)
        mode.partsSet = True

    def keyPressed(mode, event):
        if event.key in mode.keyReleasedTimes:
            mode.keyReleasedTimes.pop(event.key)
        mode.keysHeld.add(event.key)
        if event.key == 'p' and not mode.playing and mode.readyToPlay:
            mode.playing = True
            pygame.mixer.music.play()
            mode.startTime = time.time()
            return
        if not mode.playing:
            return
        attackersIndices = set()
        for i in range(len(mode.gameboards)):
            gameboard = mode.gameboards[i]
            if event.key in gameboard.keysDict and not gameboard.keysDisabled:
                col = gameboard.keysDict[event.key]
                hitAttack = gameboard.checkAllPressedPieces(col)
                if mode.players > 1 and hitAttack:
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
            if mode.players > 1:
                mode.checkDisabledBoards()
            for gameboard in mode.gameboards:
                gameboard.calculateScore()
        if mode.playing and mode.gameboards[0].minY + mode.gameboards[0].scrollY >= mode.gameboards[0].height and not mode.gameOver:
            mode.playing = False
            mode.gameOver = True
            for gameboard in mode.gameboards:
                gameboard.keysDisabled = False
            mode.displayEndScores = True
            mode.addScore()

    def addScore(mode):
        for i in range(len(mode.gameboards)):
            player = mode.getUserInput(f"Enter player {i + 1}'s name if you want to get added to the scoreboard.")
            if player == None:
                return
            gameboard = mode.gameboards[i]
            song = mode.midi.split('/')[-1]
            song = song.split('.')[0]
            newScore = Score(player, gameboard.score, song, mode.difficulty)

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
        if mode.bx0 < x < mode.bx1 and mode.by0 < y < mode.by1:
            mode.app.setActiveMode(mode.app.HomeMode)

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
            canvas.create_line(x, y0, x, y1, fill='white', width=4)

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
                canvas.create_rectangle(x0, y0, x1, y1, outline=target.color, width=4, fill='black')

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
                canvas.create_rectangle(x0, y0, x1, y1, outline=color, width=4, fill='black')

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
                canvas.create_rectangle(x0, y0, x1, y1, outline='red', width=4, fill='black')

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
                canvas.create_rectangle(x0, y0, x1, y1, outline=color, width=4, fill='black')
    
    def drawAttackMessages(mode, canvas, gameboard):
        if gameboard.keysDisabled and mode.playing:
            x0 = gameboard.offset
            x1 = x0 + gameboard.width
            y0 = gameboard.lineY
            y1 = mode.height
            canvas.create_rectangle(x0, y0, x1, y1, fill='black')
            textX = (2 * gameboard.offset + gameboard.width) / 2
            textY = (gameboard.lineY + gameboard.height) / 2
            timeLeft = int(mode.disabledTime - (time.time() - gameboard.disabledStartTime)) + 1
            if timeLeft == 1:
                canvas.create_text(textX, textY, text=f'Keys disabled for {timeLeft} more second!', fill='white')
            else:
                canvas.create_text(textX, textY, text=f'Keys disabled for {timeLeft} more seconds!', fill='white')

    def drawStrikeLine(mode, canvas, gameboard):
        canvas.create_line(gameboard.offset, gameboard.lineY, gameboard.width + gameboard.offset, gameboard.lineY,
                        width=4, fill='white')
        if gameboard.keysDisabled:
            return
        for key in gameboard.keysDict:
            col = gameboard.keysDict[key]
            keyX = (col + 1 / 2) * gameboard.colWidth + gameboard.offset
            keyY = (gameboard.lineY + gameboard.height) / 2
            canvas.create_text(keyX, keyY, text=key, fill='white', font='System 18 bold')
            if key in mode.keysHeld:
                x0 = col * gameboard.colWidth + gameboard.offset
                x1 = x0 + gameboard.colWidth
                y0 = gameboard.lineY - gameboard.smallestLength
                y1 = gameboard.lineY
                canvas.create_rectangle(x0, y0, x1, y1, fill='blue', outline='blue')

    def drawStats(mode, canvas, gameboard):
        intervalY = 25
        boxWidth, boxHeight = 150, intervalY * 6 + 5
        x0 = gameboard.offset + gameboard.width - boxWidth
        x1 = gameboard.offset + gameboard.width
        y0 = 0
        y1 = y0 + boxHeight
        textX = x0 + 10
        textY = y0 + 5
        canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='white', width=4)
        canvas.create_text(textX, textY, text=f'Score: {gameboard.score}', anchor='nw', fill='white', font='System 14 bold')
        canvas.create_text(textX, textY + intervalY, text=f'Targets: {gameboard.targetsHit}', anchor='nw', fill='white', font='System 14 bold')
        canvas.create_text(textX, textY + intervalY * 2, text=f'Tokens: {gameboard.tokensCollected}', anchor='nw', fill='white', font='System 14 bold')
        canvas.create_text(textX, textY + intervalY * 3, text=f'Obstacles: {gameboard.obstaclesHit}', anchor='nw', fill='white', font='System 14 bold')
        canvas.create_text(textX, textY + intervalY * 4, text=f'Missed: {gameboard.missedTargets}', anchor='nw', fill='white', font='System 14 bold')
        canvas.create_text(textX, textY + intervalY * 5, text=f'No Hits: {gameboard.noHits}', anchor='nw', fill='white', font='System 14 bold')

    def drawEndScores(mode, canvas):
        for i in range(len(mode.gameboards)):
            gameboard = mode.gameboards[i]
            boxWidth, boxHeight = gameboard.width * 3 / 4, gameboard.height / 5
            x0 = (2 * gameboard.offset + gameboard.width) / 2 - boxWidth / 2
            x1 = x0 + boxWidth
            y0 = gameboard.height / 2 - boxHeight / 2
            y1 = y0 + boxHeight
            canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='white', width=4)
            textX = (x0 + x1) / 2
            textY = gameboard.height / 2
            if mode.players == 1:
                canvas.create_text(textX, textY - 15, text='Final score was:', fill='white', font='System 18 bold')
                canvas.create_text(textX, textY + 15, text=f'{gameboard.score}', fill='white', font='System 18 bold')
            else:
                canvas.create_text(textX, textY - 15, text=f"Player {i + 1}'s score was:", fill='white', font='System 18 bold')
                canvas.create_text(textX, textY + 15, text=f'{gameboard.score}', fill='white', font='System 18 bold')

    def drawSongOptions(mode, canvas):
        # canvas.create_text(mode.width / 2, mode.height / 2, text='choose from the songs in terminal', fill='white')
        # for i in range(len(mode.filesInFolder)):
        #     print(f'{i}: {mode.filesInFolder[i]}')
        startY = 100
        canvas.create_text(mode.width / 2, startY, text='Song Options', fill='white', font='System 36 bold')
        startY += 50
        intervalY = 30
        numberX = 100
        songX = numberX + 100
        for i in range(len(mode.filesInFolder)):
            song = mode.filesInFolder[i].split('.')[0]
            canvas.create_text(numberX, startY + intervalY * i, text=str(i), anchor='w', fill='white', font='System 18 bold')
            canvas.create_text(songX, startY + intervalY * i, text=song, anchor='w', fill='white', font='System 18 bold')

    def getSongOptions(mode):
        mode.filesInFolder = os.listdir('music')
    
    def drawParts(mode, canvas):
        startY = 100
        canvas.create_text(mode.width / 2, startY, text='Part Options', fill='white', font='System 36 bold')
        startY += 50
        intervalY = 30
        numberX = 100
        partX = numberX + 100
        for i in range(len(mode.parts)):
            part = mode.parts[i]
            if part.partName == None:
                label = f'Part {i}'
            else:
                label = part.partName
            canvas.create_text(numberX, startY + intervalY * i, text=str(i), anchor='w', fill='white', font='System 18 bold')
            canvas.create_text(partX, startY + intervalY * i, text=label, anchor='w', fill='white', font='System 18 bold')


    def drawButtons(mode, canvas):
        textX, textY = (mode.bx0 + mode.bx1) / 2, (mode.by0 + mode.by1) / 2
        canvas.create_image(textX, textY, image=ImageTk.PhotoImage(mode.homeButton))

    def initBackground(mode):
        # image from https://www.mobilebeat.com/wp-content/uploads/2016/07/Background-Music-768x576-1280x720.jpg
        mode.background = mode.scaleImage(mode.loadImage("homebackground.png"), 1/2)
    
    def drawBackground(mode, canvas):
        canvas.create_image(mode.width / 2, mode.height / 2, image=ImageTk.PhotoImage(mode.background))

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='black')
        if mode.readyToPlay:
            mode.drawGameboards(canvas)
        else:
            mode.drawBackground(canvas)
            if not mode.displayParts:
                mode.drawSongOptions(canvas)
        if mode.displayParts and not mode.readyToPlay:
            mode.drawParts(canvas)
        if mode.displayEndScores:
            mode.drawEndScores(canvas)
        mode.drawButtons(canvas)