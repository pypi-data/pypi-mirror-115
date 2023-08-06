# TTT-game

[![codecov](https://codecov.io/gh/dm1sh/ttt-game/branch/main/graph/badge.svg?token=7GZ4FJ3E4E)](https://codecov.io/gh/dm1sh/ttt-game)
[![Test and Publish](https://github.com/dm1sh/ttt-game/actions/workflows/ci.yml/badge.svg)](https://github.com/dm1sh/ttt-game/actions/workflows/ci.yml)

A simple tic tac toe game implementation

## Usage

### Installation

Testing builds:

```bash
python -m pip install -i https://test.pypi.org/simple/ ttt-game
```

Production builds:

```bash
python -m pip install ttt-game
```

ttt-game module exports main game class `Game` and `Pl` and `Tr` enums to simplify typing.

```python
from ttt_game import Game, Tr, Pl
```

### `Game` class

```python
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

  def get_board(self) -> List[Tr]:
    """
    Returns copy of game board. Use it to display board in UI.
    """

  def check_move(self, pos: int) -> bool:
    """
    Checks if board cell empty
    """

  def check_filled(self) -> bool:
    """
    Checks if game board is filled
    """

  def check_win(self, pos: int) -> bool:
    """
    Checks if this move will make player a winner.
    """

  def insert(self, pos: int, who: Tr) -> None:
    """
    Sets game board's cell to specified value. Better use `move` method when possible
    """

  def move(self, pos: int, who: Pl) -> bool:
    """
    Sets game board cell to specified value when possible. It also returns true if player has won.
    """

  def get_free(self) -> Tuple[int]:
    """
    Returns indexes of free game board cells
    """
```

To use it you should initialize it like below:

```python
game = Game()
```

To make move, below code is listed. `result` variable will contain `True` if `Pl.X` player won the game.

```python
result = game.move(1, Tr.X)
if result:
  print("Congrats, X player won!")
```

You also can get game board array with `get_board` method. To visualize it you can customize code listed below.

```python
board = game.get_board()

for i in range(9):
  print(board[i], end=" ")
  if i % 3 == 2:
    print("\n", end="")

"""
output: Tr.E Tr.X Tr.E
        Tr.E Tr.E Tr.E
        Tr.E Tr.E Tr.E
"""
```

### `Pl` and `Tr` Enums

`Pl` has two members: `X` and `O` meaning X and O players.

```python
class Pl(Enum):
  X = 1
  O = 2
```

`Tr` enum has all members of `Pl` plus `E` entry meaning empty cell.

```python
class Tr(Enum):
  E = 0
  X = Pl.X
  O = Pl.O
```
