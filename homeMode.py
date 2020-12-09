# HomeMode class: home screen that allows user to navigate through the game

from cmu_112_graphics import *

# HomeMode class
class HomeMode(Mode):
    def appStarted(mode):
        mode.initButtonDimensions()
        mode.initBackground()

    # button dimensions
    def initButtonDimensions(mode):
        mode.buttonCoords = []
        numberOfButtons = 3
        width = 100
        height = 50
        margin = 20
        sideOffset = mode.width / 2 - width / 2 - margin - width
        topOffset = mode.height / 2
        for i in range(numberOfButtons):
            bx0 = sideOffset + i * width + margin * i
            bx1 = bx0 + width
            by0 = topOffset
            by1 = topOffset + height
            mode.buttonCoords.append((bx0, bx1, by0, by1))
        width = 50
        height = 20
        bx1 = mode.width - 20
        bx0 = bx1 - width
        by1 = mode.height - 20
        by0 = by1 - width
        mode.buttonCoords.append((bx0, bx1, by0, by1))
        mode.buttonText = ['Play', 'Create', 'Scores', 'Help']
        mode.buttonModes = [mode.app.PlayMode, mode.app.CreateMode, mode.app.ScoreMode, mode.app.HelpMode]

    def keyPressed(mode, event):
        if event.key == 'p':
            mode.app.setActiveMode(mode.app.PlayMode)
        elif event.key == 's':
            mode.app.setActiveMode(mode.app.ScoreMode)
        elif event.key == 'c':
            mode.app.setActiveMode(mode.app.CreateMode)

    def mousePressed(mode, event):
        x, y = event.x, event.y
        mode.checkPressedButtons(x, y)

    # check if buttons are pressed
    def checkPressedButtons(mode, x, y):
        for i in range(len(mode.buttonCoords)):
            bx0, bx1, by0, by1 = mode.buttonCoords[i]
            if bx0 < x < bx1 and by0 < y < by1:
                mode.app.setActiveMode(mode.buttonModes[i])

    # draw buttons
    def drawButtons(mode, canvas):
        for i in range(len(mode.buttonCoords)):
            bx0, bx1, by0, by1 = mode.buttonCoords[i]
            if i != 3:
                canvas.create_rectangle(bx0, by0, bx1, by1, fill='black', outline='white', width=4)
                style = 'System 24 bold'
            else:
                style = 'System 18 bold'
            textX, textY = (bx0 + bx1) / 2, (by0 + by1) / 2
            canvas.create_text(textX, textY, text=mode.buttonText[i], font=style, fill='white')

    # retreive background image
    def initBackground(mode):
        # image from https://www.mobilebeat.com/wp-content/uploads/2016/07/Background-Music-768x576-1280x720.jpg
        mode.background = mode.scaleImage(mode.loadImage("pictures/homebackground.png"), 1/2)
    
    # draw background
    def drawBackground(mode, canvas):
        canvas.create_image(mode.width / 2, mode.height / 2, image=ImageTk.PhotoImage(mode.background))

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='black')
        mode.drawBackground(canvas)
        canvas.create_text(mode.width / 2, mode.height / 3,
                           text='Rhythm Keys!', fill='white', font='System 48 bold')
        mode.drawButtons(canvas)
