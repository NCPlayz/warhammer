from typing import Optional

from .unit import Unit


class Board:
    def __init__(self):
        self.board = [
            [None for _ in range(100)] for _ in range(25)
        ]

    def __str__(self):
        s = []
        for y in self.board:
            y_line = ""
            for x in y:
                x: Optional[Unit]
                if x is None:
                    y_line += " "
                else:
                    y_line += str(x)
            s.append(y_line)

        return "\n".join(s)
