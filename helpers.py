from typing import Union, Tuple


def hasPressed(x: int, y: int, box: Tuple[int]) -> bool:
    return box[0] <= x <= box[0] + box[2] and box[1] <= y <= box[1] + box[3]


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

    @property
    def shape(self):
        return {"width": self.width, "height": self.height}

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
        return self.geometry()

    @property
    def visibleLines(self) -> int:
        return int(self.height / self._lineHeight)
