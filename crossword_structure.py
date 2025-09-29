import json
from typing import List, Dict

class CrosswordStructure:
    """
    Parses a crossword structure based on provided bar location data in JSON format.
    Determines the positions of across and down clues.
    """

    def __init__(self, bar_locations_csv: str):
        """
        Initialize the CrosswordStructure from a JSON string of bar locations.

        Args:
            bar_locations_csv (str): A JSON string containing "Vertical" and "Horizontal" bar positions.
        """
        self._clue_coords: List[Dict[str, int]] = []
        self._parse_bar_locations(bar_locations_csv)

    def _parse_bar_locations(self, json_text: str) -> None:
        """
        Parses the JSON bar location data to identify clue positions.

        Args:
            json_text (str): A JSON string with keys "Vertical" and "Horizontal", each mapping
                             to lists of integers indicating bar positions.
        """
        bar_data = json.loads(json_text)
        vertical_bars: List[List[int]] = bar_data["Vertical"]
        horizontal_bars: List[List[int]] = bar_data["Horizontal"]

        self._rows = len(vertical_bars)
        self._cols = len(horizontal_bars)
        clue_coords: List[Dict[str, int]] = []

        # Across clues
        for r, bars in enumerate(vertical_bars):
            positions = [0] + sorted(bars) + [self._cols]
            for i in range(len(positions) - 1):
                start = positions[i]
                end = positions[i + 1]
                if end - start > 1:
                    clue_coords.append({"row": r, "col": start, "length": end - start})

        # Down clues
        for r in range(self._rows):
            for c in range(self._cols):
                bar_above = r == 0 or r in horizontal_bars[c]
                if bar_above:
                    length = 1
                    for rr in range(r + 1, self._rows):
                        if rr in horizontal_bars[c]:
                            break
                        length += 1
                    if length > 1:
                        clue_coords.append({"row": r, "col": c, "length": length})

        self._clue_coords = clue_coords

    @property
    def clue_coords(self) -> List[Dict[str, int]]:
        """
        Returns a list of clue coordinate dictionaries, each containing 'row', 'col', and 'length'.

        Returns:
            List[Dict[str, int]]: The positions and lengths of clues.
        """
        return self._clue_coords

    @property
    def rows(self) -> int:
        """
        Returns the number of rows in the crossword grid.

        Returns:
            int: Number of rows.
        """
        return self._rows

    @property
    def cols(self) -> int:
        """
        Returns the number of columns in the crossword grid.

        Returns:
            int: Number of columns.
        """
        return self._cols
