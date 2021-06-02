#!/usr/bin/env python

# Programming assignment 3
# PSU CS541 Spring Semester 2021
# 2 June 2021
# Robby the Reinforcement Learning Robot
# Author: Genevieve LaLonde

import argparse
from random import randint
from math import floor, ceil, log
from statistics import stdev, variance, mean
from copy import copy

global env

def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
             description="Specify parameters for the 8 queens problem and genetic algorithm.")
    parser.add_argument(
        '-x', '--width',
        dest='width',
        default=10,
        help="How many squares on the x axis.") 
    parser.add_argument(
        '-y', '--height',
        dest='height',
        default=10,
        help="How many squares on the y axis.")
    parser.add_argument(
        '-s', '--step-size',
        dest='step',
        default='5',
        help="The step size, gamma.")
    parser.add_argument(
        '-c', '--can-count',
        dest='cans',
        default='20',
        help="The count of cans to strew around the room.")
    parser.add_argument(
        '-v', '--verbose',
        dest='verbose',
        default=False,
        action="store_true",
        help="Print verbose lines for debugging.")
    args = parser.parse_args()
    return args

def logger(f, rob):
    # Print robby info: location, current reward, maybe percepts
    # Print board info: graphical representation of spaces, cans, and robbie
    # separate with tabs to ensure equal spacing, or set eequal char width setting.

    robby_state = ''
    board_state = ''
    content = ''
    content += f"Robbie's position: {rob.x}, {rob.y}\n"
    content += f"Robbie's reward: {rob.reward}\n"

    content += '   0  1  2  3  4  5  6  7  8  9\n'
    for y in range(len(env.board[0])):
        content += f'{y}: '
        for x in range(len(env.board)-1):
            content += f'{env.board[x][y]}, '
        content += f'{env.board[len(env.board)-1][y]}'
        content += '\n'
    content += '\n'
    """
    for i in range(len(env.board)):
       content += f'{i} {env.board[i]}\n'
       """
    f.write(content)
    return 


def value(board):
    # back propagate

    """
    # Iterate the board
    # For each queen, count how many it is attacking.
    # Or store this as a value on each board, to avoid recomputing.
    # Considering space vs compute. Space is typically the limit.
    # Individuals only live one generation. Recalculation per individual is minimal. 
    # Recalculate to save space, and since it wouldn't be a big benefit. And to make the individual less complex.

    attacking = 0
    for i in range(len(board)):
        # go down the list and see if attack with another queen.
        for j in range(len(board)):
            # Queen in same column not possible due to env creation.
            # Check for queen in same row
            if i == j:
                continue
            if board[i] == board[j]:
                attacking += 1
            # Check whether the x and y coordinates of Q' are the same distance from Q.
            if abs(i - j) == abs(board[i] - board[j]):
                attacking += 1
    return attacking
    """
    pass


class Q_Table():
    def __init__(self):
        table = dict()


class Robbie():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reward = 0

    def sense(self):
        #global env
        # Your percepts are your state
        # Current, N, S, W, E
        # Values: empty = 0 , can = 1 , wall = -1
        percepts = [0, 0, 0, 0, 0]
        if env.board[self.x][self.y] == 1:
            percepts[0] = 1

        # North
        if self.y == 0:
            percepts[1] = -1
        elif env.board[self.x][self.y - 1] == 1:
            percepts[1] = 1

        # South
        if self.y == 9:
            percepts[2] = -1
        elif env.board[self.x][self.y + 1] == 1:
            percepts[2] = 1

        # West
        if self.x == 0:
            percepts[3] = -1
        elif env.board[self.x - 1][self.y] == 1:
            percepts[3] = 1

        # East
        if self.x == 9:
            percepts[4] = -1
        elif env.board[self.x + 1][self.y] == 1:
            percepts[4] = 1
        return percepts

    def take_action(self, action):
        # Move up, down, left, or right
        # If it's a wall lose reward -5.

        # Up
        if action == 0:
            if self.y == 0:
                self.reward -= 5
            else:
                self.y -= 1

        # Down
        if action == 1:
            if self.y == 9:
                self.reward -= 5
            else:
                self.y += 1

        # Left
        if action == 2:
            if self.x == 0:
                self.reward -= 5
            else:
                self.x -= 1

        # Right
        if action == 3:
            if self.x == 9:
                self.reward -= 5
            else:
                self.x += 1

        # Pick Up
        if action == 4:
            if env.board[self.x][self.y] == 1:
                env.board[self.x][self.y] = 0
                self.reward += 10
            else:
                self.reward += -1

        return


class Environment():
    def __init__(self, width, height, cans):
        # board size
        self.size = width * height
        self.width = width
        self.height = height
        # a list of lists
        self.board = []
        y = []
        for j in range(height):
            y.append(0)
            
        for i in range(width):
            self.board.append(copy(y))

        # Fill cans in random spots
        for i in range(cans):
            x = randint(0,9)
            y = randint(0,9)
            if self.board[x][y] == 0:
                self.board[x][y] = 1
            else:
                i -= 1


def main():
    global env
    args = parse_args()
    cans = int(args.cans)
    width = int(args.width)
    height = int(args.height)
    step = int(args.step)
    verbose = args.verbose
    f = open('robby.log', 'w')
    f.write('')

    # get setup
    env = Environment(width,height,cans)
    # Place Robby
    x = randint(0,9)
    y = randint(0,9)
    rob = Robbie(x,y)

    logger(f, rob)

    print(f'start x:{rob.x}, y:{rob.y}, r:{rob.reward} p:{rob.sense()}')
    rob.take_action(0)
    print(f'up x:{rob.x}, y:{rob.y}, r:{rob.reward} p:{rob.sense()}')
    rob.take_action(1)
    print(f'down x:{rob.x}, y:{rob.y}, r:{rob.reward} p:{rob.sense()}')
    rob.take_action(2)
    print(f'left x:{rob.x}, y:{rob.y}, r:{rob.reward} p:{rob.sense()}')
    rob.take_action(3)
    print(f'right x:{rob.x}, y:{rob.y}, r:{rob.reward} p:{rob.sense()}')
    rob.take_action(4)
    print(f'pickup x:{rob.x}, y:{rob.y}, r:{rob.reward} p:{rob.sense()}')


    # anytime to log
    f = open('robby.log', 'a')
    logger(f, rob)
    f.close()

if __name__ == '__main__':
    main()

