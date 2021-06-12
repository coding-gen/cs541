#!/usr/bin/env python

# Programming assignment 2
# PSU CS541 Spring Semester 2021
# 11 June 2021
# Final Project: relational database join optimizer
# Using Genetic Algorithm
# Author: Genevieve LaLonde

import argparse
from random import randint, shuffle
from math import floor, ceil, log
from statistics import stdev, variance, mean
import psycopg2
from psycopg2 import sql
from copy import copy


global env
global sample_stats
global cardinality_stats
global rowcount_stats
global random_tree


def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
             description="Specify parameters for the genetic algorithm join optimizer.")
    parser.add_argument(
        '-t', '--table-list', 
        dest='tables',
        nargs='+', 
        default=[],
        help="The tables being joined in the query.")
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


def myrand(x):
    # x = len(env.herd)
    return randint(0, x)


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


def inversion():
    # invert an individual
    pass


def increase_test_hardness():
    # make it harder to pass the test
    # eg hosts and parasited from Hillis as described in: 
    # An Intro to Genetic Algorithms, by Melanie Mitchell
    pass


def roulette():
    pass


def rank_fitness():
    pass


def random_death():
    # with or without elitism
    pass

def wrong_side_of_railroad_tracks():
    # In selection, breeding can only happen if both members are
    # both in the same upper half or lower half of population fitness
    # With small chance of Tony and Maria to fall in love.
    # May or may not be accompanied by mass random death.
    pass


def wandering_salesman():
    # No, not the one you're thinking. 
    # A random, unrelated addition to the population.
    pass


# connect to the database
def dbconnect(dbname, username, passwd, hostname='localhost'):
  connection = psycopg2.connect(
        host=hostname,
        database=dbname,
        user=username,
        password=passwd,
  )
  connection.autocommit = True
  return connection


def collect_rowcount(conn, table_name):
    rows = 0
    with conn.cursor() as cursor:
        # Get the count of distinct values of the ID as the cardinality.
        cmd = sql.SQL(f"SELECT COUNT(*) FROM {table_name};")
        cursor.execute(cmd)
        rows = cursor.fetchone()
    return rows[0]


def collect_cardinality(conn, table_name = 'tester'):
    cardinality = 0
    with conn.cursor() as cursor:
        # Get the count of distinct values of the ID as the cardinality.
        cmd = sql.SQL(f"SELECT count(distinct id) FROM {table_name};")
        cursor.execute(cmd)
        cardinality = cursor.fetchone()
    return cardinality[0]


def collect_sample(conn, table_name, table_size):
    sample_table = []

    # Adjust the amount sampled according to the size of the source table
    # So long as we are getting a statistically random sample,
    # We can use it to estimate selectivity.
    n = 1
    if table_size > 1000: 
        n = round(log(table_size, 2))

    with conn.cursor() as cursor:
        # Sample 0.1% of the source table
        cmd = sql.SQL(f"SELECT id FROM {table_name} WHERE 1 = ceil(random()*{n});")
        cursor.execute(cmd)
        sample_table = cursor.fetchall()
    return [x[0] for x in sample_table]


def analyze_tables(conn, tables):
    # Collect cardinality stats and a sampling table, stored locally.
    global sample_stats
    global cardinality_stats
    global rowcount_stats
    sample_stats = []
    cardinality_stats = []
    rowcount_stats = []

    for i in range(len(tables)):
        # collect stats on each table 
        rowcount_stats.append(collect_rowcount(conn,tables[i]))
        cardinality_stats.append(collect_cardinality(conn, tables[i]))
        sample_stats.append(collect_sample(conn, tables[i], rowcount_stats[i]))
    return


def build_random_tree(table_list):
    global random_tree
    # TODO this breaks for 3+ trees, find out why.

    # recursively split the tree until you're at individual elements
    # while randomly rearanging the elements in each subtree
    # at each split re-add the left/right children as a new list to this list
    local_tables = copy(table_list)
    # Shuffle so the order is random
    shuffle(local_tables)
    print(local_tables)
    if len(local_tables) > 2:
        # We want at least 1 element in the left tree, at lest one in the right
        splitter = randint(1,len(local_tables)-1)
        left = build_random_tree(local_tables[0:splitter])
        if left:
            random_tree.append(left)    
        right = build_random_tree(local_tables[splitter:len(local_tables)])
        if right:
            random_tree.append(right)
    else:
        print(f'local string to return is {local_tables}')
        return local_tables
    return


class Environment():
    def __init__(self, tables, population):
        global random_tree
        # Encode as id of table in tables list
        # Separated by join level int.
        
        # Encode as random int from 0 to len of table list
        # create list of ints from 0 - len of table list
        # random sort, pop repeatedly and append between table ids
        
        # One list to hold all individuals in the population.
        
        self.herd = []
        
        # Create individuals.
        for individual in range(population):
            random_tree = []
            build_random_tree(tables)
            self.herd.append(random_tree)


def main():
    global env
    global sample_stats
    global cardinality_stats
    global rowcount_stats

    args = parse_args()
    tables = args.tables
    # tables will be identified by their index, in alphabetical order
    generations = int(args.generations)
    mutation = float(args.mutation)
    population = int(args.population)
    step = int(args.step)
    verbose = args.verbose

    f = open('optimizer.log', 'w')
    f.write('')
    f.close()

    conn = dbconnect('test', 'admin', 'rhodes')

    tables.sort()
    analyze_tables(conn, tables)

    conn.close()
    if verbose:
        print(tables)
        for i in range(len(tables)):
            print(f'rowcount of table {tables[i]} is {rowcount_stats[i]}')
            print(f'cardinality of table {tables[i]} is {cardinality_stats[i]/rowcount_stats[i]}')
            print(f'sample of table {tables[i]} is {sample_stats[i]}')


    env = Environment(tables, population)
    print(f'herd of {population} individuals is: {env.herd}')
    for individual in env.herd:
        for item in individual:
            print(f'type of item is: {type(item[0])}')
            if len(item) > 2:
                print(f'content is {item}')
    """
    f = open('optimizer.log', 'a')
    logger(f, 1)

    # Don't let users set the step too high if the mutation starts out low.
    if mutation < 10 and step > 0:
        step = 1

    for gen in range(generations-1):
        cull()
        cross()
        mutate(mutation)
        goal_reached = logger(f, gen+2)
        if goal_reached:
            print(f'Goal reached in generation {gen}.')
            break
        else: 
            mutation -= step
    f.close()
    """


if __name__ == '__main__':
    main()

