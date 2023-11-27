from cmu_graphics import drawRect, drawLabel, rgb
from helpers import BaseGeometry, ResponsiveGeometry
from typing import List
from helpers import hasPressed


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
        self.textColor = "black"
        self.fontSize = 14

        self.setContent(content=content)

        self.scrollHeight = 60
        self.scrollDrag = None

    def setContent(self, content: str):
        self.content = content or ""
        self.scroll = 0
        self.scrollSize = max(len(self.content), 1)
        self.selectedLine = None

    def scrollUp(self):
        if self.scroll > 0:
            self.scroll -= 1

    def scrollDown(self):
        if self.scroll < self.scrollSize:
            self.scroll += 1

    def setSelectedLine(self, lineNumber):
        self.selectedLine = lineNumber
        if not (self.scroll <= lineNumber <= self.scroll + self.visibleLines):
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
            self.scrollDrag = (y, self.scroll)
        elif hasPressed(x, y, (self.x, self.y, self.width, self.height)):
            self.selectedLine = (
                self.scroll + (y - self.y) // self._lineHeight + 1
            )

    def mouseDrag(self, x, y):
        if self.scrollDrag:
            change = (
                (y - self.scrollDrag[0])
                / (self.height - 40)
                * (self.scrollSize + 20)
            )
            if 0 <= int(self.scrollDrag[1] + change) <= self.scrollSize:
                self.scroll = int(self.scrollDrag[1] + change)
            elif 0 > self.scroll + int(change):
                self.scroll = 0
            else:
                self.scroll = self.scrollSize

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
        else:
            drawLabel(
                "Select your code",
                self.x + self.width / 2,
                self.y + self.height / 2,
                size=24,
            )
