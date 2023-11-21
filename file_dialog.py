from cmu_graphics import *
from helpers import BaseGeometry, ResponsiveGeometry, hasPressed
from os import path, listdir, getcwd
import typing


class FileDialog(BaseGeometry):
    def __init__(
        self,
        app,
        setFilePath: typing.Callable,
        geometry: ResponsiveGeometry,
    ) -> None:
        super().__init__(geometry=geometry)
        self.app = app
        self.background = rgb(255, 255, 255)
        self.border = (2, rgb(185, 185, 187))
        self.isOpen = False
        self.textColor = "red"
        self.fontSize = 16
        self.openPath = getcwd()
        self.listDir = listdir(self.openPath)
        self.scrollSize = len(self.listDir) - 1
        self.scroll = 0
        self.scrollHoverColor = rgb(120, 56, 32)
        self.scrollHeight = 60
        self.scrollDrag = None
        self.selectedLine = None
        self._headerHeight = 0.1
        self._footerHeight = 0.1
        self.setFilePath = setFilePath

    def getIcon(self, dirPath: str):
        if path.isfile(dirPath):
            return (
                "./assets/python.png"
                if dirPath.endswith(".py")
                else "./assets/blank_file.png"
            )
        else:
            return "./assets/folder.png"

    def setOpenPath(self, newPath: str):
        self.openPath = newPath
        self.listDir = listdir(newPath)
        self.scroll = len(self.listDir) - 1
        self.scroll = 0

    @property
    def header(self):
        return self._headerHeight * self.height

    @property
    def footer(self):
        return self._footerHeight * self.height

    @property
    def buttonShape(self):
        return (self.width * 0.2, self.footer * 2 / 3)

    @property
    def closeButtonGeometry(self):
        return (
            self.x + (self.width / 2 - self.buttonShape[0]) / 2,
            self.y + self.height - self.footer * 0.5 - self.buttonShape[1] / 2,
            *self.buttonShape,
        )

    @property
    def openButtonGeometry(self):
        return (
            self.x + self.width / 2 + (self.width / 2 - self.buttonShape[0]) / 2,
            self.y + self.height - self.footer * 0.5 - self.buttonShape[1] / 2,
            *self.buttonShape,
        )

    def scrollUp(self):
        if self.scroll > 0:
            self.scroll -= 1

    def scrollDown(self):
        if self.scroll < self.scrollSize:
            self.scroll += 1

    @property
    def scrollDimensions(self):
        topButton = (
            self.x + self.width - 20,
            self.y + self.header,
            20,
            20,
        )
        bottomButton = (
            self.x + self.width - 20,
            self.y + self.height - self.footer - 20,
            20,
            20,
        )
        scroll = (
            self.x + self.width - 20,
            self.y
            + self.header
            + 20
            + (self.height - 40 - self.scrollHeight - (self.footer + self.header))
            * self.scroll
            / self.scrollSize,
            20,
            self.scrollHeight,
        )
        return (topButton, scroll, bottomButton)

    def openFile(filepath: str):
        assert path.isfile(filepath) and filepath.endswith(".py")

    def openFolderOrFile(self, line: str):
        print(line)
        if 0 <= line - 1 <= len(self.listDir):
            dirName = self.listDir[line - 1]
            newPath = path.join(self.openPath, dirName)
            if path.isdir(newPath):
                self.setOpenPath(newPath=newPath)
            elif newPath.endswith(".py"):
                self.setFilePath(app, newPath)
                self.isOpen = False

    def mousePress(self, x, y):
        scrollDimensions = self.scrollDimensions
        if hasPressed(x, y, scrollDimensions[0]):
            self.scrollUp()
        elif hasPressed(x, y, scrollDimensions[2]):
            self.scrollDown()
        elif hasPressed(x, y, scrollDimensions[1]):
            self.scrollDrag = (y, self.scroll)
        elif hasPressed(x, y, self.closeButtonGeometry):
            self.isOpen = False
        elif hasPressed(x, y, self.openButtonGeometry):
            self.openFolderOrFile(self.selectedLine)
        elif hasPressed(x, y, (self.x, self.y, self.header, self.header)):
            self.setOpenPath(path.dirname(self.openPath))
        elif hasPressed(x, y, (self.x, self.y + self.header, self.width, self.height)):
            line = int(self.scroll + (y - self.y - self.header) // self._lineHeight + 1)
            if self.selectedLine == line:
                self.openFolderOrFile(line)
            else:
                self.selectedLine = line

    def mouseDrag(self, x, y):
        if self.scrollDrag:
            change = (
                (y - self.scrollDrag[0])
                / (self.height - 40 - self.scrollHeight - (self.header + self.footer))
                * self.scrollSize
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

    def openDialog(self):
        self.isOpen = True
        self.setOpenPath(getcwd())

    def display(self):
        if self.isOpen:
            drawRect(
                *self.coords,
                self.width,
                self.height,
                fill=self.background,
                border=self.border[1],
                borderWidth=self.border[0],
            )
            drawRect(
                *self.coords,
                self.width,
                self.header,
                fill=rgb(185, 185, 187),
            )
            drawImage(
                "./assets/back.png",
                self.x,
                self.y,
                width=self.header,
                height=self.header,
            )
            drawLabel(
                self.openPath,
                self.x + self.header + 10,
                self.y + self.header / 2 - 6,
                fill="white",
                size=18,
                align="left-top",
            )
            drawLine(
                self.x,
                self.y + self.height - self.footer,
                self.x + self.width,
                self.y + self.height - self.footer,
                fill=rgb(185, 185, 187),
            )
            for line in range(len(self.listDir) - self.scroll):
                dirPath = self.listDir[line + self.scroll]

                Y = self.y + line * self._lineHeight + self.header + 10
                if Y > self.y + self.height - self.footer - 20:
                    break

                if line + 1 + self.scroll == self.selectedLine:
                    drawRect(
                        self.x,
                        Y - 5,
                        self.width - 20,
                        self._lineHeight,
                        fill=rgb(25, 119, 247),
                    )
                drawImage(
                    self.getIcon(path.join(self.openPath, dirPath)),
                    self.x + 30,
                    Y,
                    width=16,
                    height=16,
                )
                drawLabel(
                    dirPath,
                    self.x + 60,
                    Y,
                    align="left-top",
                    fill="white"
                    if line + 1 + self.scroll == self.selectedLine
                    else "black",
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
                drawRect(
                    *self.closeButtonGeometry, fill="white", border=rgb(202, 202, 202)
                )
                drawLabel(
                    "Close",
                    self.closeButtonGeometry[0] + self.buttonShape[0] // 2,
                    self.closeButtonGeometry[1] + self.buttonShape[1] // 2,
                    size=16,
                )
                drawRect(*self.openButtonGeometry, fill=rgb(25, 119, 247))
                drawLabel(
                    "Open",
                    self.openButtonGeometry[0] + self.buttonShape[0] // 2,
                    self.openButtonGeometry[1] + self.buttonShape[1] // 2,
                    size=16,
                    fill="white",
                )
