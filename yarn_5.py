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
                # lasers = True
                line = i.split()
                print(line)
                x = int(line[1])
                y = int(line[2])
                vx = int(line[3])
                vy = int(line[4])
                lasers.append((x, y, vx, vy))
                

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

    return(initGrid, gridAsList, blocks, lasers, openSpaces, targets, w)


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


def solveBoard(plist, gridAsList, w):
    '''
    '''
    # print(gridAsList)
    # print(plist)

    listOfDicts = []

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

        for i in range(len(mat)):
            for j in range(len(mat[0])):
                cell = mat[i][j].lower()
                if cell in special_blocks.keys():
                    dictOfBlocks[(j, i)] = cell.upper()
        listOfDicts.append(dictOfBlocks)

    return listOfDicts


class Block:

    def __init__(self, ctr_x, ctr_y):
        self.ctr_x = ctr_x
        self.ctr_y = ctr_y

    def __call__(self, typ):
        self.typ = typ

    def interact(self, position, direction):

        typ = self.typ
        if typ == 'N':
            return [((position[0] + direction[0], position[1] + direction[1]), direction)]
        elif typ == 'A':
            if position[0] % 2 == 1:
                return [(position, (direction[0], -direction[1]))]
            else:
                return [(position, (-direction[0], direction[1]))]
        elif typ == 'B':
            return 'END'
        elif typ == 'C':
            if position[0] % 2 == 1:
                return [(position, (direction[0], -direction[1])), ((position[0] + direction[0], position[1] + direction[1]), direction)]
            else:
                return [(position, (-direction[0], direction[1])), ((position[0] + direction[0], position[1] + direction[1]), direction)]
        else:
            pass


class Lazor:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.path = []


def boardCheck(width, height, listOfLazors, dictOfBlocks, targetList):
    blockList = [[0 for i in range(2 * width + 1)] for j in range(2 * height + 1)]

    # Initialize all the blocks to 'N' which are normal / "let is pass" blocks
    listOfHits = []


    for i in range(width):
        for j in range(height):
            blockList[2 * j + 1][2 * i + 1] = Block(2 * j + 1, 2 * i + 1)
            blockList[2 * j + 1][2 * i + 1].typ = 'N'


    for blk in dictOfBlocks:
        ctr_x = 2 * blk[0] + 1
        ctr_y = 2 * blk[1] + 1
        blockList[ctr_y][ctr_x].typ = dictOfBlocks[blk]

    # print(blockList[7][3].typ)


    # Lazor information initialize
    for lazor in listOfLazors:
        lazor.path.append((lazor.position, lazor.direction))

        condition = False
        while condition is False:

            # cx = lazor.path[-1][0][0]
            # cy = lazor.path[-1][0][1]
            # dx = lazor.path[-1][1][0]
            # dy = lazor.path[-1][1][1]


            if lazor.path[-1][0][0] + lazor.path[-1][1][0] < 0 or lazor.path[-1][0][0] + lazor.path[-1][1][0] > 2 * width or lazor.path[-1][0][1] + lazor.path[-1][1][1] < 0 or lazor.path[-1][0][1] + lazor.path[-1][1][1] > 2 * height:
                break

            if lazor.path[-1][0][0] % 2 == 0:
                new = blockList[lazor.path[-1][0][1]][lazor.path[-1][0][0] + lazor.path[-1][1][0]].interact((lazor.path[-1][0][0], lazor.path[-1][0][1]), (lazor.path[-1][1][0], lazor.path[-1][1][1]))
            else:
                new = blockList[lazor.path[-1][0][1] + lazor.path[-1][1][1]][lazor.path[-1][0][0]].interact((lazor.path[-1][0][0], lazor.path[-1][0][1]), (lazor.path[-1][1][0], lazor.path[-1][1][1]))

            if new == 'END':
                break
            else:
                lazor.path.append(new[0])

            if len(new) == 2:
                listOfLazors.append(Lazor((new[1][0][0], new[1][0][1]), (new[1][1][0], new[1][1][1])))

            # Break out of the for loop if the lazor reaches the boundary
            if new[0][0][0] + new[0][1][0] > 2 * width or new[0][0][0] + new[0][1][0] < 0 or new[0][0][1] + new[0][1][1] > 2 * height or new[0][0][1] + new[0][1][1] < 0:
                condition = True


            # Break out of the loop if the lazor goes into an infinite loop (max points = 100)
            # if len(lazor.path) > 3:
               #  if lazor.path[-1][0] == lazor.path[-2][0] and lazor.path[-2][0] == lazor.path[-3][0]:
               #      condition = True

            if len(lazor.path) > 2 and lazor.path[-1][0] == lazor.path[-2][0] and lazor.path[-2][0] == lazor.path[-3][0]:
                condition = True

        for hits in lazor.path:
            listOfHits.append(hits[0])
        # print(len(lazor.path), "\n", lazor.path)


    # for lazor in listOfLazors:
    #   lazor.path = []

    # print("Nos of lazers: ", len(listOfLazors))

    condition = True
    for target in targetList:
        if target not in listOfHits:
            condition = False
    return condition


if __name__ == "__main__":
    bfile = 'bff_files/yarn_5.bff'
    filename = bfile.split('\\')[-1]
    print('-=-' * 17)
    print('Solving board: ' + filename)
    t0 = time.time()
    print(readBoard('bff_files/yarn_5.bff'))

    initGrid, gridAsList, blocks, lasers, openSpaces, targets, w = readBoard(bfile)

    plist = get_permute_list(gridAsList, blocks, openSpaces)
    listOfDicts = solveBoard(plist, gridAsList, w)
    print(len(listOfDicts))
    print('-=-' * 17)
    print('Run finished. Time: %s sec' % (time.time() - t0))
    print('-=-' * 17)

    width = 5
    height = 6
    targetList = [(6, 9), (9, 2)]
    for dictOfBlocks in listOfDicts:
        # for lazor in listOfLazors:
        #     lazor.path = []
        listOfLazors = []
        listOfLazors.append(Lazor((4, 1), (1, 1)))
        result = boardCheck(width, height,  listOfLazors, dictOfBlocks, targetList)
        print(result)
        if result == True:
            print(dictOfBlocks)
            break
