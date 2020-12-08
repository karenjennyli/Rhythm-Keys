from cmu_112_graphics import *

class HomeMode(Mode):
    def appStarted(mode):
        mode.initButtonDimensions()
        mode.initBackground()

    def initButtonDimensions(mode):
        pass

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
        
    def checkPressedButtons(mode, x, y):
        pass

    def drawButtons(mode, canvas):
        pass

    def initBackground(mode):
        # image from https://www.mobilebeat.com/wp-content/uploads/2016/07/Background-Music-768x576-1280x720.jpg
        mode.background = mode.scaleImage(mode.loadImage("pictures/homebackground.png"), 1/2)
    
    def drawBackground(mode, canvas):
        canvas.create_image(mode.width / 2, mode.height / 2, image=ImageTk.PhotoImage(mode.background))

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='black')
        mode.drawBackground(canvas)
        canvas.create_text(mode.width / 2, mode.height / 2,
                           text='Rhythm Keys!', fill='white')
        canvas.create_text(mode.width / 2, 100, text='press p to play, s to see scoreboard, c for create mode', fill='white')
        mode.drawButtons(canvas)
