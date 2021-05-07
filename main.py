from copy import deepcopy


class Puzzle:
    def __init__(self, board_config):
        self.board_config = board_config
        self.children = []
        # self.parent = parent
        # self.action = action
        # self.depth = 0
        # self.heuristic = 0

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
            new_node = Puzzle(deepcopy(self.board_config))
            new_node.blank_row -= 1
            i = self.blank_row - 1
            j = self.blank_col - 1
            new_node.board_config[i - 1][j], new_node.board_config[i][j] = new_node.board_config[i][j], \
                                                                           new_node.board_config[i - 1][j]
            return new_node

    def down(self):
        if self.blank_row == 3:
            return None
        else:
            new_node = Puzzle(deepcopy(self.board_config))
            new_node.blank_row += 1
            i = self.blank_row - 1
            j = self.blank_col - 1
            new_node.board_config[i + 1][j], new_node.board_config[i][j] = new_node.board_config[i][j], \
                                                                           new_node.board_config[i + 1][j]
            return new_node

    def left(self):
        if self.blank_col == 1:
            return None
        else:
            new_node = Puzzle(deepcopy(self.board_config))
            new_node.blank_col -= 1
            i = self.blank_row - 1
            j = self.blank_col - 1
            new_node.board_config[i][j - 1], new_node.board_config[i][j] = new_node.board_config[i][j], \
                                                                           new_node.board_config[i][j - 1]
            return new_node

    def right(self):
        if self.blank_col == 3:
            return None
        else:
            new_node = Puzzle(deepcopy(self.board_config))
            new_node.blank_col += 1
            i = self.blank_row - 1
            j = self.blank_col - 1
            new_node.board_config[i][j + 1], new_node.board_config[i][j] = new_node.board_config[i][j], \
                                                                           new_node.board_config[i][j + 1]
            return new_node

    def expand(self):
        if len(self.children) == 0:

            up_child = self.up()
            if up_child is not None:
                self.children.append(up_child)

            down_child = self.down()
            if down_child is not None:
                self.children.append(down_child)

            left_child = self.left()
            if left_child is not None:
                self.children.append(left_child)

            right_child = self.right()
            if right_child is not None:
                self.children.append(right_child)

        return self.children


goal = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]

board = Puzzle([[1, 2, 5],
                [3, 0, 4],
                [6, 7, 8]])

print(board.blank_row)
print(board.blank_col)

board.children = board.expand()

print(board.children[0].blank_row)
print(board.children[0].blank_col)

print(board.children[1].blank_row)
print(board.children[1].blank_col)

print(board.children[2].blank_row)
print(board.children[2].blank_col)

print(board.children[3].blank_row)
print(board.children[3].blank_col)
