from cmu_graphics import *
from os import path
from widget import CodeSnippet, ErrorDisplay
from checkers import Checker


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
        coords=(10, 20),
        width=app.width // 2 - 50,
        height=app.height,
        content=app.content.splitlines(),
    )
    # initialize code error displayer
    app.errorDisplay = ErrorDisplay(
        app,
        coords=(app.width // 2 + 20, 20),
        width=app.width // 2 - 50,
        errors=app.checker.getAllViolations(),
    )


def redrawAll(app):
    # displat the code and foud errors
    app.snippet.display()
    app.errorDisplay.display()


if __name__ == "__main__":
    runApp(1300, 800)
