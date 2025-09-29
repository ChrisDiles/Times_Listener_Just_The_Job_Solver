# Crossword Solver

A Python tool to parse, represent, and solve numeric crossword puzzles by brute-force search with constraint propagation.

## Overview

This project is designed to solve numeric crosswords where each clue is a mathematical expression that must evaluate to a number matching the clue's length.  
It uses:

- **CrosswordStructure** to model the grid layout from bar locations.
- **ClueParser** to parse clue text and map each clue to its grid coordinates.
- **CrosswordSolver** to systematically try permutations of digit assignments, eliminate inconsistent candidates, and converge on a unique solution.

The solver updates possible values for each letter and grid cell, gradually narrowing the search space until the crossword is solved.

## Project Structure

```text
.
├── main.py                # Entry point
├── crossword_structure.py # CrosswordStructure class
├── parser.py              # ClueParser class
├── solver.py              # CrosswordSolver class
├── grid.py                # Grid and Cell classes
├── bar_locations.json     # JSON describing grid bar layout
└── clues.txt              # Text file containing crossword clues
```

## How It Works

### 1. Load Grid Layout
**CrosswordStructure** parses `bar_locations.json` to determine cell layout and clue coordinates.

### 2. Parse Clues
**ClueParser** reads `clues.txt`, creating **Clue** instances linked to the grid coordinates.

### 3. Solve Iteratively
**CrosswordSolver** uses brute-force search with constraint propagation:

- Tries valid digit assignments for each clue (within a permutation limit).
- Eliminates inconsistent digits from **DigitLetterMap**.
- Narrows down possible values for each **Cell** in the **Grid**.

### 4. Output Solution
The solved **letter-to-digit map** is displayed, followed by the solved **grid**.

## Example Usage

Run the solver from the command line:

```bash
python main.py
```

## Example Output

```
Solving clue 1 Across — 120 permutations
Eliminated {3, 5, 7} from 'A'
Eliminated {2, 4} from 'B'
Solving clue 2 Down — 60 permutations
Eliminated {0, 6} from 'C'

Solved Letters:
A = 1
B = 9
C = 8
...

Solved Grid:
+---+---+---+
| 1 | 9 | 8 |
+---+---+---+
| 7 | 4 | 2 |
+---+---+---+
| 6 | 3 | 5 |
+---+---+---+
```


## Requirements

- Python **3.9+**
- Dependencies:
  - `tqdm` (for progress bars)

Install requirements:

```bash
pip install tqdm
```

## Notes

- Input files:
  - `bar_locations.json` defines the grid layout (rows, columns, and bars).
  - `clues.txt` contains the crossword clues with directions and mathematical expressions.
- The solver uses brute-force search with **constraint propagation**, which works efficiently for most puzzles but may be slow if permutation limits are very high.
- Letters are mapped to digits consistently across all clues. Each letter corresponds to at most one digit, and no digit may be assigned to more than two letters.
