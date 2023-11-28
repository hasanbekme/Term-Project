from cmu_graphics import *
from helpers import BaseGeometry, ResponsiveGeometry
from checkers import Checker
from helpers import hasPressed


class CheckersDialog(BaseGeometry):
    def __init__(
        self,
        app,
        geometry: ResponsiveGeometry,
    ) -> None:
        super().__init__(geometry=geometry)
        self.app = app
        self.isOpen = False
        self.background = "white"
        self.textColor = "black"
        self.fontSize = 20
        self.labelHeight = 60
        self.hovering = None
        self.checkers = list(
            map(
                lambda x: (x in Checker.appliedCheckers, x),
                Checker.allCheckers(),
            )
        )
        self.checkers.sort(key=lambda x: x[1])

    def openDialog(self):
        self.isOpen = True

    def closeDialog(self):
        self.isOpen = False

    def formatCheckerName(self, name: str):
        # format checker name from function name to readble text
        name = name[5:]
        i = 1
        while i != len(name):
            if name[i].isupper():
                name = name[:i] + " " + name[i:]
                i += 2
            else:
                i += 1

        return name

    @property
    def centerCoords(self):
        # return the coordinates of checkers bar in the middle
        return (
            self.width * 0.3,
            (self.height - (len(self.checkers) + 1) * self.labelHeight) / 2
            - self.labelHeight / 2,
            self.width * 0.4,
            (len(self.checkers) + 1) * self.labelHeight,
        )

    def onMouseMove(self, x, y):
        if self.isOpen:
            if hasPressed(x, y, self.centerCoords):
                self.hovering = int((y - self.centerCoords[1]) / self.labelHeight)
            else:
                self.hovering = None

    def onMousePress(self, x, y):
        if self.isOpen:
            if hasPressed(x, y, self.centerCoords):
                pressed = int((y - self.centerCoords[1]) / self.labelHeight)
                if pressed == len(self.checkers):
                    self.closeDialog()
                    self.app.errorDisplay.setContent(content=app.checker.getAllViolations())
                else:
                    selectedChecker = self.checkers[pressed]
                    if selectedChecker[0]:
                        Checker.appliedCheckers.remove(selectedChecker[1])
                    else:
                        Checker.appliedCheckers.add(selectedChecker[1])
                    self.checkers[pressed] = (
                        not selectedChecker[0],
                        selectedChecker[1],
                    )

    def display(self):
        # draw the background
        drawRect(*self.coords, self.width, self.height, fill=self.background)

        # count the number of checkers
        totalCheckers = len(self.checkers) + 1

        # loop through checkers and display them in the window
        for i, (applied, checker) in enumerate(self.checkers):
            # y coordinate of each checker line
            y = (
                self.height - totalCheckers * self.labelHeight
            ) / 2 + self.labelHeight * i

            # change line background in hover and pressed
            if self.hovering == i:
                drawRect(
                    self.width * 0.3,
                    y - self.labelHeight / 2,
                    self.width * 0.4,
                    self.labelHeight,
                    fill=rgb(220, 220, 220),
                )

            # draw the checker name in the middle of screen
            drawLabel(
                self.formatCheckerName(checker),
                self.width / 2,
                y,
                size=self.fontSize,
                fill=self.textColor,
            )

            # borders between checker lines
            drawLine(
                self.width * 0.3,
                y + self.labelHeight / 2,
                self.width * 0.7,
                y + self.labelHeight / 2,
                fill=rgb(220, 220, 220),
                lineWidth=1,
            )

            # insert check mark if the checker is enabled
            if applied:
                drawImage(
                    "./assets/check-mark.png",
                    self.width / 2 - len(checker) * 8,
                    y - 10,
                    width=20,
                    height=20,
                )
        # y coordinate for back button
        y = (self.height + self.labelHeight * (len(self.checkers) - 1)) / 2

        # add hovering and press effects on back button
        if self.hovering == len(self.checkers):
            drawRect(
                self.width * 0.3,
                y - self.labelHeight / 2,
                self.width * 0.4,
                self.labelHeight,
                fill=rgb(220, 220, 220),
            )

        # draw the label
        drawLabel(
            "Go back",
            self.width / 2,
            y,
            size=self.fontSize,
            fill="black",
        )
        # and icon of back button
        drawImage(
            "./assets/left-arrow.png",
            self.width / 2 - 8 * 8,
            y - 10,
            width=20,
            height=20,
        )
        # border line after back button
        drawLine(
            self.width * 0.3,
            y + self.labelHeight / 2,
            self.width * 0.7,
            y + self.labelHeight / 2,
            fill=rgb(220, 220, 220),
            lineWidth=1,
        )
