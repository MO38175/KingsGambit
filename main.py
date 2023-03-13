import chess
from collections import Counter

DATAFILE = 'games.csv'

column_reference = {}
chess_games = []
winners = []
current_states = []

# Load in the data
with open(DATAFILE, 'r') as f:
    lines = f.readlines()
    for i in range(len(lines)):
        if (i == 0):
            columns = lines[i].split(',')
            for j in range(len(columns)):
                column_reference[columns[j].strip()] = j
        else:
            current_states.append(((lines[i].split(',')[column_reference['winner']]), lines[i].split(',')[column_reference['moves']].split(' ')))

# Engine init
player = 0
while ((player != 1) and (player != 2)):
    print('What piece are you?\n1. White\n2. Black')
    player = int(input())
board = chess.Board()

# Engine loop
turn_counter = 0
while (True):

    # Say whos turn it is
    if (turn_counter % 2 == 0):
        print('==WHITE\'S TURN==')
    else:
        print('==BLACK\'S TURN==')

    # Print the board
    print(board)

    # Get a legal move
    move = str()
    valid_move = False
    while (not valid_move):
        print('Move : ', end='')
        move = input()
        try:
            board.push_san(move)
            valid_move = True
        except chess.InvalidMoveError:
            print('The move you entered is not a valid move in Short Algebraic Notaion (SAN)')
        except chess.IllegalMoveError:
            print('The move you entered it not legal in the current state of the game')

    # Update the list of possible states
    new_states = []
    for i in range(len(current_states)):
        if current_states[i][1][0] == move:
            trimmed_state = current_states[i][1][1:]
            if len(trimmed_state) != 0:
                new_states.append((current_states[i][0], trimmed_state))
    current_states = new_states

    # Show the top 5 moves to come next
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
    total_elements = len(current_states)
    if (player == 1):
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

    # Increment the turn counter
    turn_counter += 1
