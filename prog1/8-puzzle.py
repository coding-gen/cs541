#!/usr/bin/env python

# Programming assignment 1
# 8 square puzzle (2-D rubix)

import argparse
from random import randint
from math import floor

global env

def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
             description="Specify the puzzle and heuristic.")
    parser.add_argument(
        '-a', '--heuristic-algorithm',
        dest='heuristic',
        default='h',
        help="Type of heurisitic algorithm to use: ")
    parser.add_argument(
        '-s', '--start-state',
        dest='start_state',
        default='4 5 b 6 1 8 7 3 2',
        help="What is the starting state of the puzzle?") 
    parser.add_argument(
        '-v', '--verbose',
        dest='verbose',
        default=False,
        action="store_true",
        help="Print verbose lines for debugging.")
    parser.add_argument(
        '-x', '--width',
        dest='width',
        default=3,
        help="How many squares on the x axis.") 
    parser.add_argument(
        '-y', '--height',
        dest='height',
        default=3,
        help="How many squares on the y axis.")
    args = parser.parse_args()
    return args



class blank():
    def __init__(self, location):
        self.location = location


def h_n(state):
    # heuristic: sum for each tile: count of moves away from its goal position.
    h_cost = 0
    for position in range(len(state)):
        moves = 0
        distance = abs(state[position] - (position + 1))
        moves += distance % 3 # x moves
        moves += floor(distance / 3) # y moves
        h_cost += moves
    return h_cost


class Environment():
    def __init__(self, width, height, start_state):
        self.size = width * height
        self.width = width
        self.height = height

        intermediate_state = start_state.split(' ')
        for position in range(len(intermediate_state)):
            if intermediate_state[position] == 'b':
                intermediate_state[position] = 9
                self.blank = blank(position)
            else: 
                intermediate_state[position] = int(intermediate_state[position])
        self.state = intermediate_state

    def swap(self, blank_original_position):
        # self.blank.location is already set for the blank's new position.

        # Move the value of the tile into the original blank location.
        self.state[blank_original_position] = self.state[self.blank.location]

        # Move the blank into the new position. 
        # Its value is always 9 so we don't need a tmp.
        self.state[self.blank.location] = 9


    def move_blank(self, direction):
        # If we're already at a wall, stay there.

        original_position = self.blank.location
        if direction == 'U':
            if self.blank.location not in [0, 1, 2]:
                self.blank.location -= 3
        elif direction == 'D':
            if self.blank.location not in [6, 7, 8]:
                self.blank.location += 3
        elif direction == 'L':
            if self.blank.location not in [0, 3, 6]:
                self.blank.location -= 1
        elif direction == 'R':
            if self.blank.location not in [2, 5, 8]:
                self.blank.location += 1

        env.swap(original_position)


def next_move(env):
    actions = []
    check_env = env
    check_env.move_blank('U')
    actions.append((h_n(check_env.state), 'U'))
    check_env = env
    check_env.move_blank('D')
    actions.append((h_n(check_env.state), 'D'))
    check_env = env
    check_env.move_blank('L')
    actions.append((h_n(check_env.state), 'L'))
    check_env = env
    check_env.move_blank('R')
    actions.append((h_n(check_env.state), 'R'))
    actions.sort(reverse = True)
    print(f'actions: {actions}')
    return actions.pop()


def main():
    # print(f'{}')
    global env
    args = parse_args()
    width = int(args.width)
    height = int(args.height)
    start_state = args.start_state
    heuristic = args.heuristic
    verbose = args.verbose
    env = Environment(width, height, start_state)

    print(f'start state is: {env.state}')
    state_moves = [env.state]
    total_cost = 0
    goal_reached = False
    moves = 0
    while not goal_reached and moves < 5:
        if h_n(env.state) == 0:
            print(f'goal state reached. \nCost: {total_cost}.\nMoves: {state_moves}')
            goal_reached = True
        else:
            move = next_move(env)
            print(f'h(current_state) = {h_n(env.state)}')
            print(f'Next move is: {move[1]} and its h is: {move[0]}')
            moves += 1



if __name__ == '__main__':
    main()
