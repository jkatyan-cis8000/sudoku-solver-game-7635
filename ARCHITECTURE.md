# Sudoku Game Architecture

## Module: SudokuGame
**Responsibility:** Core game logic including puzzle generation, validation, and game state management.

### Exposed Interfaces:
- `generate_puzzle(difficulty: int) -> tuple[list[list[int]], list[list[int]]]` - Generates a puzzle and its solution
- `validate_move(board: list[list[int]], row: int, col: int, value: int) -> bool` - Checks if a move is valid
- `is_complete(board: list[list[int]]) -> bool` - Checks if the puzzle is solved
- `get_initial_cells(puzzle: list[list[int]]) -> set[tuple[int, int]]` - Returns immutable cell positions

## Module: UserInterface
**Responsibility:** Handles user input, display, and interaction with the game.

### Exposed Interfaces:
- `display_board(board: list[list[int]], initial_cells: set) -> None` - Renders the grid
- `get_user_input() -> tuple[int, int, int] | None` - Gets row, col, value from user
- `display_message(message: str) -> None` - Shows feedback to user

## Module: Main
**Responsibility:** Orchestrates the game loop and ties all components together.

### Exposed Interfaces:
- `play_sudoku_game(difficulty: int = 30) -> None` - Main game entry point

## File Structure:
- `sudoku_game.py` - Core game logic
- `ui.py` - User interface components
- `main.py` - Game entry point

## Dependencies:
- Standard library only (no external packages)
