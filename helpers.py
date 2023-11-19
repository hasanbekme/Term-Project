import typing


def hasPressed(x: int, y: int, box: typing.Tuple[int]) -> bool:
    return box[0] <= x <= box[0] + box[2] and box[1] <= y <= box[1] + box[3]
