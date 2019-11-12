# Software Carpentry
# Group Project - Lazor Game
# Group 5: Aditiya Suru, Casey Zhu, Lincoln Kartchner
# initialize_board.py

'''
Reads in .bff file, returning all relevant parameters.
Also includes nperms() for calculating possible permutations of a list
'''

import sys
import operator
from collections import Counter
from functools import reduce
from math import factorial

# Initialize block reference information
valid_grid = ['o', 'x', 'a', 'b', 'c']
special_blocks = {
    'a': 'reflect',
    'b': 'opaque',
    'c': 'refract'
}


def nperms(plist):
    '''
    Calculates the possible permutations of a list

    **Parameters**

        plist: list
            The list to permute, made up of elements from valid_grid

    **Returns**

        perms: int
            The integer number of possible permutations
    '''

    num = factorial(len(plist))
    count_vals = Counter(plist).values()
    den = reduce(operator.mul, (factorial(i) for i in count_vals), 1)
    perms = num / den
    return(perms)


def readBoard():
    '''
    Reads in .bff file, returning relevant board parameters

    **Parameters**

        None

    **Returns**

        filename: str
            Name of the .bff file being read in.
            Includes file extension (.bff)

        initGrid: list
            List of lists, making up the input (empty) given board

        gridAsList: list
            initGrid, but reshaped to be a single list

        blocks: list
            List of tuples, each index corresponding to a different block type
            Tuples contain 2 values, the letter of the block (str),
            and the number of those blocks given (int)

        openSpaces: int
            The number of open 'o' spaces on the initial board

        lasers: list
            List of tuples, each corresponding to a different laser
            Tuple indices are int type, corresponding to x, y, dx, dy

        targets: list
            List of tuples, each corresponding to a different target
            Tuple indices are x, y coordinates of the target

        w: int
            Width of the input board

        h: int
            Height of the input board

        empty: list
            List of tuples, each corresponding to an 'x' cell
            Tuple indices are x, y coordinates of the 'x' cell
    '''

    print("Welcome to the Lazor board solver!")
    bfile = input("Enter the board (.bff file) you want to solve: ")
    filename = bfile.split('\\')[-1]

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
            # Check that first character is a valid string
            try:
                firstChar = i[0].upper()
            except SyntaxError:
                print("Error: non-char in grid!")

            # Ignore comments and whitespace
            if firstChar == '#' or firstChar == '\n' or firstChar == '\t':
                continue

            # Get reflect blocks
            elif firstChar == 'A':
                line = ''.join(i.split())
                count = int(line[1:])
                blocks[0] = ('A', count)

            # Get opaque blocks
            elif firstChar == 'B':
                line = ''.join(i.split())
                count = int(line[1:])
                blocks[1] = ('B', count)

            # Get refract blocks
            elif firstChar == 'C':
                line = ''.join(i.split())
                count = int(line[1:])
                blocks[2] = ('C', count)

            # Get lasers
            elif firstChar == 'L':
                line = i.split()
                # Initialize lazor
                x = int(line[1])
                y = int(line[2])
                dx = int(line[3])
                dy = int(line[4])
                lasers.append((x, y, dx, dy))

            # Get targets
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
    empty = []
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
            if initGrid[i][j] == 'x':
                empty.append((j, i))

    # Get grid width
    w = len(initGrid[0])
    h = len(initGrid)

    return (filename, initGrid, gridAsList, blocks,
            openSpaces, lasers, targets, w, h, empty)


if __name__ == "__main__":
    assert nperms([1, 0, 0, 0]) == 4

    # Couldn't write unit tests for readBoard() 
    # since it relies on the user entering a filename
