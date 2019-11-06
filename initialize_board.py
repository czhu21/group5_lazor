# Software Carpentry
# Group Project - Lazor Game
# Group 5: Aditiya Suru, Casey Zhu, Lincoln Kartchner
# initialize_board.py

from sympy.utilities.iterables import multiset_permutations
import sys
import operator
from collections import Counter
from math import factorial
from functools import reduce
from copy import deepcopy
import time
from lazor_print_soln import text_soln

# Initialize block reference information
valid_grid = ['o', 'x', 'a', 'b', 'c']
special_blocks = {
    'a': 'reflect',
    'b': 'opaque',
    'c': 'refract'
}


def nperms(l):
    '''
    '''
    num = factorial(len(l))
    mults = Counter(l).values()
    den = reduce(operator.mul, (factorial(v) for v in mults), 1)
    return(num/den)


def readBoard(filename):
    '''
    Reads in .bff file (filename)
    Parses for given board, including fixed blocks
    Parses for given available blocks
    Parses for lazers
    Parses for targets
    Initializes appropriate amount of each based on input numbers
    '''

    # Check if file exists, open if it does
    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print('Error: no such file exists')
        sys.exit()

    # Generate grid (list of lists) by checking for 'GRID START'
    initGrid = []
    start = False
    for i in f.readlines():
        if start:
            if "GRID STOP" in i:
                break
            initGrid.append(i)
        else:
            if "GRID START" in i:
                start = True

    if not start:
        print("Grid not initialized!")
        sys.exit()

    # Read through grid, grabbing special characters
    blocks = [None, None, None]
    lasers = []
    targets = []
    f.seek(0)
    start = False

    for i in f.readlines():
        if start:
            try:
                firstChar = i[0].upper()
            except SyntaxError:
                print("Error: non-char in grid!")

            if firstChar == '#' or firstChar == '\n' or firstChar == '\t':
                continue

            elif firstChar == 'A':
                line = ''.join(i.split())
                count = int(line[1:])
                blocks[0] = ('A', count)
                for i in range(count):
                    pass
                    # Initialize reflect block

            elif firstChar == 'B':
                line = ''.join(i.split())
                count = int(line[1:])
                blocks[1] = ('B', count)
                for i in range(count):
                    pass
                    # Initialize opaque block

            elif firstChar == 'C':
                line = ''.join(i.split())
                count = int(line[1:])
                blocks[2] = ('C', count)
                for i in range(count):
                    pass
                    # Initialize refract block

            elif firstChar == 'L':
                line = i.split()
                # Initialize lazor
                x = int(line[1])
                y = int(line[2])
                dx = int(line[3])
                dy = int(line[4])
                lasers.append((x, y, dx, dy))

            elif firstChar.upper() == 'P':
                line = i.split()
                # Initialize target
                x = int(line[1])
                y = int(line[2])
                targets.append((x, y))

            else:
                print('Warning: line begins with an invalid character')
                continue
        else:
            if "GRID STOP" in i:
                start = True
    f.close()

    # Check if necessary board components are provided
    if not start:
        print("Grid not stopped!")
        sys.exit()

    if not targets:
        print("No targets were provided!")
        sys.exit()

    if not lasers:
        print("No lasers were provided!")
        sys.exit()

    if all(i is None for i in blocks):
        print("No blocks were provided!")
        sys.exit()

    # Prep grid for conversion to list
    for i, v in enumerate(initGrid):
        initGrid[i] = v.split()

    # Convert grid to single list, get num of available spaces
    openSpaces = 0
    gridAsList = []
    for i in range(len(initGrid)):
        for j in range(len(initGrid[0])):
            initGrid[i][j] = initGrid[i][j].strip()
            initGrid[i][j] = initGrid[i][j].lower()

            gridAsList.append(initGrid[i][j])

            if initGrid[i][j] in valid_grid:
                pass
            else:
                print(initGrid[i][j])
                print('Error: Invalid block in grid!')
                sys.exit()

            if initGrid[i][j] == 'o':
                openSpaces += 1

    # init_NS, init_EW = get_nsew_coords(initGrid)
    # Get grid width
    w = len(initGrid[0])
    h = len(initGrid)

    return(initGrid, gridAsList, blocks, openSpaces, lasers, targets, w, h)


# def get_nsew_coords(grid):
#     NS = []
#     EW = []
#     for i in range(len(grid)):
#         for j in range(len(grid[0])):
#             if grid[i][j] in special_blocks:
#                 NS.append({(2*i+1, 2*j): special_blocks[grid[i][j]]})
#                 NS.append({(2*i+1, 2*j+2): special_blocks[grid[i][j]]})
#                 EW.append({(2*i, 2*j+1): special_blocks[grid[i][j]]})
#                 EW.append({(2*i+2, 2*j+2): special_blocks[grid[i][j]]})

#     return(NS, EW)


def get_permute_list(gridAsList, blocks, openSpaces):
    '''

    '''
    permute_list = []
    for i in blocks:
        if i is not None:
            for j in range(i[1]):
                permute_list.append(i[0].upper())

    for i in range(openSpaces - len(permute_list)):
        permute_list.append('o')

    return(permute_list)


def generateBoards(plist, gridAsList, w):
    '''
    '''
    # print(gridAsList)
    # print(plist)
    tries = 0

    for i in multiset_permutations(plist):
        dictOfBlocks = {}
        temp = deepcopy(gridAsList)
        index = 0

        for j in range(len(temp)):
            if temp[j] == 'o':
                temp[j] = i[index]
                index += 1
        # print(temp)

        mat = [temp[i:i+w] for i in range(0, len(temp), w)]
        # print(mat)

        for i in range(len(mat)):
            for j in range(len(mat[0])):
                cell = mat[i][j].lower()
                if cell in special_blocks.keys():
                    dictOfBlocks[(j, i)] = cell.upper()
        tries += 1
        # print(dictOfBlocks)
    # print(tries)
    return(tries)


if __name__ == "__main__":
    # TEMPORARY SOLUTION FOR YARN_5, REPLACE WITH ACTUAL SOLUTION LATER
    soln = {(0, 0): 'A', (1, 0): 'B', (3, 0): 'A', (4, 0): 'A', (0, 1): 'A', (1, 1): 'A', (4, 1): 'A', (4, 2): 'A', (0, 3): 'A', (0, 5): 'B'}
    # KEEP FILE AS YARN_5 FOR NOW
    bfile = '.\\bff_files\\yarn_5.bff'
    filename = bfile.split('\\')[-1]
    print('-=-' * 17)
    print('Solving board: ' + filename)
    t0 = time.time()

    initGrid, gridAsList, blocks, openSpaces, \
        lasers, targets, w, h = readBoard(bfile)
    solnGrid = initGrid
    plist = get_permute_list(gridAsList, blocks, openSpaces)
    tries = generateBoards(plist, gridAsList, w)
    tf = time.time()
    runtime = tf - t0

    print('Run finished. Time: %0.5f sec' % (runtime))
    print('-=-' * 17)

    text_soln(filename, initGrid, soln, tries, runtime)