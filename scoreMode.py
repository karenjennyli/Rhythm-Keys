from cmu_112_graphics import *
from Score import Score

class scoreMode(Mode):
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
            textX, textY = (x0 + x1) / 2, (y0 + y1) / 2
            canvas.create_text(textX, textY, text=mode.buttonLabels[i])

    def drawScoreboard(mode, canvas):
        startY = 100
        intervalY = 50
        rankX = 50
        playerX = rankX + 100
        scoreX = playerX + 100
        difficultyX = scoreX + 100
        songX = difficultyX + 100
        textXs = [rankX, playerX, scoreX, difficultyX, songX]
        attributes = ['Place', 'Player', 'Score', 'Difficulty', 'Song']
        for i in range(len(textXs)):
            textX = textXs[i]
            canvas.create_text(textX, startY, text=f'{attributes[i]}', anchor='w')
        if Score.scoreboard == []:
            canvas.create_text(mode.width / 2, mode.height / 2, text='No scores added yet!')
            return
        for i in range(len(Score.scoreboard)):
            score = Score.scoreboard[i]
            textY = startY + intervalY * (i + 1)
            for j in range(len(textXs)):
                textX = textXs[j]
                canvas.create_text(textX, textY, text=f'{score.attributes[j]}', anchor='w')

    def redrawAll(mode, canvas):
        mode.drawScoreboard(canvas)
        mode.drawButtons(canvas)