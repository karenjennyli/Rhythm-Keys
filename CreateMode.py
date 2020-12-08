# CreateMode class: a mode that allows the player to create and save 
# a gameboard using different notes, tokens, obstacles, and attacks

from cmu_112_graphics import *
from music21 import *
import pygame, os

class CreateMode(Mode):
    def appStarted(mode):
        mode.finished = False
        mode.saving = False
        mode.noNotesMessage = False
        mode.initDimensions()
        mode.initBackground()
        mode.initButtonDimensions()
        mode.initPalette()
        mode.initGrid()
        mode.initPageButtons()
        mode.initNoteSounds()
    
    def modeActivated(mode):
        mode.appStarted()

    # initialize the music grid
    def initGrid(mode):
        mode.pages = 1
        mode.grid = dict()
        for col in range(mode.cols):
            mode.grid[col] = ['0' for i in range(mode.pageLength)]
        mode.currentPage = 0
    
    # buttons to change current page
    def initPageButtons(mode):
        pass
        
    # initialize the different note sounds
    def initNoteSounds(mode):
        pygame.init()
        mode.soundsDict = dict()
        mode.soundsDict['C'] = pygame.mixer.Sound("mp3 Notes/c4.mp3")
        mode.soundsDict['C#'] = pygame.mixer.Sound("mp3 Notes/c-4.mp3")
        mode.soundsDict['D'] = pygame.mixer.Sound("mp3 Notes/d4.mp3")
        mode.soundsDict['D#'] = pygame.mixer.Sound("mp3 Notes/d-4.mp3")
        mode.soundsDict['E'] = pygame.mixer.Sound("mp3 Notes/e4.mp3")
        mode.soundsDict['F'] = pygame.mixer.Sound("mp3 Notes/f4.mp3")
        mode.soundsDict['F#'] = pygame.mixer.Sound("mp3 Notes/f-4.mp3")
        mode.soundsDict['G'] = pygame.mixer.Sound("mp3 Notes/g4.mp3")
        mode.soundsDict['G#'] = pygame.mixer.Sound("mp3 Notes/g-4.mp3")
        mode.soundsDict['A'] = pygame.mixer.Sound("mp3 Notes/a5.mp3")
        mode.soundsDict['A#'] = pygame.mixer.Sound("mp3 Notes/a-5.mp3")
        mode.soundsDict['B'] = pygame.mixer.Sound("mp3 Notes/b5.mp3")

    # add a new page to the grid
    def newPage(mode):
        mode.pages += 1
        for col in range(mode.cols):
            newList = ['0' for i in range(mode.pageLength)]
            mode.grid[col].extend(newList)
    
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
        mode.notes = ['c4', 'c_4', 'd4', 'd_4', 'e4', 'f4', 'f_4', 'g4', 'g_4', 'a4', 'a_4', 'b4']
        mode.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        mode.notesDict = dict()
        for i in range(len(mode.notes)):
            note = mode.notes[i]
            color = mode.colors[i]
            mode.notesDict[note] = color
        for i in range(len(mode.colors)):
            x0 = mode.PaletteSideOffset + i * mode.colorWidth
            x1 = x0 + mode.colorWidth
            y0 = mode.PaletteTopOffset
            y1 = y0 + mode.colorHeight
            note = mode.notes[i]
            color = mode.colors[i]
            mode.colorCoords[note] = (x0, y0, x1, y1, color)
        
        mode.currentNote = 'C'

    # button dimensions
    def initButtonDimensions(mode):
        mode.buttonWidth = mode.buttonHeight = 40
        mode.bx0 = 10
        mode.bx1 = mode.bx0 + mode.buttonWidth
        mode.by0 = 10
        mode.by1 = mode.by0 + mode.buttonHeight
        mode.homeButton = mode.loadImage("pictures/home.png")

    # plays the current song on the grid
    def playGrid(mode):
        pass
        # play mode

    def keyPressed(mode, event):
        if event.key == 'Left' and mode.currentPage > 0:
            mode.currentPage -= 1
        elif event.key == 'Right':
            mode.currentPage += 1
            if mode.currentPage >= mode.pages:
                mode.newPage()
        elif event.key == 'n':
            mode.appStarted()
        elif event.key == 'd':
            mode.saving = True
            mode.createMidi()
            mode.createTxt()
        elif event.key == 'p':
            mode.playGrid()

    def mousePressed(mode, event):
        x, y = event.x, event.y
        mode.checkPressedButtons(x, y)
        mode.checkPressedPalette(x, y)
        mode.checkPressedGrid(x, y)

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
                sound = mode.soundsDict[note]
                pygame.mixer.Sound.play(sound)
                return
    # check if grid is pressed
    def checkPressedGrid(mode, x, y):
        col = int((y - mode.gridTopOffset) // mode.colorHeight)
        row = int((x - mode.gridSideOffset) // mode.colorWidth)
        if not (0 <= col <= 4 and 0 <= row < mode.pageLength):
            return
        sound = mode.soundsDict[mode.currentNote]
        pygame.mixer.Sound.play(sound)
        row += mode.currentPage * mode.pageLength
        colList = mode.grid[col]
        colList[row] = mode.currentNote

    # create and save a midi file from the current grid
    def createMidi(mode):
        mode.removeWhiteSpace()
        if mode.grid[0] == []:
            mode.noNotesMessage = True
            return
        mode.songName = None
        while mode.songName == None or (mode.songName + '.mid' in os.listdir('music')):
            mode.songName = mode.getUserInput('Enter valid song name.')
            if mode.songName == None:
                return
        mode.stream = stream.Stream()
        for i in range(len(mode.grid[0])):
            notes = set()
            for col in mode.grid:
                colList = mode.grid[col]
                elem = colList[i]
                notes.add(elem)
            notesList = list(notes)
            if notesList == ['0']:
                newNote = note.Rest(type='eighth') # add a rest if there's no notes
            elif len(notesList) == 1:
                elem = notesList[0]
                noteNotation = elem + '4'
                newNote = note.Note(noteNotation, type='eighth')
            else:
                chordList = []
                for elem in notesList:
                    if elem != '0':
                        noteNotation = elem + '4'
                        chordList.append(noteNotation)
                newNote = chord.Chord(chordList, type='eighth')
            mode.stream.append(newNote)
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
        path = 'grids'
        file = mode.songName + '.txt'
        with open(os.path.join(path, file), 'w') as fp:
            fp.write(text)

    # draw home buttpn
    def drawButtons(mode, canvas):
        textX, textY = (mode.bx0 + mode.bx1) / 2, (mode.by0 + mode.by1) / 2
        canvas.create_image(textX, textY, image=ImageTk.PhotoImage(mode.homeButton))

    # get the background image
    def initBackground(mode):
        # image from https://www.mobilebeat.com/wp-content/uploads/2016/07/Background-Music-768x576-1280x720.jpg
        mode.background = mode.scaleImage(mode.loadImage("pictures/homebackground.png"), 1/2)
    
    # create mode dimensions
    def initDimensions(mode):
        mode.cols = 5
        mode.pageLength = 24
        mode.colorWidth = mode.colorHeight = (mode.width - 25) / mode.pageLength
        mode.gridTopOffset = mode.height / 2 - mode.colorHeight * mode.cols / 2
        mode.gridSideOffset = mode.width / 2 - mode.colorWidth * mode.pageLength / 2
        mode.PaletteSideOffset = 300
        mode.PaletteTopOffset = 10

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
            canvas.create_text(textX, textY, text=note, fill='white', font='System 18 bold')

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
                canvas.create_text(textX, textY, text=labelText, fill='white', font='System 18 bold')
    
    # draw current note/object selected from palette
    def drawCursor(mode, canvas):
        x1 = mode.width
        x0 = x1 - mode.colorWidth
        y0 = 0
        y1 = y0 + mode.colorHeight
        color = mode.notesDict[mode.currentNote]
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='white', width=3)
        textX = (x0 + x1) / 2
        textY = (y0 + y1) / 2
        canvas.create_text(textX, textY, text=mode.currentNote, fill='white', font='System 18 bold')

    # draw the current page of the grid
    def drawCurrentPage(mode, canvas):
        textX = mode.width / 2
        textY = mode.gridTopOffset - 25
        canvas.create_text(textX, textY, text=f'Page {mode.currentPage + 1} of {mode.pages}', fill='white', font='System 18 bold')

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
        canvas.create_text(mode.width / 2, mode.height / 2 + 15, text=f'Press "n" to create new song.', fill='white', font='System 18 bold')

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
        canvas.create_text(mode.width / 2, mode.height / 2 + 15, text=f'Press "n" to create new song.', fill='white', font='System 18 bold')

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='black')
        mode.drawBackground(canvas)
        mode.drawButtons(canvas)
        mode.drawPalette(canvas)
        if not mode.saving:
            mode.drawGrid(canvas)
            mode.drawCurrentPage(canvas)
        mode.drawCursor(canvas)
        if mode.noNotesMessage:
            mode.drawNoNotesMessage(canvas)
        if mode.finished:
            mode.drawFinishedMessage(canvas)