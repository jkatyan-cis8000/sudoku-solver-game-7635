#!/usr/bin/env python3
"""
Classic Sudoku Puzzle Game
A 9x9 grid where each row, column, and 3x3 subgrid must contain digits 1-9 exactly once.
"""

import random
import os


def generate_puzzle(difficulty: int = 30) -> tuple[list[list[int]], list[list[int]]]:
    """
    Generate a Sudoku puzzle and its solution.
    
    Args:
        difficulty: Number of empty cells (30-60 recommended)
    
    Returns:
        Tuple of (puzzle with empty cells, solution grid)
    """
    # Start with empty board
    board = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill diagonal 3x3 boxes (independent, so safe to randomize)
    for i in range(0, 9, 3):
        fill_box(board, i, i)
    
    # Solve to get a complete valid board
    solution = [row[:] for row in board]
    solve_sudoku(solution)
    
    # Create puzzle by removing cells
    puzzle = [row[:] for row in solution]
    cells_to_remove = min(max(difficulty, 30), 60)
    
    removed = 0
    while removed < cells_to_remove:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            removed += 1
    
    return puzzle, solution


def fill_box(board: list[list[int]], row: int, col: int) -> None:
    """Fill a 3x3 box with random valid numbers."""
    nums = list(range(1, 10))
    random.shuffle(nums)
    
    idx = 0
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = nums[idx]
            idx += 1


def solve_sudoku(board: list[list[int]]) -> bool:
    """Solve Sudoku using backtracking. Returns True if solved."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def is_valid(board: list[list[int]], row: int, col: int, num: int) -> bool:
    """Check if placing num at (row, col) is valid."""
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    if num in [board[r][col] for r in range(9)]:
        return False
    
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False
    
    return True


def validate_move(board: list[list[int]], row: int, col: int, value: int, 
                  initial_cells: set) -> tuple[bool, str]:
    """
    Validate a user's move.
    
    Returns:
        Tuple of (is_valid, message)
    """
    if (row, col) in initial_cells:
        return False, "Cannot modify initial puzzle cells."
    
    if not (1 <= value <= 9):
        return False, "Value must be between 1 and 9."
    
    if not (0 <= row <= 8 and 0 <= col <= 8):
        return False, "Row and column must be between 0 and 8."
    
    # Temporarily place and check validity
    if not is_valid(board, row, col, value):
        return False, f"Invalid move: {value} conflicts with existing number in row, column, or box."
    
    return True, "Valid move."


def is_complete(board: list[list[int]]) -> bool:
    """Check if the board is completely filled and valid."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False
    
    # Verify validity of complete board
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            board[row][col] = 0
            if not is_valid(board, row, col, num):
                board[row][col] = num
                return False
            board[row][col] = num
    
    return True


def get_initial_cells(puzzle: list[list[int]]) -> set:
    """Return set of positions that are initially filled (immutable)."""
    return {(r, c) for r in range(9) for c in range(9) if puzzle[r][c] != 0}


def display_board(board: list[list[int]], initial_cells: set) -> None:
    """Display the Sudoku board in a formatted grid."""
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print("\n" + "=" * 25)
    print("       SUDOKU GAME")
    print("=" * 25)
    
    for row in range(9):
        if row % 3 == 0 and row != 0:
            print("-" * 25)
        
        row_str = ""
        for col in range(9):
            if col % 3 == 0 and col != 0:
                row_str += " | "
            
            cell = board[row][col]
            if cell == 0:
                row_str += " . "
            elif (row, col) in initial_cells:
                row_str += f" \033[1m{cell}\033[0m "  # Bold for initial cells
            else:
                row_str += f" {cell} "
        
        print(f"  {row_str}")
    
    print("=" * 25)
    print("\nInstructions:")
    print("  Enter: row col value (0-8 for positions, 1-9 for values)")
    print("  Example: '4 5 7' places 7 at row 4, column 5")
    print("  Type 'quit' to exit, 'hint' for a random tip")
    print("  Type 'check' to verify your progress")


def get_user_input() -> tuple[int, int, int] | None:
    """Get and parse user input for move."""
    try:
        user_input = input("\nEnter move (row col value) or command: ").strip().lower()
        
        if user_input == 'quit':
            return None
        if user_input == 'hint':
            return ('hint',)
        if user_input == 'check':
            return ('check',)
        
        parts = user_input.split()
        if len(parts) != 3:
            print("Invalid format. Use: row col value")
            return ('error',)
        
        row, col, value = map(int, parts)
        return row, col, value
        
    except ValueError:
        print("Invalid input. Use numbers only.")
        return ('error',)


def display_message(message: str, is_error: bool = False) -> None:
    """Display a message to the user."""
    if is_error:
        print(f"\n\033[91mERROR: {message}\033[0m")
    else:
        print(f"\n\033[92m{message}\033[0m")


def play_sudoku_game(difficulty: int = 40) -> None:
    """
    Main game loop for Sudoku.
    
    Args:
        difficulty: Number of empty cells (30-60 recommended)
    """
    print("\n" + "=" * 40)
    print("   Welcome to Classic Sudoku!")
    print("=" * 40)
    print("\nDifficulty:", "Easy" if difficulty <= 35 else "Medium" if difficulty <= 50 else "Hard")
    print("Fill the 9x9 grid so each row, column, and 3x3 box contains 1-9.")
    
    # Generate puzzle
    puzzle, solution = generate_puzzle(difficulty)
    board = [row[:] for row in puzzle]
    initial_cells = get_initial_cells(puzzle)
    
    moves = 0
    hints = 0
    
    while True:
        display_board(board, initial_cells)
        
        user_input = get_user_input()
        
        if user_input is None:
            print("\nThanks for playing! The solution was:")
            display_board(solution, set())
            break
        
        if user_input[0] == 'hint':
            # Find an empty cell and reveal it
            empty_cells = [(r, c) for r in range(9) for c in range(9) 
                          if board[r][c] == 0 and (r, c) not in initial_cells]
            if empty_cells:
                row, col = random.choice(empty_cells)
                value = solution[row][col]
                board[row][col] = value
                hints += 1
                display_message(f"Hint: Placed {value} at row {row}, col {col}")
                moves += 1
            else:
                display_message("No empty cells left!")
            continue
        
        if user_input[0] == 'check':
            if is_complete(board):
                if board == solution:
                    display_message(f"\n🎉 CONGRATULATIONS! You solved the puzzle in {moves} moves with {hints} hints!")
                    break
                else:
                    display_message("\n⚠️  Board is full but has errors. Keep trying!", is_error=True)
            else:
                empty = sum(1 for r in range(9) for c in range(9) if board[r][c] == 0)
                display_message(f"Board has {empty} empty cells remaining.")
            continue
        
        if user_input[0] == 'error':
            continue
        
        row, col, value = user_input
        
        is_valid, message = validate_move(board, row, col, value, initial_cells)
        
        if is_valid:
            board[row][col] = value
            moves += 1
            display_message("✓ Move recorded!")
        else:
            display_message(message, is_error=True)
        
        # Check for win after valid move
        if is_complete(board):
            if board == solution:
                display_message(f"\n🎉 CONGRATULATIONS! You solved the puzzle in {moves} moves with {hints} hints!")
                break
            else:
                display_message("\n⚠️  Board is full but has errors. Keep trying!", is_error=True)
    
    print("\nThanks for playing Sudoku!")


if __name__ == "__main__":
    import sys
    
    # Parse difficulty from command line
    difficulty = 40
    if len(sys.argv) > 1:
        try:
            difficulty = int(sys.argv[1])
        except ValueError:
            print("Invalid difficulty. Using default (40).")
    
    play_sudoku_game(difficulty)
