from typing import Dict, Set, List

class DigitLetterMap:
    def __init__(self, letters: List[str]) -> None:
        """
        Initialize the mapping between letters and possible digits.

        Each letter initially maps to all digits (0-9), and each digit maps to all letters.

        Args:
            letters (List[str]): List of letters to be mapped.
        """
        digits = list(range(10))
        self._letter_map: Dict[str, Set[int]] = {letter: set(digits) for letter in letters}
        self._digit_map: Dict[int, Set[str]] = {digit: set(letters) for digit in digits}

    def eliminate(self, letter: str, digit: int) -> None:
        """
        Eliminate a digit from the possible values for a letter, and vice versa.

        Raises ValueError if eliminating leads to no possible digits for a letter
        or fewer than two possible letters for a digit.

        Args:
            letter (str): The letter from which to eliminate the digit.
            digit (int): The digit to eliminate.
        """
        if digit not in self._letter_map[letter]:
            return

        self._letter_map[letter].remove(digit)
        self._digit_map[digit].remove(letter)

        if not self._letter_map[letter]:
            raise ValueError(f"No possible digits remain for letter '{letter}' after eliminating digit '{digit}'.")

        if len(self._digit_map[digit]) < 2:
            raise ValueError(f"Fewer than two possible letters remain for digit '{digit}' after eliminating from letter '{letter}'.")

        self._assign_if_unique(letter, digit)

    def _assign_if_unique(self, letter: str, digit: int) -> None:
        """
        If a letter has only one candidate digit, assign it.
        If a digit is narrowed to exactly two letters, eliminate that digit from all other letters.

        Args:
            letter (str): The letter to check for unique digit assignment.
            digit (int): The digit to check for narrowing letters.
        """
        digit_candidates = self._letter_map[letter]

        if len(digit_candidates) == 1:
            assigned_digit = next(iter(digit_candidates))
            print(f"Letter {letter} assigned to digit {assigned_digit}")

        letter_candidates = self._digit_map[digit]

        if len(letter_candidates) == 2:
            print(f"Digit {digit} narrowed to letters: {letter_candidates}")
            for other_letter in self._letter_map:
                if other_letter not in letter_candidates and digit in self._letter_map[other_letter]:
                    self.eliminate(other_letter, digit)

    def __str__(self) -> str:
        """
        Return a string representation of the current letter-to-digit and digit-to-letter mappings.
        """
        lines = ["Letter to digits:"]
        for letter, digits in self._letter_map.items():
            lines.append(f"  {letter}: {sorted(digits)}")
        lines.append("Digit to letters:")
        for digit, letters in self._digit_map.items():
            lines.append(f"  {digit}: {sorted(letters)}")
        return "\n".join(lines)
    
    @property
    def letter_map(self) -> Dict[str, Set[int]]:
        """Get the current letter to digits mapping."""
        return self._letter_map
    
    @property
    def digit_map(self) -> Dict[int, Set[str]]:
        """Get the current digit to letters mapping."""
        return self._digit_map
