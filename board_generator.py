# Software Carpentry
# Lazor Project
# Group 5

'''
This generates all possible boards given the input parameters
'''

from sympy.utilities.iterables import multiset_permutations
from copy import deepcopy

# Initialize block reference information
valid_grid = ['o', 'x', 'a', 'b', 'c']
special_blocks = {
    'a': 'reflect',
    'b': 'opaque',
    'c': 'refract'
}


def get_permute_list(gridAsList, blocks, openSpaces):
    '''
    Creates a list of blocks for permuting

    **Parameters**

        gridAsList: list
            The input board grid reshaped as a single list
        blocks: list
            A list of the number of each block
            available for the given puzzle
        openSpaces: int
            The number of spaces available for placing blocks

    **Returns**

        permute_list: list
            A list of the available blocks to move,
            additional empty spaces added on until the length
            of permute_list matches openSpaces
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
    Generates all possible boards given the permute list.
    The board will be generated as a dictionary of the given blocks
    and their coordinates.
    Each board is appended to a cumulative list.

    **Parameters**

        plist: list
            The permute list (output from get_permute_list())
        gridAsList: list
            The input board grid reshaped as a single list
        w: int
            The width of the input board (how many cells across)

    **Returns**

        listOfDicts: list
            A list dictionaries, corresponding to all possible
            boards given the input blocks and available cells
    '''

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
        # print(mat)

        for i in range(len(mat)):
            for j in range(len(mat[0])):
                cell = mat[i][j].lower()
                if cell in special_blocks.keys():
                    dictOfBlocks[(j, i)] = cell.upper()
        listOfDicts.append(dictOfBlocks)
        # print(dictOfBlocks)
    return(listOfDicts)


if __name__ == "__main__":
    gridAsList = ['o', 'o', 'o', 'o']
    blocks = [('A', 1), None, None]
    openSpaces = 4
    plist = get_permute_list(gridAsList, blocks, openSpaces)
    assert plist == ['A', 'o', 'o', 'o']

    w = 2
    lod = generateBoards(plist, gridAsList, w)
    assert len(lod) == 4
    assert isinstance(lod, list)
    assert isinstance(lod[0], dict)
