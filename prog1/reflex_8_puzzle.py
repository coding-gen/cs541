#!/usr/bin/env python

# Programming assignment 1
# 8 square puzzle (2-D rubix)

import argparse
from random import randint
from math import floor
import copy


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


def h_n(state):
    # heuristic: sum for each tile: count of moves away from its goal position.
    h_cost = 0
    for position in range(len(state)):
        moves = 0
        distance = abs(state[position] - (position))
        moves += distance % 3 # x moves
        moves += floor(distance / 3) # y moves
        h_cost += moves
    # One move swaps 2 tiles, so divide the estimate by 2.
    return h_cost / 2

def swap(env, original_position, new_position):

    # Move the value of the tile into the original blank location.
    env.state[original_position] = env.state[new_position]

    # Move the blank into the new position. 
    # Its value is always 8 so we don't need a tmp.
    env.state[new_position] = 8


def move_blank(env, direction):
    # If we're already at a wall, stay there.

    original_position = env.blank.location
    if direction == 'U':
        if env.blank.location not in [0, 1, 2]:
            env.blank.location -= 3
    elif direction == 'D':
        if env.blank.location not in [6, 7, 8]:
            env.blank.location += 3
    elif direction == 'L':
        if env.blank.location not in [0, 3, 6]:
            env.blank.location -= 1
    elif direction == 'R':
        if env.blank.location not in [2, 5, 8]:
            env.blank.location += 1
    new_position = env.blank.location

    swap(env, original_position, new_position)


class blank():
    def __init__(self, location):
        self.location = location


class Environment():
    def __init__(self, width, height, start_state):
        self.size = width * height
        self.width = width
        self.height = height

        intermediate_state = start_state.split(' ')
        for position in range(len(intermediate_state)):
            if intermediate_state[position] == 'b':
                intermediate_state[position] = 8
                print(f'setting blank location to: {position}')
                self.blank = blank(position)

            else: 
                intermediate_state[position] = int(intermediate_state[position]) - 1
        self.state = intermediate_state


def next_move(env):
    actions = []

    check_env = copy.deepcopy(env)
    move_blank(check_env, 'U')
    actions.append((h_n(check_env.state), 'U'))

    check_env = copy.deepcopy(env)
    move_blank(check_env, 'D')
    actions.append((h_n(check_env.state), 'D'))

    check_env = copy.deepcopy(env)
    move_blank(check_env, 'L')
    actions.append((h_n(check_env.state), 'L'))

    check_env = copy.deepcopy(env)
    move_blank(check_env, 'R')
    actions.append((h_n(check_env.state), 'R'))

    actions.sort(reverse = True)
    return actions.pop()


def print_state(state):
    print_str = ''
    for tile in state:
        if tile == 8:
            print_str = print_str + ' b'
        else:
            print_str = print_str + ' ' + str(tile+1)
    return print_str


def main():
    args = parse_args()
    width = int(args.width)
    height = int(args.height)
    start_state = args.start_state
    heuristic = args.heuristic
    verbose = args.verbose
    env = Environment(width, height, start_state)

    state_moves = [env.state]
    moves = 0
    goal_reached = False
    path = print_state(env.state)
    while not goal_reached and moves < 20:
        print(f'state is: {print_state(env.state)}')
        print(f'blank location is: {env.blank.location}')

        if h_n(env.state) == 0:
            print(f'Goal state reached. \nCost: {moves}.\nMoves: {path}')
            goal_reached = True
        else:
            move = next_move(env)
            print(f'h(current_state) = {h_n(env.state)}')
            print(f'Next move is: {move[1]} and its h is: {move[0]}')
            move_blank(env, move[1])
            moves += 1
            path = ' -> '.join((path, print_state(env.state)))


if __name__ == '__main__':
    main()
