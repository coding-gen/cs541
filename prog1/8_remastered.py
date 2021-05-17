#!/usr/bin/env python

# Programming assignment 1
# 8 square puzzle (2-D rubix)

import argparse
from random import randint
from math import floor
import copy
import tinytree


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
    # heuristic: manhattan distance 
    h_cost = 0
    for position in range(len(state)):
        # Don't treat the blank space as a tile.
        # This enables it to be used more effectively to move tiles.
        # It also makes h(n) admissible.
        if state[position] == 8:
            continue
        moves = 0
        distance = abs(state[position] - position)
        moves += distance % 3 # x moves
        moves += floor(distance / 3) # y moves
        h_cost += moves
    return 


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
        # This is for if I do the extra credit
        self.size = width * height
        self.width = width
        self.height = height

        intermediate_state = start_state.split(' ')
        for position in range(len(intermediate_state)):
            if intermediate_state[position] == 'b':
                intermediate_state[position] = 8
                self.blank = blank(position)

            else: 
                intermediate_state[position] = int(intermediate_state[position]) - 1
        self.state = intermediate_state


def solveable(state):
    # Todo: remove b from list
    inversions = 0
    for position in range(len(state)):
        if state[position] != 8:
            inversions += abs(state[position] - position)
    print(f'inversions count = {inversions/2}')
    if (inversions/2) % 2 == 0:
        return True
    return False


def print_state(state):
    print_str = ''
    for tile in state:
        if tile == 8:
            print_str = print_str + ' b'
        else:
            print_str = print_str + ' ' + str(tile+1)
    return print_str


def next_move(env, path):
    """
    state_moves = [env.state]
    print(f'starting move sequence, path is: {path}')

    if h_n(env.state) == 0:
        return True, path
    elif len(path) >= 30:
        return False, path
    else:
        actions = []
        check_env = copy.deepcopy(env)
        move_blank(check_env, 'U')
        actions.append((len(path) + 1 + h_n(check_env.state), 'U'))

        check_env = copy.deepcopy(env)
        move_blank(check_env, 'D')
        actions.append((len(path) + 1 + h_n(check_env.state), 'D'))

        check_env = copy.deepcopy(env)
        move_blank(check_env, 'L')
        actions.append((len(path) + 1 + h_n(check_env.state), 'L'))

        check_env = copy.deepcopy(env)
        move_blank(check_env, 'R')
        actions.append((len(path) + 1 + h_n(check_env.state), 'R'))

        actions.sort(reverse = True)
        # Recursively do all actions, 
        # Starting with the one that has the best heuristic.
        # Heuristic needs to include the depth of the path up to here, a running tally.
        for i in range(len(actions)):
            action = actions.pop()
            # this should probably get its own env...
            move_blank(env,action[1])
            print(f'adding state to path: {env.state}')
            path.append(env.state)
            print(f'added: {path}')
            next_move(env, path)

        #path = ' -> '.join((path, print_state(env.state)))
        return False, path
    """
    return True, path

def main():
    args = parse_args()
    width = int(args.width)
    height = int(args.height)
    start_state = args.start_state
    heuristic = args.heuristic
    verbose = args.verbose
    env = Environment(width, height, start_state)

    assert(len(start_state.split(' ')) == 9), \
        'The start state should have 9 tiles separated by whitespace.'

    assert solveable(env.state), \
        'This puzzle has an odd number of inversions ' + \
        'and is therefore not solveable.'

    state_moves = [env.state]
    moves = 0
    goal_reached = False
    path = [env.state]
    print(f'path is: {path}')
    # path = print_state(env.state)

    while not goal_reached and moves < 2:
        print(f'starting state is: {print_state(env.state)}')

        if h_n(env.state) == 0:
            goal_reached = True
        else:
            goal_reached, path = next_move(env, path)
            #print(f'h(current_state) = {h_n(env.state)}')
            #print(f'Next move is: {move[1]} and its h is: {move[0]}')
            #move_blank(env, move[1])
            #moves += 1
    print(f'Goal state reached: {goal_reached}')
    print(f'Cost: {len(path)-1}.')
    history = ''
    for i in range(len(path) - 2):
        history + print_state(path[i]) + ' -> ' 
    history + print_state(path[len(path)-1])
    print(f'Moves: {history}')



if __name__ == '__main__':
    main()
