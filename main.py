from copy import deepcopy


class Puzzle:
    def __init__(self, board_config):
        self.board_config = board_config
        # self.parent = parent
        self.children = []
        # self.action = action
        self.depth = 0
        self.heuristic = 0

        for i in range(3):
            for j in range(3):
                if self.board_config[i][j] == 0:
                    self.blank_row = i + 1
                    self.blank_col = j + 1
                    break

    def up(self):
        if self.blank_row == 1:
            return None
        else:
            self.blank_row -= 1
            i = self.blank_row - 1
            j = self.blank_col - 1
            new_node = deepcopy(self.board_config)
            new_node[i + 1][j], new_node[i][j] = new_node[i][j], new_node[i + 1][j]
            return Puzzle(new_node)

    def down(self):
        if self.blank_row == 3:
            return None
        else:
            self.blank_row += 1
            i = self.blank_row - 1
            j = self.blank_col - 1
            new_node = deepcopy(self.board_config)
            new_node[i - 1][j], new_node[i][j] = new_node[i][j], new_node[i - 1][j]
            return Puzzle(new_node)

    def left(self):
        if self.blank_col == 1:
            return None
        else:
            self.blank_col -= 1
            i = self.blank_row - 1
            j = self.blank_col - 1
            new_node = deepcopy(self.board_config)
            new_node[i][j + 1], new_node[i][j] = new_node[i][j], new_node[i][j + 1]
            return Puzzle(new_node)

    def right(self):
        if self.blank_col == 3:
            return None
        else:
            self.blank_col += 1
            i = self.blank_row - 1
            j = self.blank_col - 1
            new_node = deepcopy(self.board_config)
            new_node[i][j - 1], new_node[i][j] = new_node[i][j], new_node[i][j - 1]
            return Puzzle(new_node)


goal = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]

board = Puzzle([[1, 2, 5],
                [3, 0, 4],
                [6, 7, 8]])
