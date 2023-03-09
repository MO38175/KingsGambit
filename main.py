import chess

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
            pass
        else:
            chess_games.append(lines[i].split(',')[column_reference['moves']].split(' '))
            winners.append(lines[i].split(',')[column_reference['winner']])

# Engine init
current_states = chess_games
player = 0
while ((player != 1) and (player != 2)):
    print('What piece are you?\n1. White\n2. Black')
    player = int(input())
board = chess.Board()

# Engine loop
turn_counter = 0
while (True):
    print(len(current_states))

    # Say whos turn it is
    if (turn_counter % 2 == 0):
        print('==WHITE\'S TURN==')
    else:
        print('==BLACK\'S TURN==')

    # Print the board
    if (player == 1):
        print(board)
    else:
        board.apply_transform(chess.flip_vertical)
        print(board)
        board.apply_transform(chess.flip_vertical)

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
        if current_states[i][0] == move:
            trimmed_state = current_states[i][1:]
            if len(trimmed_state) != 0:
                new_states.append(trimmed_state)
    current_states = new_states

    # Increment the turn counter
    turn_counter += 1