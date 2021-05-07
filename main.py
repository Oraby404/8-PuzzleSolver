class Puzzle:
    def __init__(self, initial_state, parent, action):
        self.initial_state = initial_state
        self.parent = parent
        self.children = []
        self.action = action
        self.depth = 0
        self.heuristic = 0

        for i in range(3):
            for j in range(3):
                if self.initial_state[i][j] == 0:
                    self.blank_row = i + 1
                    self.blank_col = j + 1
                    break

        #def Up(self):

        #def Down(self):

        #def Left(self):

        #def Right(self):


goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
board = Puzzle([[1, 2, 5],
                [3, 0, 4],
                [6, 7, 8]], None, None)

print(board.blank_row)
print(board.blank_col)
