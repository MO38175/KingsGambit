# Constants
DATAFILE = 'games.csv'

# "Global" variables
column_reference = {}
root_nodes = []

class TreeNode:
    def __init__(self, move, turn):
        # Self explanitory
        self.move = move

        # The turn counter of this node
        self.turn = turn

        # Dataset indices that match the path to this node
        self.data = []

        # Children of this node
        self.children = []
    
    def __str__(self):
        return f'Move : {self.move}\nTurn : {self.turn}\nData : {self.data}'

    def insert(self, path, turn, idx):
        # Don't go over the bounds of the path length
        if len(path) <= turn:
            return

        # The path no longer matches
        if self.move != path[turn]:
            return
        
        # Add the index into the node
        self.data.append(idx)

        # If we are at the end of the, stop
        if len(path) <= (turn + 1):
            return
        else:
            # Always make a node if there are no children
            if len(self.children) == 0:
                self.children.append(TreeNode(path[turn + 1], turn + 1))
            else:
                # Only make a node if there are no child nodes equal to path[turn]
                match = False
                for child in enumerate(self.children):
                    if path[turn + 1] == child[1].move:
                        match = True
                        break
                if not match:
                    self.children.append(TreeNode(path[turn + 1], turn + 1))

        # Make a new node if none of the children have path[turn+1] as their move
        for child in self.children:
            child.insert(path, turn + 1, idx)

# Load in the data
lines = []
with open(DATAFILE, 'r') as df:
    lines = df.readlines()
games = []
for i in enumerate(lines):
    if i[0] == 0:
        columns = i[1].split(',')
        for j in enumerate(columns):
            column_reference[j[1].strip()] = j[0]
    else:
        games.append(i[1].split(',')[12].split(' '))

# Get the root nodes, one for each unique first move in the game
roots = []
for game in enumerate(games):
    moves = []
    for node in enumerate(roots):
        if node[1].move not in moves:
            moves.append(node[1].move)
    if game[1][0] not in moves:
        roots.append(TreeNode(game[1][0], 0))

# Make the tree
for game in enumerate(games):
    for root in enumerate(roots):
        root[1].insert(game[1], 0, game[0])

# Kind of validate the tree
d4 = []
for game in enumerate(games):
    if game[1][0] == 'd4':
        d4.append(game[1])
moves_following_d4_in_data = []
for game in enumerate(d4):
    try:
        if game[1][1] not in moves_following_d4_in_data:
            moves_following_d4_in_data.append(game[1][1])
    except IndexError:
        pass
print(moves_following_d4_in_data)
moves_following_d4_in_tree = []
for node in enumerate(roots[0].children):
    if node[1].move not in moves_following_d4_in_tree:
        moves_following_d4_in_tree.append(node[1].move)
print(moves_following_d4_in_tree)

print(roots[1].children[0].children[0])