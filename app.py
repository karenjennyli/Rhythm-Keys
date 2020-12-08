from cmu_112_graphics import *
from HomeMode import HomeMode
from PlayMode import PlayMode
from ScoreMode import ScoreMode
from CreateMode import CreateMode

class MyModalApp(ModalApp):
    def appStarted(app):
        app.HomeMode = HomeMode()
        app.PlayMode = PlayMode()
        app.CreateMode = CreateMode()
        app.ScoreMode = ScoreMode()
        # app.setActiveMode(app.HomeMode)
        app.setActiveMode(app.CreateMode)
        app.gameboards = dict()
        # write class CreateModeSong so we can save a list of Song objects so user can edit songs later

app = MyModalApp(width=1000, height=600)