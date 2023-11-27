from cmu_graphics import *
from typing import Union
from helpers import ResponsiveGeometry
from code_snippet import CodeSnippet
from info_display import InfoDisplay
from file_dialog import FileDialog
from checkers import Checker
from checkers_dialog import CheckersDialog
from button import Button
import os


def setBackgroundColor(app, color: Union[str, rgb]) -> None:
    drawRect(0, 0, app.width, app.height, fill=color)


def setPythonFilePath(app, path: str):
    if os.path.isfile(path) and path.endswith(".py"):
        app.filePath = path
        pythonCode = open(app.filePath, "r")
        app.content = pythonCode.read()
        app.snippet.setContent(content=app.content.splitlines())
        app.checker = Checker(content=app.content)
        app.errorDisplay.setContent(content=app.checker.getAllViolations())
    else:
        app.filePath = None
        app.content = None


def onAppStart(app):
    app.filePath = None
    app.content = None

    # create file Dialog class
    app.fileDialog = FileDialog(
        app,
        geometry=ResponsiveGeometry(app, 0.25, 0.25, 0.5, 0.5),
        setFilePath=setPythonFilePath,
    )

    # initialize code style checker
    app.checker = Checker(content=app.content)

    # initialize code displayer
    app.snippet = CodeSnippet(
        app,
        geometry=ResponsiveGeometry(app, 0.02, 0.1, 0.46, 0.88),
        content=app.content.splitlines() if app.content else None,
    )

    # initialize code error displayer
    app.errorDisplay = InfoDisplay(
        app,
        setSelectedLine=app.snippet.setSelectedLine,
        geometry=ResponsiveGeometry(app, 0.52, 0.1, 0.46, 0.88),
        content=app.checker.getAllViolations(),
    )

    # create checkers settings dialog
    app.checkersDialog = CheckersDialog(
        app, geometry=ResponsiveGeometry(app, 0, 0, 1.0, 1.0)
    )

    # initialize file open dialog
    app.openFileButton = Button(
        app,
        ResponsiveGeometry(app, 0.02, 0.02, 0.1, 0.06),
        action=app.fileDialog.openDialog,
        backgroundColorHover=rgb(240, 240, 240),
        backgroundColorPressed=rgb(200, 200, 200),
        borderColor=rgb(150, 150, 150),
        borderWidth=2,
        buttonText="Open File",
        buttonFontSize=18,
    )

    # create checkers setting open button
    app.openCheckersButton = Button(
        app,
        ResponsiveGeometry(app, 0.88, 0.02, 0.1, 0.06),
        action=app.checkersDialog.openDialog,
        backgroundColorHover=rgb(240, 240, 240),
        backgroundColorPressed=rgb(200, 200, 200),
        borderColor=rgb(150, 150, 150),
        borderWidth=2,
        buttonText="Set Checkers",
        buttonFontSize=18,
    )


def onKeyPress(app, key):
    if key == "down":
        app.snippet.scrollDown()
    elif key == "up":
        app.snippet.scrollUp()


def onMousePress(app, x, y):
    if app.fileDialog.isOpen:
        app.fileDialog.mousePress(x, y)
        return
    app.snippet.mousePress(x, y)
    app.errorDisplay.mousePress(x, y)
    app.openFileButton.onMousePress(x, y)
    app.openCheckersButton.onMousePress(x, y)
    app.checkersDialog.onMousePress(x, y)


def onMouseMove(app, x, y):
    app.openFileButton.onMouseMove(x, y)
    app.openCheckersButton.onMouseMove(x, y)
    app.checkersDialog.onMouseMove(x, y)


def onMouseDrag(app, x, y):
    if app.fileDialog.isOpen:
        app.fileDialog.mouseDrag(x, y)
        return
    app.snippet.mouseDrag(x, y)
    app.errorDisplay.mouseDrag(x, y)


def onMouseRelease(app, x, y):
    if app.fileDialog.isOpen:
        app.fileDialog.mouseRelease(x, y)
        return
    app.snippet.mouseRelease(x, y)
    app.errorDisplay.mouseRelease(x, y)
    app.openFileButton.onMouseRelease(x, y)
    app.openCheckersButton.onMouseRelease(x, y)


def redrawAll(app):
    if app.fileDialog.isOpen:
        app.fileDialog.display()
        return
    elif app.checkersDialog.isOpen:
        app.checkersDialog.display()
        return
    setBackgroundColor(app, color=rgb(50, 170, 170))
    app.snippet.display()
    app.errorDisplay.display()
    app.openFileButton.display()
    app.openCheckersButton.display()


if __name__ == "__main__":
    runApp(1300, 800)
