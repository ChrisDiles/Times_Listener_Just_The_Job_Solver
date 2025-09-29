from typing import Set, Dict

class Clue:
    def __init__(
        self,
        clue_number: int,
        letter_vars: Set[str],
        expression: str,
        direction: str,
        coords: Dict[str, int]
    ) -> None:
        """
        Initialize a Clue object representing a crossword clue with an expression to evaluate.

        Args:
            clue_number (int): The number identifier of the clue.
            letter_vars (Set[str]): Set of variable names (letters) used in the clue expression.
            expression (str): A string expression to be evaluated for the clue.
            direction (str): Direction of the clue ('across' or 'down').
            coords (Dict[str, int]): Coordinates related to the clue, typically including starting row and column.
        """
        self._clue_number: int = clue_number
        self._letter_vars: Set[str] = letter_vars
        self._expression: str = expression
        self._direction: str = direction
        self._coords: Dict[str, int] = coords

    def evaluate(self, letter_dict: Dict[str, int]) -> int:
        """
        Evaluate the clue's expression using the provided letter values.

        Args:
            letter_dict (Dict[str, int]): A dictionary mapping letter variables to their integer values.

        Raises:
            ValueError: If any required letter variable is missing in the provided dictionary.

        Returns:
            int: The result of evaluating the clue's expression.
        """
        missing = self._letter_vars - letter_dict.keys()
        if missing:
            raise ValueError(f"Missing values for: {missing}")
        return eval(self._expression, {}, letter_dict)

    @property
    def clue_number(self) -> int:
        """Get the clue number."""
        return self._clue_number

    @property
    def letter_vars(self) -> Set[str]:
        """Get the set of letter variables used in the clue."""
        return self._letter_vars

    @property
    def coords(self) -> Dict[str, int]:
        """Get the coordinates associated with the clue."""
        return self._coords

    @property
    def direction(self) -> str:
        """Get the direction of the clue."""
        return self._direction

class ClueSolution:
    def __init__(self, value: int, letter_map: Dict[str, int]) -> None:
        """
        Initialize a Solution instance representing the solved value and corresponding letter-to-digit mapping.

        Args:
            value (int): The numeric value of the solution.
            letter_map (Dict[str, int]): A dictionary mapping letters to their assigned integer values.
        """
        self._value: int = value
        self._letter_map: Dict[str, int] = letter_map
    
    @property
    def letter_map(self) -> Dict[str, int]:
        """Get the mapping of letters to their integer values."""
        return self._letter_map
    
    @property
    def value(self) -> int:
        """Get the integer value of the solution."""
        return self._value
