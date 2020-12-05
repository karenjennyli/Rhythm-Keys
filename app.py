from cmu_112_graphics import *
from homeMode import homeMode
from singleMode import singleMode
from scoreMode import scoreMode

class MyModalApp(ModalApp):
    def appStarted(app):
        app.homeMode = homeMode()
        app.singleMode = singleMode()
        app.scoreMode = scoreMode()
        app.setActiveMode(app.homeMode)

app = MyModalApp(width=1000, height=600)