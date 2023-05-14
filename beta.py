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
        except chess.AmbiguousMoveError:
            print('You are confusing me, there are two or more pieces that can move to that square.')
            print('When two (or more) identical pieces can move to the same square, the moving piece is uniquely identified by specifying the piece\'s letter followed by (in order of preference)...')
            print('1. The file (letter) the piece you want to move is leaving from')
            print('2. The rank (number) the piece you want to move is leaving from')
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

# State pruning
def prune(move):
    global current_states

    new_states = []
    for i in range(len(current_states)):
        if current_states[i][1][0] == move:
            trimmed_state = current_states[i][1][1:]
            if len(trimmed_state) != 0:
                new_states.append((current_states[i][0], trimmed_state))
    current_states = new_states

# Convert to the notation that helps make an arrow
def san_to_lan(move, board):
    piece_map = {'P' : 1, 'N': 2, 'B' : 3, 'R' : 4, 'Q' : 5, 'K' : 6}

    piece = 'P'
    check = False

    # Normal move
    if (move[0].isupper()) and (move[0] != 'O') and (move[-1] != '+'):
        piece = move[0]

    # Check move
    elif move[-1] == '+':
        check = True

    # Castle move
    elif move[0] == 'O':
        if move == 'O-O':
            if board.turn == chess.WHITE:
                return chess.Move.from_uci('e1g1')
            return chess.Move.from_uci('e8g8')
        if board.turn == chess.WHITE:
            return chess.Move.from_uci('e1c1')
        return chess.Move.from_uci('e8c8')

    if (check):
        destination_square = move[1:-1]
    else:
        destination_square = move[-2:]

    possible_moves = []
    for move in board.generate_legal_moves():
        if move.to_square == chess.parse_square(destination_square):
            if board.piece_type_at(move.from_square) == piece_map[piece]:
                possible_moves.append(move)
    return possible_moves[0]

def fix_draw_order():
    # Load in the svg file
    svg_file = open("temp.svg", 'r')
    contents = ''
    char = svg_file.read(1)
    while char:
        contents += char
        char = svg_file.read(1)
    svg_file.close()

    # Split the file up by <...> tokens
    contents = contents.split('<')
    for i in range(len(contents)):
        if i != 0:
            contents[i] = '<' + contents[i]

    # Move where the pieces are drawn
    pieces = []
    for token in contents:
        if 'use' in token:
            pieces.append(token)
    for piece in pieces:
        contents.remove(piece)

    # Reconstruct the svg
    new_contents = ''
    for i in range(len(contents) - 1):
        new_contents += contents[i]
    for piece in pieces:
        new_contents += piece
    new_contents += '</svg>'

    # Write over the svg file with the new contents
    svg_file = open('temp.svg', 'w')
    svg_file.write(new_contents)
    svg_file.close()

def change_squares():
    # Load in the svg file
    svg_file = open("temp.svg", 'r')
    contents = ''
    char = svg_file.read(1)
    while char:
        contents += char
        char = svg_file.read(1)
    svg_file.close()

    # Split the file up by <...> tokens
    contents = contents.split('<')
    for i in range(len(contents)):
        if i != 0:
            contents[i] = '<' + contents[i]

    # Move where the pieces are drawn
    pieces = []
    for token in contents:
        if 'use' in token:
            pieces.append(token)
    for piece in pieces:
        contents.remove(piece)

    # Reconstruct the svg
    new_contents = ''
    for i in range(len(contents) - 1):
        new_contents += contents[i]
    for piece in pieces:
        new_contents += piece
    new_contents += '</svg>'

    # Refill the squares with better colors
    new_contents = new_contents.replace('#d18b47', '#3a6289')
    new_contents = new_contents.replace('#ffce9e', '#adc5ce')

    # Write over the svg file with the new contents
    svg_file = open('temp.svg', 'w')
    svg_file.write(new_contents)
    svg_file.close()

def loop():
    global turn_counter

    # Window element that holds the svg image
    chess_window = tk.Label(window)

    # Engine loop
    while True:

        # Who's turn is it?
        if turn_counter % 2 == 0:
            print('==WHITE\'S TURN==')
        else:
            print('==BLACK\'S TURN==')

        # Get the top 5 moves in LAN format
        five_moves = get_top_five()
        print('Top 5 Moves', five_moves)
        lan_five_moves = []
        for i in range(len(five_moves)):
            lan_five_moves.append(san_to_lan(five_moves[i][0], board))

        # Make the render
        arrows = []
        colors = ['#639754', '#7bb662', '#ffd301', '#e03c32', '#d61f1f']
        for i in range(len(lan_five_moves)):
            arrows.append(chess.svg.Arrow(lan_five_moves[i].from_square, lan_five_moves[i].to_square, color=colors[i]))
        render = chess.svg.board(board, arrows=arrows)

        # Display the new image
        with open('temp.svg', 'w') as f:
            f.write(render)
        f.close()

        change_squares()
        image_data = cairosvg.svg2png(url="temp.svg")
        image = Image.open(io.BytesIO(image_data))
        tk_image = ImageTk.PhotoImage(image)
        chess_window.configure(image=tk_image)
        chess_window.pack()

        # Await a legal move
        move = get_move(board)

        # Prune the remaining states
        prune(move)

        # Increment turn
        turn_counter += 1

if __name__ == '__main__':
    window = tk.Tk()
    load_data()
    while ((player != 1) and (player != 2)):
        print('What piece are you?\n1. White\n2. Black')
        player = int(input())
    board = chess.Board()
    loop()
    window.mainloop()
