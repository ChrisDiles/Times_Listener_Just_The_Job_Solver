from itertools import product
from collections import Counter
from digit_map import DigitLetterMap
from grid import Grid
from clue import ClueSolution
from tqdm import tqdm
import time
from typing import List, Tuple, Dict, Set

class CrosswordSolver:
    """
    Class responsible for solving a numerical crossword using constraints 
    from clues, a digit-letter mapping, and a grid structure.
    """

    def __init__(self, structure, clue_parser):
        """
        Initialize the solver with crossword structure and parsed clues.

        Args:
            structure: An object providing .rows, .cols, and .clue_coords.
            clue_parser: A ClueParser instance with parsed clues and letters.
        """
        self._structure = structure
        self._grid = Grid(structure.rows, structure.cols)
        self._clues = clue_parser.clues
        self._dlm = DigitLetterMap(clue_parser.letters)

    def solve(self, max_permutations: int = 10**7) -> None:
        """
        Attempt to solve the crossword, refining possible digits iteratively.

        Args:
            max_permutations: Maximum number of digit permutations to attempt per clue.
        """
        start_time = time.time()
        iteration = 0

        while True:
            iteration += 1
            print(f"\n--- Solve iteration {iteration} ---")

            letter_snapshot: Dict[str, Set[int]] = {
                l: set(d) for l, d in self._dlm.letter_map.items()
            }
            cell_snapshot: Dict[Tuple[int, int], Set[int]] = {
                (cell.row, cell.col): set(cell.possible_values)
                for row in self._grid._cells
                for cell in row
            }

            self._solve_once_through(max_permutations)

            letter_changed = any(letter_snapshot[l] != self._dlm.letter_map[l] for l in letter_snapshot)
            cell_changed = any(
                cell_snapshot[coord] != self._grid.get_cell(*coord).possible_values
                for coord in cell_snapshot
            )

            if all(cell.value is not None for row in self._grid._cells for cell in row):
                print(f"Puzzle solved in {time.time() - start_time:.2f} seconds!")
                break
            if not (letter_changed or cell_changed):
                print(f"No changes detected. Time: {time.time() - start_time:.2f} seconds.")
                break

    def _solve_once_through(self, max_permutations: int) -> None:
        """
        Go through all clues once, updating constraints based on valid solutions.

        Args:
            max_permutations: Limit on number of permutations to try per clue.
        """
        pairs = [(clue, self._estimate_permutations(clue)) for clue in self._clues]
        pairs.sort(key=lambda x: x[1])

        for clue, count in pairs:
            if count > max_permutations:
                print(f"Skipping clue {clue.clue_number} ({clue.direction}) — {count} permutations")
                continue

            print(f"Solving clue {clue.clue_number} {clue.direction.capitalize()} — {count} permutations")
            correct_solutions: List[ClueSolution] = []

            row, col, length = clue.coords["row"], clue.coords["col"], clue.coords["length"]
            letters = sorted(clue.letter_vars)
            digit_options: List[Set[int]] = [self._dlm.letter_map[letter] for letter in letters]

            total = 1
            for opts in digit_options:
                total *= len(opts)

            for digits in tqdm(product(*digit_options), total=total, desc=f"Clue {clue.clue_number} {clue.direction.capitalize()}", leave=False):
                if all(v <= 2 for v in Counter(digits).values()):
                    letter_dict = dict(zip(letters, digits))
                    solution = ClueSolution(clue.evaluate(letter_dict), letter_dict)
                    if solution.value < 0:
                        continue
                    if len(str(solution.value)) == length and self._do_digits_match(solution.value, clue):
                        correct_solutions.append(solution)

            if not correct_solutions:
                raise ValueError(f"No valid solutions for clue {clue.clue_number}")

            for letter in letters:
                used = {sol.letter_map[letter] for sol in correct_solutions}
                eliminated = self._dlm.letter_map[letter] - used
                for d in eliminated:
                    self._dlm.eliminate(letter, d)
                if eliminated:
                    print(f"  Eliminated {eliminated} from '{letter}'")

            cell = self._grid.get_cell(row, col)
            for i in range(length):
                allowed = {self._nth_digit(sol.value, i) for sol in correct_solutions}
                for d in cell.possible_values - allowed:
                    cell.eliminate(d)
                if i < length - 1:
                    cell = self._grid.get_next_cell(cell, clue.direction)

    def _estimate_permutations(self, clue) -> int:
        """
        Estimate how many digit permutations a clue will generate.

        Args:
            clue: A Clue object.

        Returns:
            Estimated number of digit permutations.
        """
        return eval("*".join(str(len(self._dlm.letter_map[l])) for l in clue.letter_vars))

    def _do_digits_match(self, value: int, clue) -> bool:
        """
        Check if a value's digits match the possible digits in each cell.

        Args:
            value: The numeric solution value.
            clue: The corresponding Clue object.

        Returns:
            True if all digits fit in the corresponding cells, False otherwise.
        """
        cell = self._grid.get_cell(clue.coords["row"], clue.coords["col"])
        for i, digit in enumerate(str(value)):
            if int(digit) not in cell.possible_values:
                return False
            if i < len(str(value)) - 1:
                cell = self._grid.get_next_cell(cell, clue.direction)
        return True

    def _nth_digit(self, number: int, n: int) -> int:
        """Return the nth digit (0-indexed) of a number."""
        return int(str(number)[n])

    @property
    def grid(self) -> Grid:
        """Access the internal grid."""
        return self._grid

    @property
    def dlm(self) -> DigitLetterMap:
        """Access the digit-letter map."""
        return self._dlm