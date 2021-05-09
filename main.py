from copy import deepcopy
import time
import math


class Puzzle:
    def __init__(self, board_config, action="Initial"):
        self.board_config = board_config
        self.children = []
        self.action = action
        self.parent = []
        self.cost = 0  # g(n)
        self.heuristic = 0  # h(n)
        self.key = 0  # f(n) = g(n) + h(n)

        for i in range(3):
            for j in range(3):
                if self.board_config[i][j] == 0:
                    self.blank_row = i
                    self.blank_col = j
                    break

    def up(self):
        if self.blank_row == 0:
            return None
        else:
            new_node = Puzzle(deepcopy(self.board_config), action="up")
            new_node.blank_row -= 1
            i = self.blank_row
            j = self.blank_col
            new_node.board_config[i - 1][j], new_node.board_config[i][j] = new_node.board_config[i][j], \
                                                                           new_node.board_config[i - 1][j]
            return new_node

    def down(self):
        if self.blank_row == 2:
            return None
        else:
            new_node = Puzzle(deepcopy(self.board_config), action="down")
            new_node.blank_row += 1
            i = self.blank_row
            j = self.blank_col
            new_node.board_config[i + 1][j], new_node.board_config[i][j] = new_node.board_config[i][j], \
                                                                           new_node.board_config[i + 1][j]
            return new_node

    def left(self):
        if self.blank_col == 0:
            return None
        else:
            new_node = Puzzle(deepcopy(self.board_config), action="left")
            new_node.blank_col -= 1
            i = self.blank_row
            j = self.blank_col
            new_node.board_config[i][j - 1], new_node.board_config[i][j] = new_node.board_config[i][j], \
                                                                           new_node.board_config[i][j - 1]
            return new_node

    def right(self):
        if self.blank_col == 2:
            return None
        else:
            new_node = Puzzle(deepcopy(self.board_config), action="right")
            new_node.blank_col += 1
            i = self.blank_row
            j = self.blank_col
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
                cost = node.cost
                running_time = time.time() - start_time
                while node.action != "Initial":
                    path.append(node.action)
                    node = node.parent
                print("Path to Goal :", path[::-1])
                print("Cost of Path : ", cost)
                print("Nodes Expanded : ", explored_nodes)
                print("Search Depth : ", len(path))
                print("Running Time : ", running_time)
                break

            for child in node.expand():
                if child.board_config not in frontier_boards and child.board_config not in explored:
                    child.parent = node
                    child.cost = child.parent.cost + 1
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
                cost = node.cost
                running_time = time.time() - start_time
                while node.action != "Initial":
                    path.append(node.action)
                    node = node.parent
                print("Path to Goal :", path[::-1])
                print("Cost of Path : ", cost)
                print("Nodes Expanded : ", explored_nodes)
                print("Search Depth : ", len(path))
                print("Running Time : ", running_time)
                break

            for child in node.expand():
                if child.board_config not in frontier_boards and child.board_config not in explored:
                    child.parent = node
                    child.cost = child.parent.cost + 1
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

    def manhattan(self):

        for i in range(1, 4):
            for j in range(1, 4):
                x_goal = (goal[i][j] // 3) + 1
                y_goal = (goal[i][j] % 3) + 1
                self.heuristic += abs(i - x_goal) + abs(j - y_goal)

        key = self.cost + self.heuristic
        return key

    def h_manhattan_dist(self):
        manh_dist = []
        manhattan_dist = 0
        for i in range(0, 3):
            for j in range(0, 3):
                manh_dist.append(goal[i][j])

        for i in range(0, 3):
            for j in range(0, 3):
                current_coor = self.board_config[i][j]
                x_coor = i
                y_coor = j
                index = manh_dist.index(current_coor)
                x_goal, y_goal = index // 3, index % 3
                if current_coor != 0:
                    manhattan_dist += (math.fabs(x_goal - x_coor) + math.fabs(y_goal - y_coor))

        return manhattan_dist

    def euclidean(self):
        self.heuristic = math.sqrt(pow(self.blank_row - 1, 2) + pow(self.blank_col - 1, 2))
        key = self.cost + self.heuristic
        return key

    def astar_manhattan(self):
        node = Puzzle(deepcopy(self.board_config), action="Initial")
        frontier = [node]
        frontier_boards = [node.board_config]
        explored = []
        path = []
        explored_nodes = 0
        start_time = time.time()

        while len(frontier) != 0:
            # sorted list
            node.key = node.h_manhattan_dist()
            frontier.sort(key=lambda node: node.key)
            node = frontier.pop(0)
            frontier_boards.remove(node.board_config)
            explored.append(node)
            explored_nodes += 1

            if node.is_goal():
                running_time = time.time() - start_time
                cost = node.cost
                while node.action != "Initial":
                    path.append(node.action)
                    node = node.parent
                print("Path to Goal :", path[::-1])
                print("Cost of Path : ", cost)
                print("Nodes Expanded : ", explored_nodes)
                print("Search Depth : ", len(path))
                print("Running Time : ", running_time)
                break

            for child in node.expand():
                if child.board_config not in frontier_boards and child.board_config not in explored:
                    child.parent = node
                    child.cost = child.parent.cost + 1
                    frontier.append(child)
                    frontier_boards.append(child.board_config)


goal = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]

board = Puzzle([[1, 2, 5],
                [3, 4, 0],
                [6, 7, 8]], action="Initial")

board1 = Puzzle([[1, 4, 2],
                 [6, 5, 8],
                 [7, 3, 0]], action="Initial")

board2 = Puzzle([[4, 3, 2],
                 [6, 5, 0],
                 [7, 8, 1]], action="Initial")

board3 = Puzzle([[1, 0, 2],
                 [7, 5, 4],
                 [8, 6, 3]], action="Initial")

# if board.is_solvable():
board3.astar_manhattan()
# else:
#   print("Not Solvable Puzzle")
