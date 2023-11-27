from cmu_graphics import *
from helpers import BaseGeometry, ResponsiveGeometry, hasPressed
from typing import Union, Callable


class Button(BaseGeometry):
    def __init__(
        self,
        app,
        geometry: ResponsiveGeometry,
        action: Callable,
        backgroundColorDefault: Union[str, rgb] = "white",
        backgroundColorHover: Union[str, rgb] = "white",
        backgroundColorPressed: Union[str, rgb] = "white",
        borderColor: Union[str, rgb, None] = None,
        borderWidth: int = 1,
        buttonText: str = None,
        buttonFontSize: int = 16,
        buttonFontFamily: str = "Arial",
    ) -> None:
        super().__init__(geometry)

        self.app = app
        self.backgroundColorDefault = backgroundColorDefault
        self.backgroundColorHover = backgroundColorHover
        self.backgroundColorPressed = backgroundColorPressed
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.buttonText = buttonText
        self.buttonFontSize = buttonFontSize
        self.buttonFontFamily = buttonFontFamily

        self.backgroundColor = self.backgroundColorDefault

        self.action = action

    @property
    def box(self):
        return (self.x, self.y, self.width, self.height)

    def onMouseMove(self, x, y):
        if hasPressed(x, y, self.box):
            self.backgroundColor = self.backgroundColorHover
        else:
            self.backgroundColor = self.backgroundColorDefault

    def onMouseRelease(self, x, y):
        if hasPressed(x, y, self.box):
            self.backgroundColor = self.backgroundColorHover

    def onMousePress(self, x, y):
        if hasPressed(x, y, self.box):
            self.backgroundColor = self.backgroundColorPressed
            self.action()

    def display(self):
        drawRect(
            *self.coords,
            self.width,
            self.height,
            fill=self.backgroundColor,
            border=self.borderColor,
            borderWidth=self.borderWidth
        )

        if self.buttonText:
            drawLabel(
                self.buttonText,
                self.x + self.width / 2,
                self.y + self.height / 2,
                size=self.buttonFontSize,
                font=self.buttonFontFamily,
            )
