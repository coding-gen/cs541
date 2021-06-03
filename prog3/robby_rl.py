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
        '-r', '--random-epsilon',
        dest='epsilon',
        default='0.1',
        help="Percent probability of randomness, starting value.")
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
    parser.add_argument(
        '-e', '--episodes',
        dest='episodes',
        default=2,
        help="Number of learning episodes Robby gets.")
    parser.add_argument(
        '-t', '--trials',
        dest='trials',
        default=2,
        help="Number of trials/actions in each episode.")
    args = parser.parse_args()
    return args

def logger(f, rob, action = -1):
    # Print robby info: location, current reward, maybe percepts
    # Print board info: graphical representation of spaces, cans, and robbie
    # separate with tabs to ensure equal spacing, or set eequal char width setting.

    robby_state = ''
    board_state = ''
    content = ''
    content += f"Robbie's position: {rob.x}, {rob.y}\n"
    content += f"Robbie's reward: {rob.reward}\n"
    if action >= 0:
        if action == 0: 
            action = 'Up'
        elif action == 1:
            action = 'Down'
        elif action == 2:
            action = 'Left'
        elif action == 3:
            action = 'Right'
        elif action == 4:
            action = 'Pick Up'
        content += f"Action Robbie took: {action}.\n"

    content += '   0  1  2  3  4  5  6  7  8  9\n'
    for y in range(len(env.board[0])):
        content += f'{y}: '
        for x in range(len(env.board)-1):
            content += f'{env.board[x][y]}, '
        content += f'{env.board[len(env.board)-1][y]}'
        content += '\n'
    content += '\n'

    f.write(content)
    return 


def value(board):
    # back propagate values

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


class Q_table():
    def __init__(self):
        self.table = dict()
        # key: (state, last 3 actions), value: dict
            # key: next action, value: reward
        # (percepts 5 with 3 possible values)
        # (previous actions 3 with 5 possible actions)
        # (next actions 1 with 5 possible actions)
        # 1 reward value for each of those above
        """
        percepts = [0, 0, 0, 0, 0]
        for p in range(5):
            percepts.append([-1, 0, 1]) 
        actions = [0, 1, 2, 3, 4]

        # I'll go ahead and init illegal states to 0 for simplicity.
        # For every possible combination of percepts, set the reward of each possible action to 0.
        for percept in range(len(percepts)):
            for p_value in percept:
                for action in actions:
                    self.table[percepts] =  
        """
        pass

    def choose_action(self, percepts, epsilon):
        # If we haven't seen this state yet, init all its actions to reward 0.
        if tuple(percepts) not in self.table: 
            self.table[tuple(percepts)] = [0, 0, 0, 0, 0]
            # EG access reward for action 3 (Left) as t[(0,0,0,0,0)][3]

        # All possible actions
        actions = self.table[tuple(percepts)]
        # Init to all the possible actions
        actions_for_rand = self.table[tuple(percepts)]
        if randint(0,100) > (epsilon * 10):
            max_value = max(actions)

            # If one action has a best reward, use it (hill climb).
            if actions.count(max_value) == 1:
                actions_for_rand = [actions.index(max_value)]

            # Otherwise pick one of the tied max rewards at random
            else:
                actions_for_rand = []
                for i in range(len(actions)):
                    if actions[i] == max_value:
                        actions_for_rand.append(i)
        print (f'possible actions: {actions}')
        print (f'possible rand actions: {actions_for_rand}')

        return randint(0,len(actions_for_rand)-1)




def record(l, x):
    # Remember the last 3 moves.
    if len(l) > 2:
        l.pop(0)
    l.append(x)
    return


class Robbie():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reward = 0
        self.action_sequence = []

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
            record(self.action_sequence, 0)
            if self.y == 0:
                self.reward -= 5
            else:
                self.y -= 1

        # Down
        if action == 1:
            record(self.action_sequence, 1)
            if self.y == 9:
                self.reward -= 5
            else:
                self.y += 1

        # Left
        if action == 2:
            record(self.action_sequence, 2)
            if self.x == 0:
                self.reward -= 5
            else:
                self.x -= 1

        # Right
        if action == 3:
            record(self.action_sequence, 3)
            if self.x == 9:
                self.reward -= 5
            else:
                self.x += 1

        # Pick Up
        if action == 4:
            record(self.action_sequence, 4)
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
        # TODO fix this is meant to be 50/50 chance to have a can
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
    verbose = args.verbose
    episodes = int(args.episodes)
    trials = int(args.trials)
    epsilon = float(args.epsilon)
    f = open('robby.log', 'w')
    f.write('')
    # After coding, defaults should be:
    # episodes: 5000
    # trials/steps/actions: 200
    # n = 0.2
    # g = 0.9
    # For epsilon greedy, e = p(doing non-optimal/greedy/hill-climb action)
    # e=0.1 initially, reduce about every 50 epochs till 0, and stays

    # get setup

    q = Q_table()
    env = Environment(width,height,cans)
    # Place Robby
    x = randint(0,9)
    y = randint(0,9)
    rob = Robbie(x,y)

    logger(f, rob)

    # Learning
    # Trials
    for e in range(episodes):
        # Episodes
        # New distribution of cans
        # New Robbie position
        # Same Q-matrix
        for t in range(trials):
            # Take a random action
            original_reward = copy(rob.reward)
            original_percepts = rob.sense()
            # Read the Q table and choose an action with a high reward with greater probability.
            print(f'action = {q.choose_action(original_percepts, epsilon)}')
            # A small random chance epsilon to still explore some random action instead though.
            # Can start epsilon high and slowly reduce like annealing.
            # Maybe reduce, at a rate slightly faster than the count of episodes.
            # aka once we're about to be done, we want to be making the best choices

            # Just any random action
            # action = randint(0,4)

            # An action from the Q table
            action = q.choose_action(original_percepts, epsilon)

            rob.take_action(action)
            logger(f, rob, action)

            # Update the q table with the state, action, and reward from that action
            # Record the original percepts, reward (as diff of original, new reward), action taken, new percepts
            # Maybe also record the 3 previous actions as part of the state, along with percepts.

            action_reward = rob.reward - original_reward
        # Track the total reward of the episode, make charts on this (1 point per 100 episodes)
        # Avg: sum of rewards per episode, std dev aka test average and test-std-dev

    f.close()

if __name__ == '__main__':
    main()

