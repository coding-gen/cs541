#!/usr/bin/env python

import argparse
from random import randint

global env


class rumba():
    def __init__(self, location):
        self.location = randint(0,8)

    def detect_clean(self):
        global env
        return env.rooms[self.location]['clean']

    def clean(self):
        env.rooms[self.location]['clean'] = True
        return

    def move(self):
        if self.location == 0:
            self.location = 1
        elif self.location == 1:
            self.location = 2
        elif self.location == 2:
            self.location = 5
        elif self.location == 5:
            self.location = 8
        elif self.location == 8:
            self.location = 7
        elif self.location == 7:
            self.location = 6
        elif self.location == 6:
            self.location = 3
        elif self.location == 3:
            self.location = 4
        elif self.location == 4:
            self.location = 1
            self.location = 0


class Environment():
    def __init__(self, width, height, dirty):
        self.width = width
        self.height = height
        self.rooms = {\
            0: {'clean': True}, \
            1: {'clean': True}, \
            2: {'clean': True}, \
            3: {'clean': True}, \
            4: {'clean': True}, \
            5: {'clean': True}, \
            6: {'clean': True}, \
            7: {'clean': True}, \
            8: {'clean': True} \
            }
        for i in range(dirty):
            childsplay = randint(0,8)
            while self.rooms[childsplay]['clean'] == False:
                childsplay = randint(0,8)
            self.rooms[childsplay]['clean'] = False


def main():
    global env
    env = Environment(3, 3, 3)
    print('Starting state:')
    print (f'width = {env.width}')
    print (f'height = {env.height}')
    for i in range(9):
        print(f"Room {i} is clean: {env.rooms[i]['clean']}")
    print('-----')
    z = rumba(0)

    actions = 0
    any_dirty = True
    for i in range(100):
        while any_dirty == True:
            any_dirty = False
            for i in range(9):
                if not env.rooms[i]['clean']:
                    any_dirty = True
            #print(f'Rumba is at: {z.location}.')
            if z.detect_clean():
                #print('It\'s clean here! Moving on.')
                if z.location == 4:
                    actions +=1
                z.move()
            else:
                #print('Cleaning this dirty room.')
                z.clean()
            actions += 1
    dirty_rooms = 0
    for i in range(9):
        if not {env.rooms[i]['clean']}:
            dirty_rooms += 1


    print(f"Actions taken: {actions}")
    print(f"Rooms still dirty: {dirty_rooms}")

if __name__ == '__main__':
    main()