from cmu_112_graphics import *

class HomeMode(Mode):
    def appStarted(mode):
        mode.initButtonDimensions()
        mode.initBackground()

    def initButtonDimensions(mode):
        # mode.numberOfButtons = 5
        mode.buttonWidth = 60
        mode.buttonHeight = 30
        mode.bx0, mode.bx1 = 0, mode.buttonWidth
        mode.by0, mode.by1 = 0, mode.buttonHeight
        # mode.buttonCoordinates = []
        # for i in range(mode.numberOfButtons):
        #     x0 = i * mode.buttonWidth
        #     x1 = x0 + mode.buttonWidth
        #     mode.buttonCoordinates.append((x0, x1))
        # mode.buttonLabels = ['Home', 'Single', 'Create', 'Score']

    def keyPressed(mode, event):
        if event.key == 'p':
            mode.app.setActiveMode(mode.app.PlayMode)
        elif event.key == 's':
            mode.app.setActiveMode(mode.app.ScoreMode)

    def mousePressed(mode, event):
        x, y = event.x, event.y
        mode.checkPressedButtons(x, y)
        
    def checkPressedButtons(mode, x, y):
        # mode.modesList = [mode.app.HomeMode, mode.app.singleMode, mode.app.multiMode, mode.app.createMode, mode.app.scoreMode]
        # y0, y1 = mode.by0, mode.by1
        # for i in range(mode.numberOfButtons):
        #     x0, x1 = mode.buttonCoordinates[i]
        #     if x0 < x < x1 and y0 < y < y1:
        #         if i == 1:
        #             mode.appStarted()
        #             return
        #         mode.app.setActiveMode(mode.modesList[i])
        if mode.bx0 < x < mode.bx1 and mode.by0 < y < mode.by1:
            mode.app.setActiveMode(mode.app.HomeMode)

    def drawButtons(mode, canvas):
        canvas.create_rectangle(mode.bx0, mode.by0, mode.bx1, mode.by1, fill='black', outline='white', width=4)
        textX, textY = (mode.bx0 + mode.bx1) / 2, (mode.by0 + mode.by1) / 2
        canvas.create_text(textX, textY, text='Home', fill='white', font='System 14 bold')
        # for i in range(mode.numberOfButtons):
        #     x0, x1 = mode.buttonCoordinates[i]
        #     y0, y1 = mode.by0, mode.by1
        #     canvas.create_rectangle(x0, y0, x1, y1, fill='white')
        #     textX, textY = (x0 + x1) / 2, (y0 + y1) / 2
        #     canvas.create_text(textX, textY, text=mode.buttonLabels[i])

    def initBackground(mode):
        # image from https://www.mobilebeat.com/wp-content/uploads/2016/07/Background-Music-768x576-1280x720.jpg
        mode.background = mode.scaleImage(mode.loadImage("homebackground.png"), 1/2)
    
    def drawBackground(mode, canvas):
        canvas.create_image(mode.width / 2, mode.height / 2, image=ImageTk.PhotoImage(mode.background))

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='black')
        mode.drawBackground(canvas)
        canvas.create_text(mode.width / 2, mode.height / 2,
                           text='Rhythm Keys!', fill='white')
        canvas.create_text(mode.width / 2, 100, text='press p to play, s to see scoreboard', fill='white')
        mode.drawButtons(canvas)
