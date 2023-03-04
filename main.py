import chess
import chess.svg

DATAFILE = 'games.csv'

column_reference = {}
chess_games = []

# Load the moves of each game into the list "chess_games"
def load_games():
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
    return

# Print the board safely
def print_board(board, player):
    # White player case
    if (player == 1):
        print(board)
    # Black player case
    else:
        board.apply_transform(chess.flip_vertical)
        print(board)
        board.apply_transform(chess.flip_vertical)
    
def get_move(board):
    move = str()
    legal = False
    while (not legal):
        print(board.legal_moves)
        print('Move : ', end='')
        move = input()
        move = chess.Move.from_uci(move)
        if (move in board.legal_moves):
            print('legal')
            legal = True
        else:
            print('not legal')
            legal = False
    return move

if __name__ == '__main__':
    load_games()
    
    # Is the player black or white?
    player_piece = 0
    while ((player_piece != 1) and (player_piece != 2)):
        print('What piece are you?\n1. White\n2. Black')
        player_piece = int(input())

    # Create a new board
    board = chess.Board()

    while (True):
        print_board(board, player_piece)
        move = get_move(board)
        board.push(move)
