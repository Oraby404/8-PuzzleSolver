import sys
from copy import deepcopy
import time
import math
import numpy


class Puzzle:
    def __init__(self, board_config, action="Initial"):
        # current board configuration
        self.board_config = board_config
        # nodes expanded by current node
        self.children = []
        # action taken to bring current node (up, down, left, right)
        self.action = action
        # the parent node of the current node
        self.parent = []
        # cumulative cost to reach current node
        self.cost = 0  # g(n)
        # value of the heuristic function for current node
        self.heuristic = 0  # h(n)
        # key is the sum of cumulative cost and  heuristic function for current node
        self.key = 0  # f(n) = g(n) + h(n)

        # calculate the x and y coordinates of the blank tile
        for i in range(3):
            for j in range(3):
                if self.board_config[i][j] == 0:
                    # x coordinates
                    self.blank_row = i
                    # y coordinates
                    self.blank_col = j
                    break

    # function up to replace the blank tile with the tile above it
    def up(self):
        # check if limit is not reached
        if self.blank_row == 0:
            return None
        else:
            # create a new node with the same configuration and action up
            new_node = Puzzle(deepcopy(self.board_config), action="up")
            # new coordinates of the blank tile
            new_node.blank_row -= 1
            i = self.blank_row
            j = self.blank_col
            # swap the blank tile with the one above it
            new_node.board_config[i - 1][j], new_node.board_config[i][j] = new_node.board_config[i][j], \
                                                                           new_node.board_config[i - 1][j]
            return new_node

    # function down to replace the blank tile with the tile below it
    def down(self):
        # check if limit is not reached
        if self.blank_row == 2:
            return None
        else:
            # create a new node with the same configuration and action down
            new_node = Puzzle(deepcopy(self.board_config), action="down")
            # new coordinates of the blank tile
            new_node.blank_row += 1
            i = self.blank_row
            j = self.blank_col
            # swap the blank tile with the one below it
            new_node.board_config[i + 1][j], new_node.board_config[i][j] = new_node.board_config[i][j], \
                                                                           new_node.board_config[i + 1][j]
            return new_node

    # function left to replace the blank tile with the tile on its left
    def left(self):
        # check if limit is not reached
        if self.blank_col == 0:
            return None
        else:
            # create a new node with the same configuration and action left
            new_node = Puzzle(deepcopy(self.board_config), action="left")
            # new coordinates of the blank tile
            new_node.blank_col -= 1
            i = self.blank_row
            j = self.blank_col
            # swap the blank tile with the one on its left
            new_node.board_config[i][j - 1], new_node.board_config[i][j] = new_node.board_config[i][j], \
                                                                           new_node.board_config[i][j - 1]
            return new_node

    # function right to replace the blank tile with the tile on its right
    def right(self):
        # check if limit is not reached
        if self.blank_col == 2:
            return None
        else:
            # create a new node with the same configuration and action right
            new_node = Puzzle(deepcopy(self.board_config), action="right")
            # new coordinates of the blank tile
            new_node.blank_col += 1
            i = self.blank_row
            j = self.blank_col
            # swap the blank tile with the one on its right
            new_node.board_config[i][j + 1], new_node.board_config[i][j] = new_node.board_config[i][j], \
                                                                           new_node.board_config[i][j + 1]
            return new_node

    # function expand creates all possible children nodes give any node
    def expand(self):
        # make sure the children list is empty
        if len(self.children) == 0:
            # save the action that brought the current node to avoid adding
            # its reverse action in the children nodes
            last_action = self.action

            # get the child generated from moving blank tile up
            up_child = self.up()
            if up_child is not None and last_action != "down":
                self.children.append(up_child)

            # get the child generated from moving blank tile down
            down_child = self.down()
            if down_child is not None and last_action != "up":
                self.children.append(down_child)

            # get the child generated from moving blank tile right
            left_child = self.left()
            if left_child is not None and last_action != "right":
                self.children.append(left_child)

            # get the child generated from moving blank tile left
            right_child = self.right()
            if right_child is not None and last_action != "left":
                self.children.append(right_child)

        # return a list of children generated , all of type "Puzzle"
        return self.children

    # Breadth-First Search Algorithm
    def bfs(self):
        # check if the current board configuration is solvable
        if self.is_solvable():
            # enqueue the starting node in the frontier queue
            frontier = [self]
            # frontier boards are the the boards of the nodes that are already in the frontier queue
            # this list is needed for comparison since we can't compare objects directly
            frontier_boards = [self.board_config]
            # list of explored board configurations to avoid repetition and infinite loops
            explored = []
            # max search depth the tree reached
            max_search_depth = 0
            # number of explored node , the ones in the frontier are not included
            explored_nodes = 0
            # start time of the search
            start_time = time.time()

            # loop until the frontier queue is empty
            while len(frontier) != 0:
                # dequeue node from the queue
                self = frontier.pop(0)
                # also from the frontier boards list
                frontier_boards.pop(0)
                # add the node to the explored list
                explored.append(self.board_config)
                # increment the explored node by 1
                explored_nodes += 1

                # check if the current node is the goal configuration
                if self.is_goal():
                    # if yes display the search analysis and return 1
                    self.display(start_time, explored_nodes, max_search_depth)
                    return 1

                # if the node is not the goal , expand the node to get all possible children
                for child in self.expand():
                    # check if the child board is in the frontier and explored lists or not
                    if child.board_config not in frontier_boards and child.board_config not in explored:
                        # set the child node's parent
                        child.parent = self
                        # set the cost to reach this node
                        child.cost = child.parent.cost + 1
                        # enqueue the child in the frontier list and frontier boards
                        frontier.append(child)
                        frontier_boards.append(child.board_config)
                        # check for the max search depth
                        if child.cost > max_search_depth:
                            max_search_depth = child.cost
            print("Couldn't Solve Puzzle")
            return 0
        print("Not Solvable Puzzle")

    # Depth-First Search Algorithm
    def dfs(self, depth):
        # check if the current board configuration is solvable
        if self.is_solvable():
            # push the starting node in the frontier stack
            frontier = [self]
            # frontier boards are the the boards of the nodes that are already in the frontier stack
            # this list is needed for comparison since we can't compare objects directly
            frontier_boards = [self.board_config]
            # list of explored board configurations to avoid repetition and infinite loops
            explored = []
            # max search depth the tree reached
            max_search_depth = 0
            # number of explored node , the ones in the frontier are not included
            explored_nodes = 0
            # start time of the search
            start_time = time.time()

            # loop until the frontier stack is empty
            while len(frontier) != 0:
                # pop node from the stack
                self = frontier.pop()
                # also from the frontier boards list
                frontier_boards.pop()
                # add the node to the explored list
                explored.append(self.board_config)
                # increment the explored node by 1
                explored_nodes += 1

                # check if the current node is the goal configuration
                if self.is_goal():
                    # if yes display the search analysis and return 1
                    self.display(start_time, explored_nodes, max_search_depth)
                    return 1

                # if the node is not the goal , expand the node to get all possible children
                for child in self.expand():
                    # check if the child board is in the frontier and explored lists or not
                    if child.board_config not in frontier_boards and child.board_config not in explored:
                        # set the child node's parent
                        child.parent = self
                        # set the cost to reach this node
                        child.cost = child.parent.cost + 1

                        # check if the max depth is reached
                        if child.cost <= depth:
                            # push the child in the frontier list and frontier boards
                            frontier.append(child)
                            frontier_boards.append(child.board_config)
                            # check for the max search depth
                            if child.cost > max_search_depth:
                                max_search_depth = child.cost
            return 0
        print("Not Solvable Puzzle")

    # Iterative-Deepening Search
    def ids(self):
        # check if the current board configuration is solvable
        if self.is_solvable():
            # start with depth = 0 to depth = sys.maxsize
            for depth in range(sys.maxsize):
                # DLS with limit = depth
                if self.dfs(depth):
                    return 1
        print("Not Solvable Puzzle")

    # A* Search
    # argument : heuristic function
    def a_star(self, h_function):
        # check if the current board configuration is solvable
        if self.is_solvable():
            # insert the starting node in the frontier list
            frontier = [self]
            # frontier boards are the the boards of the nodes that are already in the frontier stack
            # this list is needed for comparison since we can't compare objects directly
            frontier_boards = [self.board_config]
            # list of explored board configurations to avoid repetition and infinite loops
            explored = []
            # max search depth the tree reached
            max_search_depth = 0
            # number of explored node , the ones in the frontier are not included
            explored_nodes = 0
            # start time of the search
            start_time = time.time()

            # loop until the frontier list is empty
            while len(frontier) != 0:
                # sort the frontier list with key to form the frontier heap
                frontier.sort(key=lambda node: node.key)
                # dequeue node from the heap
                self = frontier.pop(0)
                # also from the frontier boards list
                frontier_boards.remove(self.board_config)
                # add the node to the explored list
                explored.append(self.board_config)
                # increment the explored node by 1
                explored_nodes += 1

                # check if the current node is the goal configuration
                if self.is_goal():
                    # if yes display the search analysis and return 1
                    self.display(start_time, explored_nodes, max_search_depth)
                    return 1

                # if the node is not the goal , expand the node to get all possible children
                for child in self.expand():
                    # set the child node's parent
                    child.parent = self
                    # set the cost to reach this node
                    child.cost = child.parent.cost + 1
                    # calculate the heuristic function for this node
                    if h_function == "euclidean":
                        child.euclidean()
                    else:
                        child.manhattan()

                    # check if the child board is in the frontier and explored lists or not
                    if child.board_config not in frontier_boards and child.board_config not in explored:
                        # enqueue the child in the frontier list and frontier boards
                        frontier.append(child)
                        frontier_boards.append(child.board_config)
                        # check for the max search depth
                        if child.cost > max_search_depth:
                            max_search_depth = child.cost

                    # if the board is in the frontier list , check for possible decrease key
                    elif child.board_config in frontier_boards:
                        # get the index of the node in frontier list
                        for i in range(0, len(frontier)):
                            if child.board_config == frontier[i].board_config:
                                break
                        # if the node key is less than the one in the frontier list,
                        # decrease key
                        if child.key < frontier[i].key:
                            frontier[i] = child
                            # check for the max search depth
                            if child.cost > max_search_depth:
                                max_search_depth = child.cost
            print("Couldn't Solve Puzzle")
            return 0
        print("Not Solvable Puzzle")

    # Manhattan heuristic function
    # calculates the sum of the distances (sum of the vertical and horizontal distances)
    # from the blocks to their goal position in addition to the cumulative cost
    def manhattan(self):
        for i in range(0, 3):
            for j in range(0, 3):
                # check if the tile is not the blank tile
                if self.board_config[i][j] != 0:
                    # calculate the x coordinates of the given tile in the goal configuration
                    x_goal = (self.board_config[i][j] // 3)
                    # calculate the x coordinates of the given tile in the goal configuration
                    y_goal = (self.board_config[i][j] % 3)
                    # calculate the heuristic for each tile and sum them
                    self.heuristic += (abs(i - x_goal) + abs(j - y_goal))
        # key equals to the heuristic value plus the cumulative cost
        self.key = self.cost + self.heuristic

    # Euclidean heuristic function
    # calculates the length of the hypotenuse between 2 points
    def euclidean(self):
        for i in range(0, 3):
            for j in range(0, 3):
                # check if the tile is not the blank tile
                if self.board_config[i][j] != 0:
                    # calculate the x coordinates of the given tile in the goal configuration
                    x_goal = (self.board_config[i][j] // 3)
                    # calculate the x coordinates of the given tile in the goal configuration
                    y_goal = (self.board_config[i][j] % 3)
                    # calculate the heuristic for each tile and sum them
                    self.heuristic += math.sqrt(pow(i - x_goal, 2) + pow(j - y_goal, 2))
        # key equals to the heuristic value plus the cumulative cost
        self.key = self.cost + self.heuristic

    # checks if the current configuration is solvable
    def is_solvable(self):
        # convert the 2-D array of the configuration to 1-D array
        state = numpy.array(self.board_config).flatten()
        # an inversion happens if a number has a number with smaller value on its right
        # exept for the blank tile
        inv_count = 0
        for i in range(9):
            for j in range(i + 1, 9):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inv_count += 1
        # not solvable if odd count
        return inv_count % 2 == 0

    # checks if the current configuration is the goal configuration
    def is_goal(self):
        return self.board_config == goal

    # display the solution analysis
    def display(self, start_time, explored_nodes, max_search_depth):
        # end the search time
        running_time = time.time() - start_time
        path = []
        cost = self.cost
        # roll back to the starting node to get the path
        while self.action != "Initial":
            path.append(self.action)
            self = self.parent

        print("Path to Goal :", path[::-1])
        print("Cost of Path : ", cost)
        print("Nodes Expanded : ", explored_nodes)
        print("Search Depth : ", len(path))
        print("Max Search Depth : ", max_search_depth)
        print("Running Time : ", running_time)


goal = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]]

board = Puzzle([[1, 2, 5],
                [3, 0, 4],
                [6, 7, 8]], action="Initial")

board1 = Puzzle([[1, 4, 2],
                 [6, 5, 8],
                 [7, 3, 0]], action="Initial")

board2 = Puzzle([[1, 0, 2],
                 [7, 5, 4],
                 [8, 6, 3]], action="Initial")

board3 = Puzzle([[4, 1, 3],
                 [0, 2, 6],
                 [7, 5, 8]], action="Initial")

board4 = Puzzle([[4, 3, 2],
                 [6, 5, 0],
                 [7, 8, 1]], action="Initial")

print("Using BFS Search\n")
board1.bfs()
print("     ****\nUsing DLS Search\n")
board1.dfs(12)
print("     ****\nUsing IDS Search\n")
board1.ids()
print("     ****\nUsing A* Search with Manhattan heuristic\n")
board1.a_star("manhattan")
print("     ****\nUsing A* Search with Euclidean heuristic\n")
board1.a_star("euclidean")
