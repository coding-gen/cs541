#!/usr/bin/env python

# Programming assignment 2
# PSU CS541 Spring Semester 2021
# 16 May 2021
# 8 Queens Problem
# Using Genetic Algorithm
# Author: Genevieve LaLonde

import argparse
from random import randint
from math import floor, ceil, log
from statistics import stdev, variance, mean

global env

def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
             description="Specify parameters for the 8 queens problem and genetic algorithm.")
    parser.add_argument(
        '-g', '--generations',
        dest='generations',
        default='1',
        help="How many generations to run for.")
    parser.add_argument(
        '-m', '--mutation_probability',
        dest='mutation',
        default='80',
        help="Percent probability of random mutations, eg: 10.")
    parser.add_argument(
        '-p', '--population_size',
        dest='population',
        default='10',
        help="Initial size of the population.")
    parser.add_argument(
        '-s', '--mutation_step',
        dest='step',
        default='5',
        help="How fast to linearly reduce the  mutation.")
    parser.add_argument(
        '-v', '--verbose',
        dest='verbose',
        default=False,
        action="store_true",
        help="Print verbose lines for debugging.")
    args = parser.parse_args()
    return args

def logger(f, generation):
    goal_reached = False
    content = ''
    content += 'generation\tfitness\tboard\n'
    for board in env.herd:
        content += f'{generation}\t{board[0]}\t{board[1]}\n'
        if board[0] == 0:
            goal_reached = True
    f.write(content)
    if goal_reached:
        f.write('Goal Reached.\n')
        return True
    return False

def fitness(board):
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



class Environment():
    def __init__(self, population):
        # One list to hold all individuals in the population.
        self.herd = []

        # Create individuals.
        # Board is always 8X8
        # List of 8 elements
        # For each line, the index is the line number,
        # Its value is the location of the queen.
        # Place one queen at a random location in each list.
        for individual in range(population):
            board = []
            for queen in range(8):
                board.append(randint(0, 7))
            self.herd.append((fitness(board), board))


def myrand(x):
    return randint(0, len(env.herd))


def cull():
    # the greater the greater variance in fitness, the more poor fitness members to die
    # aka trim the tail, more if it's long
    # As generations improve and the variance decreases, less culling should occur automatically.
    fitness_l = []
    for board in env.herd:
        fitness_l.append(board[0])
    if len(fitness_l) > 1: 
        # Variance over 4 is the percent of population we'll rotate
        rotate_count = round(len(env.herd) * variance(fitness_l)/100)
    else:
        rotate_count = 0

    # Replace worst fitness members with the best fitness members.
    env.herd = sorted(env.herd)
    for i in range(rotate_count):
        env.herd[len(env.herd)-(i+1)] = env.herd[i]
    # Shuffle up again before cross breeding.
    # Should we shuffle, or should best breed with best?
    # env.herd = sorted(env.herd, key=myrand)

def assess_split(mother, father):
    # Find the best split point for these parents
    # To produce the fitest children
    fitness_results = []
    for split in range(2, 7):
        mother_fit = fitness(mother[split:] + father[:split]) 
        father_fit = fitness(father[split:] + mother[:split])
        fitness_results.append((mother_fit + father_fit, split))
    return sorted(fitness_results)[0][1]


def cross():
    # We already randomized in cull.
    # So we don't have to worry too much about cross breeding with a sibling.

    # For every other member, split it and the next one at the cross point.
    # swap the crossed members.
    # skip the next one (already crossed)
    for i in range(len(env.herd)-1):
        if i % 2 == 0:
            # Determine for this pair if we should split at 3, 4, or 5.
            cross_point = assess_split(env.herd[i][1], env.herd[i+1][1])
            # At a low probability, use a random cross point instead.
            if randint(0,50) == 25:
                cross_point = randint(3, 5)

            temp1 = env.herd[i][1][:cross_point] + env.herd[i+1][1][cross_point:] 
            temp2 = env.herd[i+1][1][:cross_point] + env.herd[i][1][cross_point:]
            env.herd[i] = (fitness(temp1), temp1)
            env.herd[i+1] = (fitness(temp2), temp2)
    # if population has an odd number, cross the last one with the first one
    # essentially this means the last one crossed with the second one.
    if len(env.herd) % 2 == 1:
            temp1 = env.herd[i][1][:cross_point] + env.herd[0][1][cross_point:] 
            temp2 = env.herd[0][1][:cross_point] + env.herd[i][1][cross_point:]
            env.herd[i] = (fitness(temp1), temp1)
            env.herd[0] = (fitness(temp2), temp2)
    pass


def mutate(mutation):
    # individual: (fitness, board): (2, [2, 4, 1, 7, 0, 3, 6, 2])
    for individual in env.herd:
        if randint(0,100) < mutation:
            individual[1][randint(0,7)] = randint(0,7)


def main():
    global env
    args = parse_args()
    generations = int(args.generations)
    mutation = float(args.mutation)
    population = int(args.population)
    step = int(args.step)
    verbose = args.verbose
    f = open('queens.log', 'w')
    f.write('')
    f.close()

    env = Environment(population)

    f = open('queens.log', 'a')
    goal_reached = logger(f, 1)
    if goal_reached:
        print(f'Goal reached in generation 1.')
        f.close()
        return

    # Don't let users set the step too high if the mutation starts out low.
    if mutation < 10 and step > 0:
        step = 1

    for gen in range(generations-1):
        cull()
        cross()
        mutate(mutation)
        goal_reached = logger(f, gen+2)
        if goal_reached:
            print(f'Goal reached in generation {gen+2}.')
            break
        else: 
            mutation -= step
    f.close()


if __name__ == '__main__':
    main()

