from crossword_structure import CrosswordStructure
from parser_1 import ClueParser
from solver import CrosswordSolver

def main():
    """
    Main entry point to parse crossword structure and clues,
    then solve the crossword puzzle and display the solution.

    Expects:
    - 'bar_locations.json' containing JSON with "Vertical" and "Horizontal" bars.
    - 'clues.txt' containing clues in the expected format with directions and clue expressions.

    The solved grid and solved letters are printed to the console.
    """
    try:
        # Load bar locations JSON
        with open("bar_locations.json", "r") as f:
            bar_locations_json = f.read()

        # Load clues text
        with open("clues.txt", "r") as f:
            clues_text = f.read()

        # Parse crossword structure
        structure = CrosswordStructure(bar_locations_json)

        # Parse clues with clue coordinates
        clue_parser = ClueParser(clues_text, structure.clue_coords)

        # Initialize solver and solve puzzle
        solver = CrosswordSolver(structure, clue_parser)
        solver.solve()

        # Show solved letters summary
        solved_letters = {letter: solver.dlm.letter_map[letter] for letter in sorted(solver.dlm.letter_map)}
        print("\nSolved letters:")
        for letter, digits in solved_letters.items():
            print(f"  {letter}: {sorted(digits)}")

        # Print solved grid
        print("\nSolved Grid:")
        print(solver.grid)

    except FileNotFoundError as e:
        print(f"Error: Missing file - {e.filename}")
    except ValueError as e:
        print(f"Solving error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
