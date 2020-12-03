from cmu_112_graphics import *

class multiMode(Mode):
    def appStarted(mode):
        mode.initButtonDimensions()

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

    def keyPressed(mode, event):
        pass

    def mousePressed(mode, event):
        x, y = event.x, event.y
        mode.checkPressedButtons(x, y)

    def checkPressedButtons(mode, x, y):
        mode.modesList = [mode.app.homeMode, mode.app.singleMode, mode.app.multiMode, mode.app.createMode, mode.app.scoreMode]
        y0, y1 = mode.by0, mode.by1
        for i in range(mode.numberOfButtons):
            x0, x1 = mode.buttonCoordinates[i]
            if x0 < x < x1 and y0 < y < y1:
                mode.app.setActiveMode(mode.modesList[i])

    def drawButtons(mode, canvas):
        for i in range(mode.numberOfButtons):
            x0, x1 = mode.buttonCoordinates[i]
            y0, y1 = mode.by0, mode.by1
            canvas.create_rectangle(x0, y0, x1, y1, fill='white')
            print(x0, x1, y0, y1)
            textX, textY = (x0 + x1) / 2, (y0 + y1) / 2
            canvas.create_text(textX, textY, text=mode.buttonLabels[i])

    def redrawAll(mode, canvas):
        canvas.create_text(mode.width / 2, mode.height / 2, 
                           text='Multiplayer Mode!')
        mode.drawButtons(canvas)