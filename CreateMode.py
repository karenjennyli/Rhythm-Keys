# CreateMode class: a mode that allows the player to create and save 
# a gameboard using different notes, tokens, obstacles, and attacks
# User can also open existing gameboards/grids

from cmu_112_graphics import *
from music21 import *
import pygame, os, time

class CreateMode(Mode):
    def appStarted(mode):
        mode.timerDelay = 10
        mode.finished = False
        mode.saving = False
        mode.noNotesMessage = False
        mode.bpm = 120
        mode.timeInterval = 60 * 1000 / mode.bpm / 2 # since each is 1/8 note
        mode.playing = False
        mode.displayFiles = False
        mode.initDimensions()
        mode.initBackground()
        mode.initButtonDimensions()
        mode.initPalette()
        mode.initGrid()
        mode.initCreateButtons()
        mode.initNoteSounds()
    
    def modeActivated(mode):
        mode.appStarted()

    ###############################################
    # Initializing
    ###############################################

    # create mode dimensions
    def initDimensions(mode):
        mode.cols = 5
        mode.pageLength = 24
        mode.colorWidth = mode.colorHeight = (mode.width - 25) / mode.pageLength
        mode.eraserLength = mode.colorWidth * 0.9
        mode.gridTopOffset = mode.height / 2 - mode.colorHeight * mode.cols / 2
        mode.gridSideOffset = mode.width / 2 - mode.colorWidth * mode.pageLength / 2
        mode.numberOfLetters = 16
        mode.PaletteSideOffset = mode.width / 2 - mode.colorWidth * mode.numberOfLetters / 2
        mode.PaletteTopOffset = 20

    # get the background image
    def initBackground(mode):
        # image from https://www.mobilebeat.com/wp-content/uploads/2016/07/Background-Music-768x576-1280x720.jpg
        mode.background = mode.scaleImage(mode.loadImage("pictures/homebackground.png"), 1/2)
    
    # button dimensions
    def initButtonDimensions(mode):
        mode.buttonWidth = mode.buttonHeight = 40
        mode.bx0 = 10
        mode.bx1 = mode.bx0 + mode.buttonWidth
        mode.by0 = 10
        mode.by1 = mode.by0 + mode.buttonHeight
        # https://www.flaticon.com/
        mode.homeButton = mode.loadImage("pictures/home.png")

    # create mode buttons
    def initCreateButtons(mode):
        # buttons: new, open, save, play/stop, left, right
        mode.buttonText = ['New', 'Open', 'Save', 'Play', '←', '→']
        mode.buttonCoords = []
        width = 75
        height = 35
        margin = 20
        sideOffset = mode.width / 2 - margin / 2 - width - margin - width
        topOffset = 100
        numberOfButtons = 4
        for i in range(numberOfButtons):
            bx0 = sideOffset + i * width + margin * i
            bx1 = bx0 + width
            by0 = topOffset
            by1 = topOffset + height
            mode.buttonCoords.append((bx0, bx1, by0, by1))
        width = height = 25
        bx0 = mode.width / 4 + 10
        bx1 = bx0 + width
        by0 = mode.gridTopOffset - 35
        by1 = by0 + height
        mode.buttonCoords.append((bx0, bx1, by0, by1))
        bx1 = mode.width * 3 / 4 - 10
        bx0 = bx1 - width
        mode.buttonCoords.append((bx0, bx1, by0, by1))

    # creates the note "Palette" at the top of the screen
    def initPalette(mode):
        mode.colors = ['maroon',
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
        mode.colorCoords = dict()
        mode.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        mode.gamepieces = ['T', 'O', '@', 'X']
        mode.paletteLetters = mode.notes + mode.gamepieces
        mode.colors = mode.colors + ['black' for i in range(len(mode.gamepieces))]
        mode.notesDict = dict()
        for i in range(len(mode.paletteLetters)):
            letter = mode.paletteLetters[i]
            color = mode.colors[i]
            mode.notesDict[letter] = color
        for i in range(len(mode.colors)):
            x0 = mode.PaletteSideOffset + i * mode.colorWidth
            x1 = x0 + mode.colorWidth
            y0 = mode.PaletteTopOffset
            y1 = y0 + mode.colorHeight
            letter = mode.paletteLetters[i]
            color = mode.colors[i]
            mode.colorCoords[letter] = (x0, y0, x1, y1, color)
        mode.currentNote = 'C'

    # initialize the music grid
    def initGrid(mode):
        mode.pages = 1
        mode.grid = dict()
        for col in range(mode.cols):
            mode.grid[col] = ['0' for i in range(mode.pageLength)]
        mode.currentPage = 0
    
    # initialize the different note sounds
    def initNoteSounds(mode):
        pygame.init()
        mode.soundsDict = dict()
        # audio files from:
        # https://www.reddit.com/r/piano/comments/3u6ke7/heres_some_midi_and_mp3_files_for_individual/
        mode.soundsDict['C'] = pygame.mixer.Sound("mp3 notes/c4.mp3")
        mode.soundsDict['C#'] = pygame.mixer.Sound("mp3 notes/c-4.mp3")
        mode.soundsDict['D'] = pygame.mixer.Sound("mp3 notes/d4.mp3")
        mode.soundsDict['D#'] = pygame.mixer.Sound("mp3 notes/d-4.mp3")
        mode.soundsDict['E'] = pygame.mixer.Sound("mp3 notes/e4.mp3")
        mode.soundsDict['F'] = pygame.mixer.Sound("mp3 notes/f4.mp3")
        mode.soundsDict['F#'] = pygame.mixer.Sound("mp3 notes/f-4.mp3")
        mode.soundsDict['G'] = pygame.mixer.Sound("mp3 notes/g4.mp3")
        mode.soundsDict['G#'] = pygame.mixer.Sound("mp3 notes/g-4.mp3")
        mode.soundsDict['A'] = pygame.mixer.Sound("mp3 notes/a5.mp3")
        mode.soundsDict['A#'] = pygame.mixer.Sound("mp3 notes/a-5.mp3")
        mode.soundsDict['B'] = pygame.mixer.Sound("mp3 notes/b5.mp3")
    
    # add a new page to the grid
    def newPage(mode):
        mode.pages += 1
        for col in range(mode.cols):
            newList = ['0' for i in range(mode.pageLength)]
            mode.grid[col].extend(newList)
    
    ###############################################
    # Checking for events
    ###############################################

    def timerFired(mode):
        if mode.playing:
            try:
                dt = time.time() - mode.startTime
            except:
                return
            mode.currentIndex = int(dt * 1000 / mode.timeInterval)
            if mode.currentIndex >= mode.pages * mode.pageLength:
                mode.playing = False
                return
            if not mode.playedOrNot[mode.currentIndex]:
                mode.playedOrNot[mode.currentIndex] = True
                for note in mode.stream[mode.currentIndex]:
                    sound = mode.soundsDict[note]
                    pygame.mixer.Sound.play(sound)

    def keyPressed(mode, event):
        return
        if event.key == 'Left' and mode.currentPage > 0:
            mode.currentPage -= 1
        elif event.key == 'Right':
            mode.currentPage += 1
            if mode.currentPage >= mode.pages and not mode.playing:
                mode.newPage()
            elif mode.currentPage >= mode.pages:
                mode.currentPage -= 1
        elif event.key == 'n':
            mode.appStarted()
        elif event.key == 'd':
            mode.saving = True
            mode.createMidi()
            mode.createTxt()
        elif event.key == 'p':
            mode.playGrid()
        elif event.key == 's':
            mode.playing = False
        elif event.key == 'o':
            mode.getFiles()
            mode.displayFiles = True
            mode.getGrid()

    def mousePressed(mode, event):
        x, y = event.x, event.y
        mode.checkPressedButtons(x, y)
        mode.checkPressedPalette(x, y)
        mode.checkPressedGrid(x, y)
        mode.checkPressedCreateButtons(x, y)

    # check if create buttons are pressed
    def checkPressedCreateButtons(mode, x, y):
        mode.buttonText = ['New', 'Open', 'Save', 'Play', '←', '→']
        for i in range(len(mode.buttonCoords)):
            bx0, bx1, by0, by1 = mode.buttonCoords[i]
            if bx0 < x < bx1 and by0 < y < by1:
                if i == 0:
                    mode.appStarted()
                elif i == 1:
                    mode.getFiles()
                    mode.displayFiles = True
                    mode.getGrid()
                elif i == 2:
                    mode.saving = True
                    mode.createMidi()
                    mode.createTxt()
                elif i == 3:
                    if mode.playing:
                        mode.playing = False
                    else:
                        mode.playing = True
                        mode.playGrid()
                elif i == 4 and mode.currentPage > 0:
                    mode.currentPage -= 1
                elif i == 5:
                    mode.currentPage += 1
                    if mode.currentPage >= mode.pages and not mode.playing:
                        mode.newPage()
                    elif mode.currentPage >= mode.pages:
                        mode.currentPage -= 1

    # check if home button is pressed
    def checkPressedButtons(mode, x, y):
        if mode.bx0 < x < mode.bx1 and mode.by0 < y < mode.by1:
            mode.app.setActiveMode(mode.app.HomeMode)

    # check if note Palette is pressed
    def checkPressedPalette(mode, x, y):
        for note in mode.colorCoords:
            x0, y0, x1, y1, color = mode.colorCoords[note]
            if x0 < x < x1 and y0 < y < y1:
                mode.currentNote = note
                if note in mode.gamepieces:
                    return
                sound = mode.soundsDict[note]
                pygame.mixer.Sound.play(sound)
                return
   
    # check if grid is pressed
    def checkPressedGrid(mode, x, y):
        col = int((y - mode.gridTopOffset) // mode.colorHeight)
        row = int((x - mode.gridSideOffset) // mode.colorWidth)
        if not (0 <= col <= 4 and 0 <= row < mode.pageLength):
            return
        if mode.currentNote not in mode.gamepieces:
            sound = mode.soundsDict[mode.currentNote]
            pygame.mixer.Sound.play(sound)
        if mode.currentNote == 'X':
            newNote = '0'
        else:
            newNote = mode.currentNote
        row += mode.currentPage * mode.pageLength
        colList = mode.grid[col]
        colList[row] = newNote

    ###############################################
    # Play grid
    ###############################################

     # plays the current song on the grid
    def playGrid(mode):
        if not mode.getMusicStream():
            return
        mode.playing = True
        mode.currentIndex = 0
        mode.startTime = time.time()

    def getMusicStream(mode):
        mode.stream = []
        containsNotes = False
        for i in range(len(mode.grid[0])):
            notes = set()
            for col in mode.grid:
                colList = mode.grid[col]
                elem = colList[i]
                if elem in mode.gamepieces:
                    continue
                notes.add(elem)
            notesList = list(notes)
            if '0' in notesList:
                notesList.remove('0')
            if notesList == []:
                mode.stream.append([])
            else:
                mode.stream.append(notesList)
                containsNotes = True
        mode.playedOrNot = [False for i in range(len(mode.stream))]
        return containsNotes

    ###############################################
    # Creating/retreiving text and midi files
    ###############################################

    # remove empty grid cells at the end of the grid
    def removeWhiteSpace(mode):
        gridLength = len(mode.grid[0])
        i = gridLength - 1
        containsNotes = False
        while not containsNotes and i >= 0:
            for col in mode.grid:
                colList = mode.grid[col]
                if colList[i] != '0':
                    containsNotes = True
                    return
            if not containsNotes:
                for col in mode.grid:
                    colList = mode.grid[col]
                    colList.pop()
                i -= 1
            
    # create and save a midi file from the current grid
    def createMidi(mode):
        mode.removeWhiteSpace()
        if mode.grid[0] == []:
            mode.noNotesMessage = True
            return
        mode.songName = None
        # while mode.songName == None or (mode.songName + '.mid' in os.listdir('music')):
        while mode.songName == None:
            mode.songName = mode.getUserInput('Enter valid song name.')
            if mode.songName == None:
                return
        mode.stream = stream.Stream()
        containsNotes = False
        for i in range(len(mode.grid[0])):
            notes = set()
            for col in mode.grid:
                colList = mode.grid[col]
                elem = colList[i]
                if elem in mode.gamepieces:
                    continue
                notes.add(elem)
            notesList = list(notes)
            if notesList == ['0'] or notesList == []:
                newNote = note.Rest(type='eighth') # add a rest if there's no notes
            elif len(notesList) == 1:
                elem = notesList[0]
                noteNotation = elem + '4'
                newNote = note.Note(noteNotation, type='eighth')
                containsNotes = True
            else:
                chordList = []
                for elem in notesList:
                    if elem != '0':
                        noteNotation = elem + '4'
                        chordList.append(noteNotation)
                newNote = chord.Chord(chordList, type='eighth')
                containsNotes = True
            mode.stream.append(newNote)
        if not containsNotes:
            mode.noNotesMessage = True
            return
        midiFromStream = midi.translate.streamToMidiFile(mode.stream)
        mode.stream.write('midi', 'music/' + mode.songName + '.mid')
        mode.finished = True

    # create and save a text file for the gameboard on the grid
    def createTxt(mode):
        if mode.grid[0] == [] or mode.songName == None:
            return
        text = ''
        for col in mode.grid:
            colList = mode.grid[col]
            for note in colList:
                text += note + ' '
            text += '\n'
        text = text[:-1]
        # referenced for writing files
        # https://www.geeksforgeeks.org/create-an-empty-file-using-python/
        path = 'gameboards'
        file = mode.songName + '.txt'
        with open(os.path.join(path, file), 'w') as fp:
            fp.write(text)

    # retrieve grid from text file
    def getGrid(mode):
        index = None
        while index == None or index not in range(len(mode.filesInFolder)):
            inputString = mode.getUserInput('Enter grid number.')
            if inputString == None:
                mode.displayFiles = False
                return
            try:
                index = int(inputString)
            except:
                continue
        textFileName = 'gameboards/' + mode.filesInFolder[index]
        textFile = open(textFileName, 'r')
        textGrid = textFile.read()
        gridList = textGrid.splitlines()
        mode.grid = dict()
        for i in range(len(gridList)):
            mode.grid[i] = gridList[i].split(' ')
            mode.grid[i].pop()
        mode.pages = len(mode.grid[0]) // mode.pageLength + 1
        mode.currentPage = 0
        missingRows = mode.pageLength - len(mode.grid[0]) % mode.pageLength
        newRows = ['0' for i in range(missingRows)]
        for col in mode.grid:
            mode.grid[col].extend(newRows)
        mode.displayFiles = False

    ###############################################
    # Drawing
    ###############################################

    # draw create mode buttons
    def drawCreateButtons(mode, canvas):
        for i in range(len(mode.buttonCoords)):
            bx0, bx1, by0, by1 = mode.buttonCoords[i]
            canvas.create_rectangle(bx0, by0, bx1, by1, fill='black', outline='white', width=3)
            textX, textY = (bx0 + bx1) / 2, (by0 + by1) / 2
            if mode.buttonText[i] == 'Play' and mode.playing:
                mode.buttonText[i] = 'Stop'
            elif mode.buttonText[i] == 'Stop' and not mode.playing:
                mode.buttonText[i] = 'Play'
            canvas.create_text(textX, textY, text=mode.buttonText[i], font='System 18 bold', fill='white')
        
    # draw home buttpn
    def drawButtons(mode, canvas):
        textX, textY = (mode.bx0 + mode.bx1) / 2, (mode.by0 + mode.by1) / 2
        canvas.create_image(textX, textY, image=ImageTk.PhotoImage(mode.homeButton))

    # draw background image
    def drawBackground(mode, canvas):
        canvas.create_image(mode.width / 2, mode.height / 2, image=ImageTk.PhotoImage(mode.background))

    # draw note palette at top of screen
    def drawPalette(mode, canvas):
        for note in mode.colorCoords:
            x0, y0, x1, y1, color = mode.colorCoords[note]
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='white', width=3)
            textX = (x0 + x1) / 2
            textY = (y0 + y1) / 2
            if note == 'X':
                continue
            elif note == 'T':
                color = 'gold'
            else:
                color = 'white'
            canvas.create_text(textX, textY, text=note, fill=color, font='System 18 bold')
        x0, y0, x1, y1, color = mode.colorCoords[mode.currentNote]
        canvas.create_rectangle(x0, y0, x1, y1, outline='white', width=6)

    # draw grid with all the notes, tokens, other objects, etc
    def drawGrid(mode, canvas):
        start = mode.currentPage * mode.pageLength
        end = start + mode.pageLength
        if mode.grid[0] == []:
            return
        for col in mode.grid:
            colList = mode.grid[col]
            for index in range(start, end):
                i = index - start
                x0 = mode.gridSideOffset + i * mode.colorWidth
                x1 = x0 + mode.colorWidth
                y0 = mode.gridTopOffset + col * mode.colorHeight
                y1 = y0 + mode.colorHeight
                note = colList[index]
                if note == '0':
                    color = 'black'
                    labelText = ''
                else:
                    color = mode.notesDict[note]
                    labelText = note
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='white', width=3)
                textX = (x0 + x1) / 2
                textY = (y0 + y1) / 2
                if note == 'T':
                    textColor = 'gold'
                else:
                    textColor = 'white'
                canvas.create_text(textX, textY, text=labelText, fill=textColor, font='System 18 bold')
    
    # draw the current page of the grid
    def drawCurrentPage(mode, canvas):
        textX = mode.width / 2
        textY = mode.gridTopOffset - 35
        canvas.create_text(textX, textY, text=f'Page {mode.currentPage + 1} of {mode.pages}', fill='white', font='System 24 bold', anchor='n')

    # draw message to tell user there are no notes added to the grid
    def drawNoNotesMessage(mode, canvas):
        boxWidth = 400
        boxHeight = 200
        x0 = mode.width / 2 - boxWidth / 2
        x1 = x0 + boxWidth
        y0 = mode.height / 2 - boxHeight / 2
        y1 = y0 + boxHeight
        canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='white', width=4)
        canvas.create_text(mode.width / 2, mode.height / 2 - 15, text=f'No notes to create a song.', fill='white', font='System 18 bold')
        canvas.create_text(mode.width / 2, mode.height / 2 + 15, text=f'Press "New" to create new song.', fill='white', font='System 18 bold')

    # draw message that midi and text files were saved
    def drawFinishedMessage(mode, canvas):
        boxWidth = 400
        boxHeight = 200
        x0 = mode.width / 2 - boxWidth / 2
        x1 = x0 + boxWidth
        y0 = mode.height / 2 - boxHeight / 2
        y1 = y0 + boxHeight
        canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='white', width=4)
        canvas.create_text(mode.width / 2, mode.height / 2 - 15, text=f'{mode.songName} added to music library!', fill='white', font='System 18 bold')
        canvas.create_text(mode.width / 2, mode.height / 2 + 15, text=f'Press "New" to create new song.', fill='white', font='System 18 bold')

    def drawHelp(mode, canvas):
        msg3 = '"T" = token, "O" = obstacle, "@" = attack'
        canvas.create_text(mode.width / 2, mode.height - 140, text=msg3, font='System 18 bold italic', fill='white')

    def getFiles(mode):
        mode.filesInFolder = os.listdir('gameboards')

    def drawFiles(mode, canvas):
        x0 = mode.width / 2
        x1 = mode.width
        y0 = 0
        y1 = mode.height
        canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='white', width=4)
        startY = 50
        canvas.create_text(mode.width * 3 / 4, startY, text='Grid Options', fill='white', font='System 24 bold')
        startY += 50
        intervalY = 20
        numberX = mode.width / 2 + 50
        nameX = numberX + 50
        for i in range(len(mode.filesInFolder)):
            fileName = mode.filesInFolder[i]
            name = fileName.split('.')[0]
            canvas.create_text(numberX, startY + intervalY * i, text=str(i), anchor='w', fill='white', font='System 14 bold')
            canvas.create_text(nameX, startY + intervalY * i, text=name, anchor='w', fill='white', font='System 14 bold')

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='black')
        mode.drawBackground(canvas)
        mode.drawButtons(canvas)
        mode.drawPalette(canvas)
        mode.drawCreateButtons(canvas)
        mode.drawHelp(canvas)
        if not mode.saving:
            mode.drawGrid(canvas)
            mode.drawCurrentPage(canvas)
        if mode.noNotesMessage:
            mode.drawNoNotesMessage(canvas)
        if mode.finished:
            mode.drawFinishedMessage(canvas)
        if mode.displayFiles:
            mode.drawFiles(canvas)