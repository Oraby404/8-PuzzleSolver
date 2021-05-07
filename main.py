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

    def is_goal(self):
        return list(self.board_config) == goal

    def bfs(self):
        node = Puzzle(deepcopy(self.board_config))
        frontier = [node]
        explored = []

        while len(frontier) != 0:
            # queue
            node = frontier.pop(0)
            explored.append(node)

            if node.is_goal():
                print(node.board_config)
                break

            for child in node.expand():
                if child not in frontier and child not in explored:
                    frontier.append(child)

    def dfs(self):
        node = Puzzle(deepcopy(self.board_config))
        frontier = [node]
        explored = []

        while len(frontier) != 0:
            # stack
            node = frontier.pop()
            explored.append(node)

            if node.is_goal():
                print(node.board_config)
                break

            for child in node.expand():
                if child not in frontier and child not in explored:
                    frontier.append(child)


goal = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]

board = Puzzle([[0, 1, 2],
                [4, 3, 5],
                [6, 7, 8]])

board.dfs()
