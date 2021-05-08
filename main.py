from copy import deepcopy
import time


class Puzzle:
    def __init__(self, board_config, action="Initial"):
        self.board_config = board_config
        self.children = []
        self.action = action
        self.parent = []
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
            new_node = Puzzle(deepcopy(self.board_config), action="up")
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
            new_node = Puzzle(deepcopy(self.board_config), action="down")
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
            new_node = Puzzle(deepcopy(self.board_config), action="left")
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
            new_node = Puzzle(deepcopy(self.board_config), action="right")
            new_node.blank_col += 1
            i = self.blank_row - 1
            j = self.blank_col - 1
            new_node.board_config[i][j + 1], new_node.board_config[i][j] = new_node.board_config[i][j], \
                                                                           new_node.board_config[i][j + 1]
            return new_node

    def expand(self):
        if len(self.children) == 0:
            last_action = self.action

            right_child = self.right()
            if right_child is not None and last_action != "left":
                self.children.append(right_child)

            left_child = self.left()
            if left_child is not None and last_action != "right":
                self.children.append(left_child)

            down_child = self.down()
            if down_child is not None and last_action != "up":
                self.children.append(down_child)

            up_child = self.up()
            if up_child is not None and last_action != "down":
                self.children.append(up_child)

        return self.children

    def is_goal(self):
        return list(self.board_config) == goal

    def bfs(self):
        node = Puzzle(deepcopy(self.board_config), action="Initial")
        frontier = [node]
        frontier_boards = [node.board_config]
        explored = []
        path = []
        explored_nodes = 0
        start_time = time.time()

        while len(frontier) != 0:
            # queue
            node = frontier.pop(0)
            frontier_boards.pop(0)
            explored.append(node.board_config)
            explored_nodes += 1

            if node.is_goal():
                running_time = time.time() - start_time
                while node.action != "Initial":
                    path.append(node.action)
                    node = node.parent
                print("Path to Goal :", path[::-1])
                print("Cost of Path : ", len(path))
                print("Nodes Expanded : ", explored_nodes)
                print("Search Depth : ", len(path))
                print("Running Time : ", running_time)
                break

            for child in node.expand():
                if child.board_config not in frontier_boards and child.board_config not in explored:
                    child.parent = node
                    frontier.append(child)
                    frontier_boards.append(child.board_config)

    def dfs(self):
        node = Puzzle(deepcopy(self.board_config), action="Initial")
        frontier = [node]
        frontier_boards = [node.board_config]
        explored = []
        path = []
        explored_nodes = 0
        start_time = time.time()

        while len(frontier) != 0:
            # stack
            node = frontier.pop()
            frontier_boards.pop()
            explored.append(node.board_config)
            explored_nodes += 1

            if node.is_goal():
                running_time = time.time() - start_time
                while node.action != "Initial":
                    path.append(node.action)
                    node = node.parent
                print("Path to Goal :", path[::-1])
                print("Cost of Path : ", len(path))
                print("Nodes Expanded : ", explored_nodes)
                print("Search Depth : ", len(path))
                print("Running Time : ", running_time)
                break

            for child in node.expand():
                if child.board_config not in frontier_boards and child.board_config not in explored:
                    child.parent = node
                    frontier.append(child)
                    frontier_boards.append(child.board_config)

    def is_solvable(self):
        inv_count = 0
        for i in range(0, 2):
            for j in range(i + 1, 3):
                if self.board_config[j][i] > 0 and self.board_config[j][i] > self.board_config[i][j]:
                    inv_count += 1
        # not solvable if odd count
        return inv_count % 2 == 0


goal = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]

board = Puzzle([[1, 2, 5],
                [3, 4, 0],
                [6, 7, 8]], action="Initial")

board1 = Puzzle([[1, 4, 2],
                 [6, 5, 8],
                 [7, 3, 0]], action="Initial")

board2 = Puzzle([[1, 0, 2],
                 [7, 5, 4],
                 [8, 6, 3]], action="Initial")

board3 = Puzzle([[3, 1, 2],
                 [6, 4, 5],
                 [0, 7, 8]], action="Initial")

# if board.is_solvable():
board3.dfs()
# else:
# print("Not Solvable Puzzle")
