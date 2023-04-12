import chess
import chess.svg
import cairosvg
import io
import tkinter as tk
from PIL import Image,ImageTk

BOARD_SIZE = 400
BORDER_RATIO = 0.0385
SQUARE_RATIO = 0.115375

def find_coordinate(mx, my):
    # Letters in the x direction, a->h, Numbers in the y direction, 8->1
    letter_map = {0 : 'a', 1 : 'b', 2 : 'c', 3 : 'd', 4 : 'e', 5 : 'f', 6 : 'g', 7 : 'h'}
    number_map = {0 : 8, 1 : 7, 2 : 6, 3 : 5, 4 : 4, 5 : 3, 6 : 2, 7 : 1}

    coord_x = None
    coord_y = None

    # Border offset
    actual_board_start = BOARD_SIZE * BORDER_RATIO
    actual_board_end = BOARD_SIZE - (BOARD_SIZE * BORDER_RATIO)

    # Check the x coordinate
    for i in range(8):
        square_start = (actual_board_start + (BOARD_SIZE * SQUARE_RATIO * i))
        square_end = (actual_board_start + (BOARD_SIZE * SQUARE_RATIO * (i + 1)))
        if (mx > square_start) and (mx < square_end):
            coord_x = letter_map[i]

    # Check the y coordinate
    for i in range(8):
        square_start = (actual_board_start + (BOARD_SIZE * SQUARE_RATIO * i))
        square_end = (actual_board_start + (BOARD_SIZE * SQUARE_RATIO * (i + 1)))
        if (my > square_start) and (my < square_end):
            coord_y = number_map[i]

    coordinate = (coord_x, coord_y)
    return coordinate

# The click functions
def on_click(event):
    coordinate = find_coordinate(event.x, event.y)

# The chess board
board = chess.Board()

# Convert the board to an SVG image
board_svg = chess.svg.board(board=board, size=BOARD_SIZE)
with open('temp.svg', 'w') as f:
    f.write(board_svg)
f.close()

# Tkinter crap I got from online
main=tk.Tk()

image_data = cairosvg.svg2png(url="temp.svg")
image = Image.open(io.BytesIO(image_data))
tk_image = ImageTk.PhotoImage(image)

button=tk.Label(main, image=tk_image)
button.pack(expand=True, fill="both")

# Bind the "<Button-1>" event to the on_click function and the image that is tied to button
button.bind("<Button-1>", on_click)

main.mainloop()
