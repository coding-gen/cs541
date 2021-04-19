#!/usr/bin/env python

import argparse
from random import randint

global env

def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
             description="Specify the agent.")
    parser.add_argument(
        '-a', '--agent-type',
        dest='agent_type',
        default='1',
        help="Agent type: 1: reflex, 2: random, 3: murphy's reflex, 4: murhpy's random") 
    parser.add_argument(
        '-d', '--dirty-rooms',
        dest='dirty',
        default=3,
        help="How many rooms are dirty.") 
    parser.add_argument(
        '-y', '--height',
        dest='height',
        default=3,
        help="How many rooms on the y axis.")
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
        help="How many rooms on the x axis.") 
    args = parser.parse_args()
    return args


class rumba():
    def __init__(self, location):
        self.location = [randint(0,2), randint(0,2)]

    def detect_clean(self):
        global env
        return env.rooms[self.location[0]][self.location[1]]['clean']

    def clean(self):
        env.rooms[self.location[0]][self.location[1]]['clean'] = True
        return

    def reflex_move(self):
        if self.location == [0,0]:
            self.location = [0,1]
        elif self.location == [0,1]:
            self.location = [0,2]
        elif self.location == [0,2]:
            self.location = [1,2]
        elif self.location == [1,2]:
            self.location = [2,2]
        elif self.location == [2,2]:
            self.location = [2,1]
        elif self.location == [2,1]:
            self.location = [2,0]
        elif self.location == [2,0]:
            self.location = [1,0]
        elif self.location == [1,0]:
            self.location = [1,1]
        elif self.location == [1,1]:
            self.location = [0,1]
            self.location = [0,0]

    def rand_move(self):
        # Randomize the direction.
        # If we're already at a wall, go the other way instead.
        direction = randint(0,3)
        if direction == 0:
            if self.location[0] != 2:
                self.location[0] += 1
            #else:
            #    self.location[0] += 1
        elif direction == 1:
            if self.location[1] != 2:
                self.location[1] += 1
            #else:
            #    self.location[1] += 1
        elif direction == 2:
            if self.location[0] != 0:
                self.location[0] -= 1
            #else:
            #    self.location[0] -= 1
        elif direction == 3:
            if self.location[1] != 0:
                self.location[1] -= 1
            #else:
            #    self.location[1] -= 1


class Environment():
    def __init__(self, width, height, dirty):
        self.width = width
        self.height = height

        # Build the space.
        rows = {}
        for j in range(height):
            row = {}
            for i in range(width):
                row[i] = {'clean': True}
            rows[j] = row
        self.rooms = rows

        # Dirty the rooms
        for i in range(dirty):
            childsplay_x = randint(0,2)
            childsplay_y = randint(0,2)
            while self.rooms[childsplay_y][childsplay_x]['clean'] == False:
                childsplay_x = randint(0,2)
                childsplay_y = randint(0,2)
            self.rooms[childsplay_y][childsplay_x]['clean'] = False


def main():
    global env
    args = parse_args()
    width = int(args.width)
    height = int(args.height)
    dirty = int(args.dirty)
    agent_type = int(args.agent_type)
    verbose = args.verbose
    env = Environment(width, height, dirty)

    if verbose:
        print('Starting state:')
        print (f'width = {env.width}')
        print (f'height = {env.height}')
        for i in range(3):
            for j in range(3):
                print(f"Room {i},{j} is clean: {env.rooms[i][j]['clean']}")
        print('-----')
    z = rumba(0)

    cleans = 0
    moves = 0
    any_dirty = True
    for i in range(100):
        while any_dirty == True:
            any_dirty = False
            for i in range(3):
                for j in range(3):
                    if not env.rooms[i][j]['clean']:
                        any_dirty = True
            #print(f'Rumba is at: {z.location}.')
            if agent_type == 1:
                if z.detect_clean():
                    #print('It\'s clean here! Moving on.')
                    if z.location == 4:
                        moves += 1
                    z.reflex_move()
                    moves += 1
                else:
                    #print('Cleaning this dirty room.')
                    z.clean()
                    cleans += 1
            elif agent_type == 2:
                if randint(0,1) == 0:
                    z.clean()
                    cleans += 1
                else:
                    z.rand_move()
                    moves += 1

    dirty_rooms = 0
    for i in range(3):
        for j in range(3):
            if not {env.rooms[i][j]['clean']}:
                dirty_rooms += 1

    if verbose:
        print(f"Moves taken: {moves}")
        print(f"Cleanings performed: {cleans}")
        print(f"Rooms still dirty: {dirty_rooms}")
    else:
        print(dirty, moves, cleans)

if __name__ == '__main__':
    main()
