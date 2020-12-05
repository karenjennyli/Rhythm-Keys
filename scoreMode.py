from cmu_112_graphics import *
from Score import Score

class scoreMode(Mode):
    def appStarted(mode):
        mode.initBackground()
        mode.initButtonDimensions()

    def initButtonDimensions(mode):
        mode.buttonWidth = mode.buttonHeight = 40
        mode.bx0 = 10
        mode.bx1 = mode.bx0 + mode.buttonWidth
        mode.by0 = 10
        mode.by1 = mode.by0 + mode.buttonHeight
        mode.homeButton = mode.loadImage("home.png")

    def keyPressed(mode, event):
        pass

    def mousePressed(mode, event):
        x, y = event.x, event.y
        mode.checkPressedButtons(x, y)

    def checkPressedButtons(mode, x, y):
        if mode.bx0 < x < mode.bx1 and mode.by0 < y < mode.by1:
            mode.app.setActiveMode(mode.app.homeMode)

    def drawButtons(mode, canvas):
        textX, textY = (mode.bx0 + mode.bx1) / 2, (mode.by0 + mode.by1) / 2
        canvas.create_image(textX, textY, image=ImageTk.PhotoImage(mode.homeButton))

    def initBackground(mode):
        # image from https://www.mobilebeat.com/wp-content/uploads/2016/07/Background-Music-768x576-1280x720.jpg
        mode.background = mode.scaleImage(mode.loadImage("homebackground.png"), 1/2)
    
    def drawBackground(mode, canvas):
        canvas.create_image(mode.width / 2, mode.height / 2, image=ImageTk.PhotoImage(mode.background))

    def drawScoreboard(mode, canvas):
        startY = 100
        canvas.create_text(mode.width / 2, startY, text='Scoreboard', fill='white', font='System 36 bold')
        startY += 50
        intervalY = 30
        rankX = 100
        intervalX = 150
        playerX = rankX + intervalX
        scoreX = playerX + intervalX
        difficultyX = scoreX + intervalX
        songX = difficultyX + intervalX
        textXs = [rankX, playerX, scoreX, difficultyX, songX]
        # if Score.scoreboard == []:
        #     canvas.create_text(mode.width / 2, mode.height / 2, text='No scores added yet!', fill='white', font='System 18 bold')
        #     return
        attributes = ['Place', 'Player', 'Score', 'Difficulty', 'Song']
        for i in range(len(textXs)):
            textX = textXs[i]
            canvas.create_text(textX, startY, text=f'{attributes[i]}', anchor='w', fill='white', font='System 24 bold')
        for i in range(len(Score.scoreboard)):
            score = Score.scoreboard[i]
            textY = startY + intervalY * (i + 1)
            for j in range(len(textXs)):
                textX = textXs[j]
                canvas.create_text(textX, textY, text=f'{score.attributes[j]}', anchor='w', fill='white', font='System 18 bold')

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='black')
        mode.drawBackground(canvas)
        mode.drawScoreboard(canvas)
        mode.drawButtons(canvas)