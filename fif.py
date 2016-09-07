#!/usr/bin/env python3

import random
import time
import sys
import curses


VALID_MOVES = "wasd"
SOLVED_BOARD = [[" 1"," 2"," 3"," 4"], [" 5"," 6"," 7"," 8"],
                [" 9","10","11","12"], ["13","14","15"," "]]


def empty_finder(board):
    for i in range(4):
        if "  " in board[i]:
            for g in range(4):
                if "  " in board[i][g]:
                    return [i, g]


def IsOppMove(cs,lm):
    """determines if random move (for scramble)
    would just undo what has just been done"""
    if (lm == "w" and cs == "s") or (lm == "s" and cs == "w"):
        return True
    elif (lm == "a" and cs == "d") or (lm == "d" and cs == "a"):
        return True
    else:
        return False


def IsValid(move, board):
    e = empty_finder(board)
    if move.lower() == "quit":
        sys.exit()
    elif len(move) > 1:
        return False
    elif move not in VALID_MOVES:
        return False
    elif (move == "w" and e[0] == 3) or (move == "s" and e[0] == 0):
        return False
    elif (move == "d" and e[1] == 0) or (move == "a" and e[1] == 3):
        return False
    else:
        return True


def mover(move, board):
    e = empty_finder(board)
    if move == "s":
        board[e[0]][e[1]] = board[e[0] - 1][e[1]]
        board[e[0] - 1][e[1]] = "  "
    elif move == "d":
        board[e[0]][e[1]] = board[e[0]][e[1] - 1]
        board[e[0]][e[1] - 1] = "  "
    elif move == "w":
        board[e[0]][e[1]] = board[e[0] + 1][e[1]]
        board[e[0] + 1][e[1]] = "  "
    elif move == "a":
        board[e[0]][e[1]] = board[e[0]][e[1] + 1]
        board[e[0]][e[1] + 1] = "  "


def scrambler():
    dupe = [[" 1"," 2"," 3"," 4"], [" 5"," 6"," 7"," 8"],
            [" 9","10","11","12"], ["13","14","15","  "]]
    last_move = ""
    for i in range(150):
        current_rand = random.randrange(4)
        current_scramble = VALID_MOVES[current_rand]
        if not IsOppMove(current_scramble, last_move):
            if IsValid(current_scramble, dupe):
                mover(current_scramble, dupe)
    return dupe


def show_board(board):
    for i in board:
        print("____________")
        print("|" + "|".join(i) + "|")
    print("____________")


def main():
    print("""Play the world famous Fifteen Puzzle!
Use WASD + Enter to move the tiles into the following order:
from left to right and top to bottom the numbers
from highest to lowest.

Use Ctrl-C to exit the program.""")

    while True:
        scrambled = scrambler()
        start_time = time.time()
        while scrambled != SOLVED_BOARD:
            print()
            show_board(scrambled)
            print()
            move = (input("Your move: ")).lower()
            if IsValid(move, scrambled):
                mover(move, scrambled)
            else:
                print()
                print("That is not a valid move.")
        print()
        show_board(SOLVED_BOARD)
        print()
        end_time = time.time()
        elapsed = round(end_time - start_time)
        print("Congratulations! You have solved the world famous Fifteen puzzle in %s seconds!" % (elapsed))
        answer = input("Do you want to play again? (Y/N): ")
        answer = answer.lower()
        if answer[0] != "y":
            break


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("Thanks for playing!")
