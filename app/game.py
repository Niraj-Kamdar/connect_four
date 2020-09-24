import itertools
from enum import Enum

import numpy as np

M = 6
N = 7


class TurnEnum(Enum):
    Yellow = "Y"
    Red = "R"


class Connect4:
    def __init__(self):
        self.turn = TurnEnum.Yellow
        self.matrix = np.array([["-"] * N for i in range(M)])
        self.top = {i: M - 1 for i in range(N)}

    def is_row_connected(self):
        for i in range(M):
            for j, k in itertools.groupby(self.matrix[i, :]):
                if j != "-" and len(tuple(k)) >= 4:
                    return j
        return None

    def is_column_connected(self):
        for i in range(N):
            for j, k in itertools.groupby(self.matrix[:, i]):
                if j != "-" and len(tuple(k)) >= 4:
                    return j
        return None

    def is_diagonal_connected(self):
        for A in [self.matrix, np.fliplr(self.matrix)]:
            for i in range(1 - M, N):
                for j, k in itertools.groupby(A.diagonal(i)):
                    if j != "-" and len(tuple(k)) >= 4:
                        return j
        return None

    def is_tie(self):
        if sum(self.top.values()) == 0:
            return "TIE"
        return None

    def check_win(self):
        row = self.is_row_connected()
        col = self.is_column_connected()
        diag = self.is_diagonal_connected()
        return row or col or diag

    def move(self, col):
        if 0 <= col < N and self.top[col] > 0:
            self.matrix[self.top[col], col] = self.turn.value
            self.top[col] -= 1
        else:
            raise ValueError

    def play(self, col):
        self.move(col)
        tie = self.is_tie()
        if tie:
            return tie
        winner = self.check_win()
        if winner:
            winner = "Yellow" if winner == "Y" else "Red"
        self.change_turn()
        return winner

    def change_turn(self):
        if self.turn == TurnEnum.Yellow:
            self.turn = TurnEnum.Red
        else:
            self.turn = TurnEnum.Yellow

    def __str__(self):
        return str(self.matrix)
