from cmu_graphics import *
from os import path
from typing import Union
from helpers import ResponsiveGeometry
from code_snippet import CodeSnippet
from info_display import InfoDisplay
from checkers import Checker


def setBackgroundColor(app, color: Union[str, rgb]) -> None:
    drawRect(0, 0, app.width, app.height, fill=color)


def onAppStart(app):
    filePath = ""
    # prompt user until enters valid python file path
    while not path.exists(filePath) or not filePath.endswith(".py"):
        filePath = input("Please enter your python file path: ")
    # save file path and open code content
    app.filePath = filePath
    codeFile = open(app.filePath, "r")
    app.content = codeFile.read()
    # initialize code style checker
    app.checker = Checker(context=app.content)
    # initialize code displayer
    app.snippet = CodeSnippet(
        app,
        geometry=ResponsiveGeometry(app, 0.02, 0.1, 0.46, 0.88),
        content=app.content.splitlines(),
    )
    # initialize code error displayer
    app.errorDisplay = InfoDisplay(
        app,
        setSelectedLine=app.snippet.setSelectedLine,
        geometry=ResponsiveGeometry(app, 0.52, 0.1, 0.46, 0.88),
        content=app.checker.getAllViolations(),
    )


def onKeyPress(app, key):
    if key == "down":
        app.snippet.scrollDown()
    elif key == "up":
        app.snippet.scrollUp()


def onMousePress(app, x, y):
    app.snippet.mousePress(x, y)
    app.errorDisplay.mousePress(x, y)


def onMouseDrag(app, x, y):
    app.snippet.mouseDrag(x, y)
    app.errorDisplay.mouseDrag(x, y)


def onMouseRelease(app, x, y):
    app.snippet.mouseRelease(x, y)
    app.errorDisplay.mouseRelease(x, y)


def redrawAll(app):
    setBackgroundColor(app, color=rgb(50, 170, 170))
    # displat the code and foud errors
    app.snippet.display()
    app.errorDisplay.display()


if __name__ == "__main__":
    runApp(1300, 800)
