from cmu_graphics import *
from typing import Union
from helpers import ResponsiveGeometry, hasPressed
from code_snippet import CodeSnippet
from info_display import InfoDisplay
from file_dialog import FileDialog
from checkers import Checker
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
        app.errorDisplay.setContent(content = app.checker.getAllViolations())
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

    app.openIconGeometry = ResponsiveGeometry(app, 0.025, 0.02, 0.042, 0.07)


def onKeyPress(app, key):
    if key == "down":
        app.snippet.scrollDown()
    elif key == "up":
        app.snippet.scrollUp()


def onMousePress(app, x, y):
    if app.fileDialog.isOpen:
        app.fileDialog.mousePress(x, y)
        return
    if hasPressed(
        x,
        y,
        (
            *app.openIconGeometry(),
            app.openIconGeometry.width,
            app.openIconGeometry.height,
        ),
    ):
        app.fileDialog.openDialog()
    app.snippet.mousePress(x, y)
    app.errorDisplay.mousePress(x, y)


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


def redrawAll(app):
    if app.fileDialog.isOpen:
        app.fileDialog.display()
        return
    setBackgroundColor(app, color=rgb(50, 170, 170))
    drawImage(
        "./assets/python-file.png",
        *app.openIconGeometry(),
        **app.openIconGeometry.shape
    )
    app.snippet.display()
    app.errorDisplay.display()


if __name__ == "__main__":
    runApp(1300, 800)
