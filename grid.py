from typing import Optional, Set, Tuple, List

class Cell:
    def __init__(self, row: int, col: int, value: Optional[int] = None) -> None:
        """
        Initialize a Cell at a specific grid position.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
            value (Optional[int], optional): The assigned value of the cell. Defaults to None.
        """
        self.row: int = row
        self.col: int = col
        self._value: Optional[int] = value
        self._possible_values: Set[int] = set(range(10))

    @property
    def value(self) -> Optional[int]:
        """Return the currently assigned value of the cell, or None if unassigned."""
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        """Assign a definite value to the cell."""
        self._value = value

    def _assign_if_unique(self) -> None:
        """
        Assign the cell’s value if only one possible value remains.

        Raises:
            ValueError: If no candidate values remain for this cell.
        """
        if len(self.possible_values) == 0:
            raise ValueError(f"No candidate values at {self.coords}.")
        elif len(self.possible_values) == 1:
            self.value = next(iter(self.possible_values))
            print(f"Cell at {self.coords} has been assigned the value: {self.value}.")

    def eliminate(self, value: int) -> None:
        """
        Eliminate a possible candidate value from this cell.

        Args:
            value (int): The digit to eliminate from possible values.
        """
        self._possible_values.remove(value)
        self._assign_if_unique()

    @property
    def coords(self) -> Tuple[int, int]:
        """Return the (row, col) coordinates of this cell."""
        return (self.row, self.col)

    @property
    def possible_values(self) -> Set[int]:
        """Return the set of possible digits that this cell can take."""
        return self._possible_values

    def __str__(self) -> str:
        """Return the string representation of the cell’s value or a blank space if unassigned."""
        return str(self._value) if self._value is not None else " "

from typing import List

class Grid:
    def __init__(self, rows: int, cols: int) -> None:
        """
        Initialize a Grid object with the specified number of rows and columns.

        Args:
            rows (int): Number of rows in the grid.
            cols (int): Number of columns in the grid.
        """
        self._rows: int = rows
        self._cols: int = cols
        self._cells: List[List[Cell]] = [
            [Cell(row, col) for col in range(cols)]
            for row in range(rows)
        ]

    def get_cell(self, row: int, col: int) -> Cell:
        """
        Retrieve the Cell object at the specified row and column.

        Args:
            row (int): Row index of the cell.
            col (int): Column index of the cell.

        Returns:
            Cell: The cell at the given coordinates.
        """
        return self._cells[row][col]
    
    def get_next_cell(self, cell: Cell, direction: str) -> Cell:
        """
        Return the next cell in the specified direction from the given cell.

        Args:
            cell (Cell): The current cell.
            direction (str): Either 'across' or 'down'.

        Returns:
            Cell: The next cell in the given direction.

        Raises:
            IndexError: If the next cell is out of bounds.
        """
        row, col = cell.coords
        if direction == "across":
            col += 1
        elif direction == "down":
            row += 1
        else:
            raise ValueError(f"Invalid direction '{direction}'")

        if 0 <= row < self._rows and 0 <= col < self._cols:
            return self.get_cell(row, col)
        else:
            raise IndexError(f"Next cell out of bounds: ({row}, {col})")

    def __str__(self) -> str:
        """
        Return a string representation of the grid with cells formatted in a table.

        Returns:
            str: String showing the grid with borders and cell values.
        """
        horizontal_line = '+' + '+'.join(['-' * 3] * self._cols) + '+'
        lines = []
        for row in self._cells:
            lines.append(horizontal_line)
            row_str = '|'.join(f' {str(cell)} ' for cell in row)
            lines.append('|' + row_str + '|')
        lines.append(horizontal_line)
        return '\n'.join(lines)

    @property
    def rows(self) -> int:
        """Number of rows in the grid."""
        return self._rows

    @property
    def cols(self) -> int:
        """Number of columns in the grid."""
        return self._cols
