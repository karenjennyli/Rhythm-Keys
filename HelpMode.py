# ScoreMode class: mode for user to see the scoreboard with ranked scores
# from this session

from cmu_112_graphics import *

# HelpMode class
class HelpMode(Mode):
    def appStarted(mode):
        mode.initBackground()
        mode.initButtonDimensions()

    # home button dimensions
    def initButtonDimensions(mode):
        mode.buttonWidth = mode.buttonHeight = 40
        mode.bx0 = 10
        mode.bx1 = mode.bx0 + mode.buttonWidth
        mode.by0 = 10
        mode.by1 = mode.by0 + mode.buttonHeight
        mode.homeButton = mode.loadImage("pictures/home.png")

    def keyPressed(mode, event):
        pass

    def mousePressed(mode, event):
        x, y = event.x, event.y
        mode.checkPressedButtons(x, y)

    # check if home button is pressed
    def checkPressedButtons(mode, x, y):
        if mode.bx0 < x < mode.bx1 and mode.by0 < y < mode.by1:
            mode.app.setActiveMode(mode.app.HomeMode)

    # draw home button
    def drawButtons(mode, canvas):
        textX, textY = (mode.bx0 + mode.bx1) / 2, (mode.by0 + mode.by1) / 2
        canvas.create_image(textX, textY, image=ImageTk.PhotoImage(mode.homeButton))

    # get background image
    def initBackground(mode):
        # image from https://www.mobilebeat.com/wp-content/uploads/2016/07/Background-Music-768x576-1280x720.jpg
        mode.background = mode.scaleImage(mode.loadImage("pictures/homebackground.png"), 1/2)
    
    # draw background
    def drawBackground(mode, canvas):
        canvas.create_image(mode.width / 2, mode.height / 2, image=ImageTk.PhotoImage(mode.background))

    def drawInstructions(mode, canvas):
        msg = """Play Mode:
Choose the number of players you want, then which song you want to play from those listed.
If you are using a preset gameboard, you cannot choose which parts you want to play.
Otherwise, enter the part numbers that you want to play.
In the game, collect tokens (yellow circles), avoid skulls (obstacles), and hit the colorful targets.
In multiplayer, attack your opponents with the sword gamepieces on the board:
they'll disable your opponent's keys.

Create Mode:
Create a song and a gameboard at the same time!
Select the note or gamepiece type in the top palette and click the grid cells to add them.
Erase using the empty black square in the top palette.
If you mess up, create a new grid. You can also open an existing grid, or save the current grid.
Play your grid to see if you want to make changes!

Note: You can add more midi files to the music folder if you'd like!
The limitation is that the whole song must be one tempo though, so it works best with more simple songs!


Credit: home, skull, and sword icons made by Freepik from www.flaticon.com
"""
        canvas.create_text(60, 60, text=msg, fill='white', font='System 18 bold', anchor='nw')

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='black')
        mode.drawBackground(canvas)
        mode.drawButtons(canvas)
        mode.drawInstructions(canvas)