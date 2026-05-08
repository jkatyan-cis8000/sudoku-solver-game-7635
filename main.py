#!/usr/bin/env python3
"""
Classic Sudoku - Main Entry Point
Play a 9x9 Sudoku puzzle with validation and completion checking.
"""

from sudoku_game import play_sudoku_game

if __name__ == "__main__":
    import sys
    
    # Default difficulty (number of empty cells)
    difficulty = 40
    
    if len(sys.argv) > 1:
        try:
            difficulty = int(sys.argv[1])
            if not 20 <= difficulty <= 70:
                print("Difficulty should be between 20 and 70. Using default (40).")
                difficulty = 40
        except ValueError:
            print("Invalid difficulty. Using default (40).")
    
    play_sudoku_game(difficulty)
