import io
import tkinter as tk
from collections import Counter

import chess
import chess.svg
import cairosvg
from PIL import Image,ImageTk


# Constants
DATAFILE = 'games.csv'

# Global Variables
column_reference = {}
winners = []
current_states = []
turn_counter = 0
player = 0 # 1 = white, 2 = black

# Dataloader
def load_data():
    with open(DATAFILE, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if i == 0:
                columns = lines[i].split(',')
                for j in range(len(columns)):
                    column_reference[columns[j].strip()] = j
            else:
                current_states.append(((lines[i].split(',')[column_reference['winner']]), lines[i].split(',')[column_reference['moves']].split(' ')))

# The move getter
def get_move(board):
    move = str()
    valid_move = False
    while not valid_move:
        print('Move : ', end='')
        move = input()
        try:
            board.push_san(move)
            valid_move = True
        except chess.InvalidMoveError:
            print('The move you entered is not a valid move in Short Algebraic Notaion (SAN)')
        except chess.IllegalMoveError:
            print('The move you entered it not legal in the current state of the game')
    return move

# Top 5 Moves
def get_top_five():
    next_moves = []
    for i in range(len(current_states)):
        if (turn_counter % 2) == 0:
            if current_states[i][0] == 'black':
                next_moves.append(current_states[i][1][0])
        else:
            if current_states[i][0] == 'white':
                next_moves.append(current_states[i][1][0])
    counted = Counter(next_moves)
    top_five = counted.most_common(5)
    return top_five
    '''
    total_elements = len(current_states)
    if player == 1:
        if (turn_counter % 2) == 0:
            print('Moves Black is likely to play')
        else:
            print('Moves you could play')
    else:
        if (turn_counter % 2) == 1:
            print('Moves White is likely to play')
        else:
            print('Moves you could play')
    for element, count in top_five:
        percentage = (count / total_elements) * 100
        print(f"{element}: {percentage:.2f}%")
    '''

# State pruning
def prune(move):
    new_states = []
    for i in range(len(current_states)):
        if current_states[i][1][0] == move:
            trimmed_state = current_states[i][1][1:]
            if len(trimmed_state) != 0:
                new_states.append((current_states[i][0], trimmed_state))
    current_states = new_states

if __name__ == '__main__':
    # Setup stuff
    load_data()
    while ((player != 1) and (player != 2)):
        print('What piece are you?\n1. White\n2. Black')
        player = int(input())
    board = chess.Board()

    # Engine loop
    while True:
        # Who's turn is it?
        if turn_counter % 2 == 0:
            print('==WHITE\'S TURN==')
        else:
            print('==BLACK\'S TURN==')

        # Render the board with the top five arrows
        get_top_five()

        # Await a legal move
        move = get_move(board)

        # Prune the remaining states
        prune(move)

        # Increment turn
        turn_counter += 1

        # Repeat
