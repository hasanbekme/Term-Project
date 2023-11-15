from cmu_graphics import *
from typing import Tuple, List
from checkers import StyleViolation


class CodeSnippet:
    def __init__(
        self,
        app,
        coords: Tuple[int, int] = (0, 0),
        width: int = 400,
        height: int = 900,
        content: List[str] = None,
    ) -> None:
        self.app = app
        self.x, self.y = coords
        self.width = width
        self.height = height
        self.background = "white"
        self.content = content
        self.border = (1, "gray")
        self.fontSize = 16

    @property
    def coords(self):
        return (self.x, self.y)

    def display(self):
        drawRect(
            *self.coords,
            self.width,
            self.height,
            fill=self.background,
            border=self.border[1],
            borderWidth=self.border[0]
        )
        if self.content:
            for lineNo, line in enumerate(self.content):
                drawLabel(
                    str(lineNo + 1),
                    self.x + 5,
                    self.y + lineNo * 30 + 10,
                    align="left-top",
                    size=self.fontSize,
                    font="Arial",
                )
                drawLabel(
                    line,
                    self.x + 50,
                    self.y + lineNo * 30 + 10,
                    align="left",
                    size=self.fontSize,
                    font="Arial",
                )


class ErrorDisplay:
    def __init__(
        self,
        app,
        coords: Tuple[int, int] = (0, 0),
        width: int = 400,
        height: int = 900,
        errors: List[StyleViolation] = None,
    ) -> None:
        self.app = app
        self.x, self.y = coords
        self.width = width
        self.height = height
        self.background = "white"
        self.errors = errors
        self.border = (1, "gray")
        self.fontSize = 16
        self.textColor = "red"

    @property
    def coords(self):
        return (self.x, self.y)

    def display(self):
        drawRect(
            *self.coords,
            self.width,
            self.height,
            fill=self.background,
            border=self.border[1],
            borderWidth=self.border[0]
        )
        if self.errors:
            for lineNo, line in enumerate(self.errors):
                drawLabel(
                    str(line),
                    self.x + 20,
                    self.y + lineNo * 30 + 10,
                    align="left",
                    size=self.fontSize,
                    font="Arial",
                    fill=self.textColor,
                )
