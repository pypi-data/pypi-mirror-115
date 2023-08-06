from typing import List, Tuple
from enum import Enum


class Pl(Enum):
  X = 1
  O = 2


class Tr(Enum):
  E = 0
  X = Pl.X
  O = Pl.O


class Game:
  """
  Board indexes preview:

  [[0, 1, 2],

   [3, 4, 5],

   [6, 7, 8]]

   Board array itself:

  [Tr.E, Tr.E, Tr.E, Tr.E, Tr.E, Tr.E, Tr.E, Tr.E, Tr.E]
  """
  _board: List[Tr]

  def __init__(self):
    self._board = [Tr.E] * 9

  def get_board(self) -> List[Tr]:
    """
    Returns copy of game board. Use it to display board in UI.
    """
    return self._board.copy()

  def check_move(self, pos: int) -> bool:
    """
    Checks if board cell empty
    """
    return self._board[pos] == Tr.E

  def check_filled(self) -> bool:
    """
    Checks if game board is filled
    """
    return self._board.count(Tr.E) == 0

  def check_win(self, pos: int) -> bool:
    """
    Checks if this move will make player a winner.
    """
    b = self._board

    row_n = pos - pos % 3
    row = b[row_n] == b[row_n + 1] == b[row_n + 2] != Tr.E

    col_n = pos % 3
    col = b[col_n] == b[col_n + 3] == b[col_n + 6] != Tr.E

    diag = False
    alt_diag = False

    if (pos % 4 == 0):
      diag = b[0] == b[4] == b[8] != Tr.E
    if (pos in (2, 4, 6)):
      alt_diag = b[2] == b[4] == b[6] != Tr.E

    return row or col or diag or alt_diag

  def insert(self, pos: int, who: Tr) -> None:
    """
    Sets game board's cell to specified value. Better use `move` method when possible
    """
    self._board[pos] = who

  def move(self, pos: int, who: Pl) -> bool:
    """
    Sets game board cell to specified value when possible. It also returns true if player has won.
    """
    if (self.check_move(pos)):
      self.insert(pos, who)
      return self.check_win(pos)
    else:
      return False

  def get_free(self) -> Tuple[int]:
    """
    Returns indexes of free game board cells
    """

    return tuple(filter(lambda i: self._board[i] == Tr.E, range(9)))
