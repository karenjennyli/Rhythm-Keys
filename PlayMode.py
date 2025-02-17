# PlayMode class: the mode that allows the player to choose their song 
# and play the song

from cmu_112_graphics import *
from music21 import *
import pygame, time, random, os
import HomeMode
from GamePiece import Target, Token, Obstacle
from Gameboard import Gameboard
from PresetGameboard import PresetGameboard
from Score import Score

# Playmode Class
class PlayMode(Mode):
    def appStarted(mode):
        mode.initBackground()
        mode.getSongOptions()
        mode.partsSet = False
        mode.presetGameboard = False
        mode.activated = True
        mode.readyToPlay = False
        mode.displayParts = False
        mode.playing = False
        mode.gameOver = False
        mode.timerDelay = 1
        mode.displayEndScores = False
        mode.difficulty = None
        mode.initKeysHeld()
        mode.initButtonDimensions()
        mode.getNumberOfPlayers()
        if mode.players == None:
            return
        else:
            mode.disabledTime = 5
        mode.initMusic()
        mode.initGameboards(mode.players)
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

    ###############################################
    # Initializing
    ###############################################

    # get background image
    def initBackground(mode):
        # image from https://www.mobilebeat.com/wp-content/uploads/2016/07/Background-Music-768x576-1280x720.jpg
        mode.background = mode.scaleImage(mode.loadImage("pictures/homebackground.png"), 1/2)
        # images from https://www.flaticon.com/
        mode.skull = mode.loadImage("pictures/skull.png")
        mode.sword = mode.loadImage("pictures/sword.png")
    
    # get user input of number of players
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

    # initialized gameboards
    def initGameboards(mode, players):
        keyDicts = []
        keyDict0 = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4}
        keyDict1 = {'6': 0, '7': 1, '8': 2, '9': 3, '0': 4}
        keyDict2 = {'z': 0, 'x': 1, 'c': 2, 'v': 3, 'b': 4}
        keyDict3 = {'n': 0, 'm': 1, ',': 2, '.': 3, '/': 4}
        keyDicts.extend([keyDict0, keyDict1, keyDict2, keyDict3])
        mode.gameboards = []
        for i in range(mode.players):
            if not mode.presetGameboard:
                newBoard = Gameboard(mode.players)
            else:
                newBoard = PresetGameboard(mode.players)
            newBoard.initBoardDimensions(i, mode.width / mode.players, mode.height)
            newBoard.setKeysDict(keyDicts[i])
            mode.gameboards.append(newBoard)

    # get difficulty based on user input
    def initDifficulty(mode):
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

    # intialize scrolling for each gameboard
    def initScrolling(mode):
        for i in range(mode.players):
            gameboard = mode.gameboards[i]
            gameboard.initScroll(mode.timeInterval)
        
    # initialize all gameboard pieces for all gameboards
    def initGamePiecesAllBoards(mode):
        for gameboard in mode.gameboards:
            gameboard.initGamePieceDimensions()
            if mode.presetGameboard:
                gameboard.initGamePieces(mode.grid)
            else:
                gameboard.initGamePieces(mode.partsNotes)
        mode.readyToPlay = True

    # button dimensions
    def initButtonDimensions(mode):
        mode.buttonWidth = mode.buttonHeight = 40
        mode.bx0 = 10
        mode.bx1 = mode.bx0 + mode.buttonWidth
        mode.by0 = 10
        mode.by1 = mode.by0 + mode.buttonHeight
        # https://www.flaticon.com/
        mode.homeButton = mode.loadImage("pictures/home.png")

    # get the music that player wants to play and info from the music
    def initMusic(mode):
        mode.loadMusic()
        if mode.midi == None:
            return
        mode.getScoreInfo()
        mode.getScorePart()

    # intialize keysHeld dict to store keys currently pressed
    def initKeysHeld(mode):
        mode.keysHeld = set()
        mode.keyReleasedTimes = dict()
        mode.releaseWaitTime = 0.1

    # get song player wants to play
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
        fileName = mode.filesInFolder[index]
        textFileName = fileName.split('.')[0] + '.txt'
        if textFileName in os.listdir('gameboards'):
            mode.presetGameboard = True
            textFileName = 'gameboards/' + textFileName
            textFile = open(textFileName, 'r')
            mode.textGrid = textFile.read()
            mode.getGrid()
        mode.midi = 'music/' + fileName
        pygame.mixer.music.load(mode.midi)

    # get the grid from saved gameboards folder
    def getGrid(mode):
        gridList = mode.textGrid.splitlines()
        mode.grid = dict()
        for i in range(len(gridList)):
            mode.grid[i] = gridList[i].split(' ')
            mode.grid[i].pop()

    # extract necessary info from midi file using music21
    # referenced music21 user's guide and documentation to use music21 module
    # https://web.mit.edu/music21/doc/usersGuide/index.html
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
        # time interval is time in ms / beat (quarter note)
        mode.timeInterval = 60 * 1000 / mode.bpm # 60s * 1000ms / bpm = ms/beat, time between each note

    # select music part
    # referenced music21 user's guide and documentation to use music21 module
    # https://web.mit.edu/music21/doc/usersGuide/index.html
    def getScorePart(mode):
        mode.parts = mode.musicScore.parts
        if mode.presetGameboard: # use all the parts(there's probably only going to be one)
            partIndices = [i for i in range(len(mode.parts))]
            mode.partsSet = True
        else:
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

    # get all the names of the files in the music folder
    def getSongOptions(mode):
        mode.filesInFolder = os.listdir('music')
    
    ###############################################
    # Checking for events
    ###############################################

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

    # disable gameboard's keys after getting attacked
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

    # let user add their score to the scoreboard
    def addScore(mode):
        for i in range(len(mode.gameboards)):
            player = mode.getUserInput(f"Enter player {i + 1}'s name if you want to get added to the scoreboard.")
            if player == None:
                return
            gameboard = mode.gameboards[i]
            song = mode.midi.split('/')[-1]
            song = song.split('.')[0]
            newScore = Score(player, gameboard.score, song, mode.difficulty)

    # check if the gameboards should still be disabled
    def checkDisabledBoards(mode):
        currentTime = time.time()
        for gameboard in mode.gameboards:
            if gameboard.disabledStartTime != None and currentTime - gameboard.disabledStartTime > mode.disabledTime:
                gameboard.disabledStartTime = None
                gameboard.keysDisabled = False

    # check if the keys are still pressed
    def checkKeys(mode):
        releasedKeys = set()
        for key in mode.keyReleasedTimes:
            if time.time() - mode.keyReleasedTimes[key] > mode.releaseWaitTime:
                releasedKeys.add(key)
        for key in releasedKeys:
            mode.keyReleasedTimes.pop(key)
            mode.keysHeld.remove(key)
    
    # scroll the screen
    def scroll(mode):
        dt = time.time() - mode.startTime
        for gameboard in mode.gameboards:
            gameboard.setScroll(dt)

    def mousePressed(mode, event):
        x, y = event.x, event.y
        mode.checkPressedButtons(x, y)
        
    # check if home button is pressed
    def checkPressedButtons(mode, x, y):
        if mode.bx0 < x < mode.bx1 and mode.by0 < y < mode.by1:
            mode.app.setActiveMode(mode.app.HomeMode)

    ###############################################
    # Drawing
    ###############################################

    # draw all gameboards
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
        decimal = -mode.gameboards[0].scrollY / (mode.gameboards[0].minY - mode.gameboards[0].height)
        x = decimal * mode.width
        y = mode.height
        canvas.create_line(0, y, x, y, fill='white', width=30)

    # draw all targets
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
                if y1 > gameboard.lineY and not target.pressed and not target.missed:
                    target.missed = True
                    gameboard.missedTargets += 1
                if not target.pressed:
                    canvas.create_rectangle(x0, y0, x1, y1, outline=target.color, width=4, fill='black')

    # draw all tokens
    def drawTokens(mode, canvas, gameboard):
        tokensDict = gameboard.tokensDict
        for col in tokensDict:
            for token in tokensDict[col]:
                x0 = token.x + gameboard.pieceSideMargin + gameboard.offset
                x1 = x0 + gameboard.colWidth - 2 * gameboard.pieceSideMargin
                y0 = token.y0 + gameboard.scrollY
                y1 = token.y1 + gameboard.scrollY
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                r = abs(y0 - y1) / 2
                if y1 > gameboard.height or y0 < 0:
                    continue
                color = 'gold'
                if not token.pressed:
                    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color, width=4, fill='black')
                    r *= .6
                    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=color, width=4, fill='black')

    # draw all obstacles
    def drawObstacles(mode, canvas, gameboard):
        obstaclesDict = gameboard.obstaclesDict
        for col in obstaclesDict:
            for obstacle in gameboard.obstaclesDict[col]:
                x0 = obstacle.x + gameboard.pieceSideMargin + gameboard.offset
                x1 = x0 + gameboard.colWidth - 2 * gameboard.pieceSideMargin
                y0 = obstacle.y0 + gameboard.scrollY
                y1 = obstacle.y1 + gameboard.scrollY
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                if y1 > gameboard.height or y0 < 0:
                    continue
                if not obstacle.pressed:
                    canvas.create_rectangle(x0, y0, x1, y1, outline='white', width=4, fill='black')
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.skull))

    # draw all attacks
    def drawAttacks(mode, canvas, gameboard):
        attacksDict = gameboard.attacksDict
        for col in attacksDict:
            for attack in attacksDict[col]:
                x0 = attack.x + gameboard.pieceSideMargin + gameboard.offset
                x1 = x0 + gameboard.colWidth - 2 * gameboard.pieceSideMargin
                y0 = attack.y0 + gameboard.scrollY
                y1 = attack.y1 + gameboard.scrollY
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                if y1 > gameboard.height or y0 < 0:
                    continue
                if attack.pressed:
                    color = 'green'
                else:
                    color = 'red'
                if not attack.pressed:
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.sword))
                    # canvas.create_rectangle(x0, y0, x1, y1, outline=color, width=4, fill='black')
    
    # draw the message that the gameboard's keys are disabled
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
                canvas.create_text(textX, textY, text=f'Keys disabled for {timeLeft} more second!', fill='white', font='System 14 bold')
            else:
                canvas.create_text(textX, textY, text=f'Keys disabled for {timeLeft} more seconds!', fill='white', font='System 14 bold')

    # the strike line at the bottom of the screen
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
                # y0 = gameboard.lineY - gameboard.smallestLength
                y0 = gameboard.lineY - gameboard.tokenLength
                y1 = gameboard.lineY
                canvas.create_rectangle(x0, y0, x1, y1, fill='blue', outline='blue')

    # draw the stats of the player
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

    # draw a message with the player's end score
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

    # draw the song options the player can choose from
    def drawSongOptions(mode, canvas):
        startY = 50
        canvas.create_text(mode.width / 2, startY, text='Song Options', fill='white', font='System 36 bold')
        startY += 50
        intervalY = 20
        numberX = 100
        songX = numberX + 50
        for i in range(len(mode.filesInFolder)):
            fileName = mode.filesInFolder[i]
            song = fileName.split('.')[0]
            textFileName = song + '.txt'
            if textFileName in os.listdir('gameboards'):
                style = 'System 14 bold italic'
                song = '* ' + song
            else:
                style = 'System 14 bold'
            canvas.create_text(numberX, startY + intervalY * i, text=str(i), anchor='w', fill='white', font='System 14 bold')
            canvas.create_text(songX, startY + intervalY * i, text=song, anchor='w', fill='white', font=style)
        textX = mode.width / 2
        textY = mode.height - 10
        canvas.create_text(textX, textY, text='Italicized titles with * have a preset gameboard.', anchor='s', font='System 18 bold italic', fill='white')

    # draw the part options for a song the user can choose from
    def drawParts(mode, canvas):
        startY = 50
        canvas.create_text(mode.width / 2, startY, text='Part Options', fill='white', font='System 36 bold')
        startY += 50
        intervalY = 20
        numberX = 100
        partX = numberX + 50
        for i in range(len(mode.parts)):
            part = mode.parts[i]
            if part.partName == None:
                label = f'Part {i}'
            else:
                label = part.partName
            canvas.create_text(numberX, startY + intervalY * i, text=str(i), anchor='w', fill='white', font='System 14 bold')
            canvas.create_text(partX, startY + intervalY * i, text=label, anchor='w', fill='white', font='System 14 bold')

    # draw home button
    def drawButtons(mode, canvas):
        textX, textY = (mode.bx0 + mode.bx1) / 2, (mode.by0 + mode.by1) / 2
        canvas.create_image(textX, textY, image=ImageTk.PhotoImage(mode.homeButton))

    # draw background
    def drawBackground(mode, canvas):
        canvas.create_image(mode.width / 2, mode.height / 2, image=ImageTk.PhotoImage(mode.background))

    # draw press p to play message
    def drawPressP(mode, canvas):
        x0 = 100
        x1 = mode.width - 100
        y0 = mode.height / 2 - 50
        y1 = mode.height / 2 + 50
        canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='white', width=4)
        textX, textY = (x0 + x1) / 2, (y0 + y1) / 2
        canvas.create_text(textX, textY, text='Press "p" to play!', fill='white', font='System 18 bold')

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
        if not mode.playing and not mode.gameOver and mode.partsSet and mode.difficulty != None:
            mode.drawPressP(canvas)
        mode.drawButtons(canvas)