import re
from typing import List, Set
from clue import Clue

class ClueParser:
    """
    Parses a block of clue text along with clue coordinates and produces Clue objects.
    Also extracts the unique letters used in clue expressions.
    """

    def __init__(self, clues_text: str, clue_coords: List[dict]):
        """
        Initializes the ClueParser and processes the clues.

        Args:
            clues_text (str): The raw string containing Across and Down clues.
            clue_coords (List[dict]): A list of dictionaries with keys "row", "col", and "length".
        """
        self._clues: List[Clue] = []
        self._letters: Set[str] = set()
        self._parse_clues(clues_text, clue_coords)

    def _insert_multiplication(self, expr: str) -> str:
        """
        Inserts explicit multiplication operators where implied (e.g., '2A' becomes '2*A').

        Args:
            expr (str): The expression to modify.

        Returns:
            str: The modified expression with multiplication operators inserted.
        """
        expr = re.sub(r'(\d)([A-Z])', r'\1*\2', expr)
        expr = re.sub(r'([A-Z])(\d)', r'\1*\2', expr)
        while re.search(r'([A-Z])([A-Z])', expr):
            expr = re.sub(r'([A-Z])([A-Z])', r'\1*\2', expr)
        expr = re.sub(r'([A-Z])\(', r'\1*(', expr)
        expr = re.sub(r'\)([A-Z])', r')*\1', expr)
        expr = re.sub(r'\)\(', r')*(', expr)
        return expr

    def _parse_clues(self, clues_text: str, clue_coords: List[dict]) -> None:
        """
        Parses the clue text and coordinates, generating Clue objects.

        Args:
            clues_text (str): Raw clue text containing "Across" and "Down" sections.
            clue_coords (List[dict]): A list of dictionaries each with clue metadata.
        """
        lines = clues_text.strip().splitlines()
        direction = None
        index = 0

        for line in lines:
            line = line.strip()
            if line.lower() in {"across", "down"}:
                direction = line.lower()
                continue

            match = re.match(r"(\d+)\s+(.*)", line)
            if not match:
                continue

            clue_number = int(match.group(1))
            expression = self._insert_multiplication(match.group(2).strip())
            letters = set(re.findall(r'\b[A-Z]\b', expression))
            self._letters.update(letters)

            coords = clue_coords[index]
            index += 1
            self._clues.append(Clue(clue_number, letters, expression, direction, coords))

    @property
    def clues(self) -> List[Clue]:
        """
        Returns the list of parsed Clue objects.

        Returns:
            List[Clue]: All clues extracted from the text.
        """
        return self._clues

    @property
    def letters(self) -> Set[str]:
        """
        Returns the set of all unique letters used in clue expressions.

        Returns:
            Set[str]: Unique clue variable letters.
        """
        return self._letters
