from cmu_graphics import *
from typing import List, Union, Callable
from helpers import hasPressed
from checkers import StyleViolation


class ResponsiveGeometry:
    def __init__(
        self,
        app,
        x: Union[float, int],
        y: Union[float, int],
        width: Union[float, int],
        height: Union[float, int],
    ) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.app = app

    @property
    def x(self):
        return (
            self._x if isinstance(self._x, int) else self.app.width * self._x
        )

    @property
    def y(self):
        return (
            self._y if isinstance(self._y, int) else self.app.height * self._y
        )

    @property
    def width(self):
        return (
            self._width
            if isinstance(self._width, int)
            else self.app.width * self._width
        )

    @property
    def height(self):
        return (
            self._height
            if isinstance(self._height, int)
            else self.app.height * self._height
        )

    def __call__(self) -> tuple:
        return (self.x, self.y)


class BaseGeometry:
    def __init__(self, geometry: ResponsiveGeometry) -> None:
        self.geometry = geometry
        self._lineHeight = 25

    @property
    def x(self):
        return self.geometry.x

    @property
    def y(self):
        return self.geometry.y

    @property
    def width(self):
        return self.geometry.width

    @property
    def height(self):
        return self.geometry.height

    @property
    def coords(self):
        return (self.x, self.y)

    @property
    def visibleLines(self) -> int:
        return int(self.height / self._lineHeight)


class CodeSnippet(BaseGeometry):
    def __init__(
        self,
        app,
        geometry: ResponsiveGeometry,
        content: List[str] = None,
    ) -> None:
        super().__init__(geometry=geometry)
        self.app = app
        self.background = "white"
        self.border = (1, "gray")
        self.content = content
        self.textColor = "black"
        self.fontSize = 14
        self.scroll = 0
        self.scrollSize = len(self.content)
        self.scrollHeight = 60
        self.scrollDrag = None
        self.selectedLine = 10

    def scrollUp(self):
        if self.scroll > 0:
            self.scroll -= 1

    def scrollDown(self):
        if self.scroll < self.scrollSize:
            self.scroll += 1

    def setSelectedLine(self, lineNumber):
        self.selectedLine = lineNumber
        if not (self.scroll <= lineNumber <= self.scroll + self.visibleLines):
            print("Visible lnies ", self.visibleLines)
            print("Line number ", lineNumber)
            self.scroll = (
                0
                if lineNumber <= self.visibleLines // 2
                else lineNumber - self.visibleLines // 2
            )

    @property
    def scrollDimensions(self):
        topButton = (self.x + self.width - 20, self.y, 20, 20)
        bottomButton = (
            self.x + self.width - 20,
            self.y + self.height - 20,
            20,
            20,
        )
        scroll = (
            self.x + self.width - 20,
            self.y
            + 20
            + (self.height - 40 - self.scrollHeight)
            * self.scroll
            / self.scrollSize,
            20,
            self.scrollHeight,
        )
        return (topButton, scroll, bottomButton)

    def mousePress(self, x, y):
        scrollDimensions = self.scrollDimensions
        if hasPressed(x, y, scrollDimensions[0]):
            self.scrollUp()
        elif hasPressed(x, y, scrollDimensions[2]):
            self.scrollDown()
        elif hasPressed(x, y, scrollDimensions[1]):
            self.scrollDrag = y
        elif hasPressed(x, y, (self.x, self.y, self.width, self.height)):
            self.selectedLine = (
                self.scroll + (y - self.y) // self._lineHeight + 1
            )

    def mouseDrag(self, x, y):
        if self.scrollDrag:
            change = (
                (y - self.scrollDrag)
                / (self.height - 40 - self.scrollHeight)
                * self.scrollSize
            )
            if 0 <= self.scroll + int(change) <= self.scrollSize:
                self.scroll += int(change)
            elif 0 > self.scroll + int(change):
                self.scroll = 0
            else:
                self.scroll = self.scrollSize
            self.scrollDrag = y

    def mouseRelease(self, x, y):
        if self.scrollDrag:
            self.scrollDrag = None

    def display(self):
        # draw the rectangle around editor area
        drawRect(
            *self.coords,
            self.width,
            self.height,
            fill=self.background,
            border=self.border[1],
            borderWidth=self.border[0],
        )

        # write the content in code snippet
        if self.content:
            # calculate the offset of code from top
            # go through every line line igoring first lines in offset
            for lineNo in range(len(self.content) - self.scroll):
                line = self.content[lineNo + self.scroll]
                yValue = self.y + lineNo * self._lineHeight + 10
                if yValue > self.y + self.height - 20:
                    break
                if lineNo + 1 + self.scroll == self.selectedLine:
                    drawRect(
                        self.x,
                        self.y + lineNo * self._lineHeight,
                        self.width,
                        self._lineHeight,
                        fill="red",
                        opacity=40,
                    )
                drawLabel(
                    str(lineNo + 1 + self.scroll),
                    self.x + 5,
                    yValue,
                    fill=self.textColor,
                    align="left-top",
                    size=self.fontSize,
                    font="Arial",
                )
                drawLabel(
                    line,
                    self.x + 50,
                    yValue,
                    align="left-top",
                    size=self.fontSize,
                    font="Arial",
                )

        # draw the scrollbar
        drawRect(
            *self.scrollDimensions[0],
            fill=rgb(200, 200, 200),
            border=rgb(100, 100, 100),
        )
        drawRect(
            *self.scrollDimensions[2],
            fill=rgb(200, 200, 200),
            border=rgb(100, 100, 100),
        )
        drawRect(
            *self.scrollDimensions[1],
            fill=rgb(150, 150, 150) if self.scrollDrag else rgb(200, 200, 200),
            border=rgb(100, 100, 100),
        )


class InfoDisplay(BaseGeometry):
    def __init__(
        self,
        app,
        setSelectedLine: Callable,
        geometry: ResponsiveGeometry,
        content: List[StyleViolation] = None,
    ) -> None:
        super().__init__(geometry=geometry)
        self.app = app
        self.background = "white"
        self.border = (1, "gray")
        self.content = content
        self.textColor = "red"
        self.fontSize = 14
        self.scroll = 0
        self.scrollSize = len(self.content)
        self.scrollHovered = False
        self.scrollHoverColor = rgb(120, 56, 32)
        self.scrollHeight = 60
        self.scrollDrag = None
        self.selectedLine = None
        self.setSelectedLine = setSelectedLine

    def scrollUp(self):
        if self.scroll > 0:
            self.scroll -= 1

    def scrollDown(self):
        if self.scroll < self.scrollSize:
            self.scroll += 1

    @property
    def scrollDimensions(self):
        topButton = (self.x + self.width - 20, self.y, 20, 20)
        bottomButton = (
            self.x + self.width - 20,
            self.y + self.height - 20,
            20,
            20,
        )
        scroll = (
            self.x + self.width - 20,
            self.y
            + 20
            + (self.height - 40 - self.scrollHeight)
            * self.scroll
            / self.scrollSize,
            20,
            self.scrollHeight,
        )
        return (topButton, scroll, bottomButton)

    def mousePress(self, x, y):
        scrollDimensions = self.scrollDimensions
        if hasPressed(x, y, scrollDimensions[0]):
            self.scrollUp()
        elif hasPressed(x, y, scrollDimensions[2]):
            self.scrollDown()
        elif hasPressed(x, y, scrollDimensions[1]):
            self.scrollDrag = y
        elif hasPressed(x, y, (self.x, self.y, self.width, self.height)):
            self.selectedLine = int(
                self.scroll + (y - self.y) // self._lineHeight + 1
            )
            if self.selectedLine <= len(self.content):
                self.setSelectedLine(self.content[self.selectedLine - 1].line)

    def mouseDrag(self, x, y):
        if self.scrollDrag:
            change = (
                (y - self.scrollDrag)
                / (self.height - 40 - self.scrollHeight)
                * self.scrollSize
            )
            if 0 <= self.scroll + int(change) <= self.scrollSize:
                self.scroll += int(change)
            elif 0 > self.scroll + int(change):
                self.scroll = 0
            else:
                self.scroll = self.scrollSize
            self.scrollDrag = y

    def mouseRelease(self, x, y):
        if self.scrollDrag:
            self.scrollDrag = None

    def display(self):
        # draw the rectangle around editor area
        drawRect(
            *self.coords,
            self.width,
            self.height,
            fill=self.background,
            border=self.border[1],
            borderWidth=self.border[0],
        )

        # write the content in code snippet
        if self.content:
            # calculate the offset of code from top
            # go through every line line igoring first lines in offset
            for lineNo in range(len(self.content) - self.scroll):
                line = self.content[lineNo + self.scroll]
                yValue = self.y + lineNo * self._lineHeight + 10
                if yValue > self.y + self.height - 20:
                    break
                drawLabel(
                    line,
                    self.x + 20,
                    yValue,
                    align="left-top",
                    fill=self.textColor,
                    size=self.fontSize,
                    font="Arial",
                )
                if lineNo + 1 + self.scroll == self.selectedLine:
                    drawRect(
                        self.x,
                        self.y + lineNo * self._lineHeight,
                        self.width,
                        self._lineHeight,
                        fill="black",
                        opacity=40,
                    )

        # draw the scrollbar
        drawRect(
            *self.scrollDimensions[0],
            fill=rgb(200, 200, 200),
            border=rgb(100, 100, 100),
        )
        drawRect(
            *self.scrollDimensions[2],
            fill=rgb(200, 200, 200),
            border=rgb(100, 100, 100),
        )
        drawRect(
            *self.scrollDimensions[1],
            fill=rgb(150, 150, 150) if self.scrollDrag else rgb(200, 200, 200),
            border=rgb(100, 100, 100),
        )
