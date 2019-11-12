# LAZOR
# simulate_board.py
'''
This file simulates and checks if the given board
with the given arrangement of blocks is the correct solution

It checks if all the targets are in pathh of the lazer or not.

it contains
1) Class Block - defines the "blocks"
2) Class Lazor - defines the "lazor"
3) boardCheck function - checks if the board is the correct solution
4) getSolution function - bridge between lazor.py and simulate_board

'''

import sys

# Initialize block reference information
valid_grid = ['o', 'x', 'a', 'b', 'c']
special_blocks = {
    'a': 'reflect',
    'b': 'opaque',
    'c': 'refract'
}


class Block:
    '''
    Defines a block on the given board.
    Eg: For a 4 X 4 board, there will be 16 blocks.

    attributes and call
        ctr_x - the centre x coordinate of the block
        ctr_y - the centre y coordinate of the block
        typ - the type of the block (Refract / reflect...)

    types of blocks
        N - Normal: Lets lazor pass through
        A - Reflect: Reflects the lazer
        B - Opaque: Absorbs the lazer
        C - Refract: Combination of N and A

    interact function
        the lazer interacts with each block it comes in contact with

        parameters:
            lazer position
            lazer direction

        output:
            updated position and direction

        Example, assume a laser is at (2, 7), going in (1, -1):
            It is interacting with the block whose center is (3, 7)
            After interaction, the direction and or or position witll change
            If the 3, 7 block is Normal, the laser position will change,
            but the direction remains same.

            If the 3,7 block is reflect,the position remains same,the direction
            changes. With the same position,but the updated direction,the lazer
            will now interact with the 1, 7 block!!!

            If the 3, 7 block is opaque, end lazer !

            If the 3, 7 block is refract, append a new lazer to the listOfLazer
            And reflect (change the direction)

    '''

    def __init__(self, ctr_x, ctr_y):
        # The block center coordinates
        self.ctr_x = ctr_x
        self.ctr_y = ctr_y

    def __call__(self, typ):
        # The block type
        self.typ = typ

    def interact(self, position, direction):
        typ = self.typ
        # If normal, let the lazer pass. Position updated, direction same
        if typ == 'N':
            return [((position[0] + direction[0],
                      position[1] + direction[1]), direction)]
        # If Type A, change the direction based on the N/S or E/W face
        # Finding out which face the lazer is interacting with is easy to find
        # If the x-coordinate of lazer is divisible by 2,
        # it is going to left/right
        # Hence, it is interacting with the E/W face ! And vice - versa
        elif typ == 'A':
            if position[0] % 2 == 1:
                return [(position, (direction[0], -direction[1]))]
            else:
                return [(position, (-direction[0], direction[1]))]
        # If type B, then return End of lazer
        elif typ == 'B':
            return 'END'
        # If type C, the return 2 lazers:
        # One relfected Based on type A
        # The other "refracted", change the position, keep the direction same.
        # Same as type N
        elif typ == 'C':
            if position[0] % 2 == 1:
                return [(position, (direction[0], -direction[1])),
                        ((position[0] + direction[0], position[1] +
                            direction[1]), direction)]
            else:
                return [(position, (-direction[0], direction[1])),
                        ((position[0] + direction[0], position[1] +
                          direction[1]), direction)]
        # Easy to include other block types if required
        else:
            print("Wrong block type???")
            pass


class Lazor:
    '''
    This is the lazor class.
    This stores all information about a given lazer
    Definitions:
    1) position - initial position
    2) Direction - initial direction
    3) path - This is a list of tuples of position and direction.

    For example, if a lazer is at 2, 7, going in -1, 1. And all blocks are N
    Then the path will be [((2, 7), (-1, 1)), ((1, 8), (-1, 1), ...)]

    The path will be appended as the laser moves and interacts with the blocks
    '''

    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.path = []


def boardCheck(width, height, listOfLazors, dictOfBlocks, targetList):
    '''
    The function checks if the board is correct or wrong

    inputs
        width - Width of the board
        height - Height of the board
        listOfLazors - All the lazors given from the .bff file
        dictOfBlocks - the block position on the board as found by permutations
        targetList - list of the targets from the .bff file

    outputs
        condition: True if correct, False if wrong board

    How does it work

    First all the boards are set to normal.
    Then based on the dictOfBlocks, we update their types.
    Example - if block at 1, 2 is refract,
    the corresponding block type is changed

    then for each lazor in the list of lazors, we track the path of the
    lazor by letting it interact with each block

    the list of lazors is appended if a new lazor is
    created by the refract block

    width and height are in the "big coordinates picture based"
    While all other coordinates are as per the specifications

    width and height will be 4, 4
    the coordinates will range from 0, 8 and 0, 8

    then for each lazor, the list of points it touches is put in a list
    This is the list of hits.

    The target list is checked with the listOfHits.

    If all targets are present in list of hits, its a success
    And True is returned
    Otherwise, return False

    '''
    blockList = [[0 for i in range(2 * width + 1)]
                 for j in range(2 * height + 1)]

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
        while not condition:

            cx = lazor.path[-1][0][0]
            cy = lazor.path[-1][0][1]
            dx = lazor.path[-1][1][0]
            dy = lazor.path[-1][1][1]

            # If the lazer initially is going outside the board, then break
            if (cx + dx < 0 or cx + dx > 2 * width or
                    cy + dy < 0 or cy + dy > 2 * height):
                break

            if cx % 2 == 0:
                new = blockList[cy][cx + dx].interact((cx, cy), (dx, dy))
            else:
                new = blockList[cy + dy][cx].interact((cx, cy), (dx, dy))

            if new == 'END':
                break
            else:
                lazor.path.append(new[0])

            if len(new) == 2:
                listOfLazors.append(Lazor((new[1][0][0],
                                           new[1][0][1]), (new[1][1][0],
                                                           new[1][1][1])))

            # Break out of the for loop if the lazor reaches the boundary
            if (new[0][0][0] + new[0][1][0] > 2 * width or
                new[0][0][0] + new[0][1][0] < 0 or
                new[0][0][1] + new[0][1][1] > 2 * height or
                    new[0][0][1] + new[0][1][1]) < 0:
                condition = True

            # Break out of the loop if the lazer is in a "stale-mate" position
            if (len(lazor.path) > 2 and lazor.path[-1][0] ==
                    lazor.path[-2][0] and
                    lazor.path[-2][0] == lazor.path[-3][0]):
                condition = True

        for hits in lazor.path:
            listOfHits.append(hits[0])

    condition = True
    for target in targetList:
        if target not in listOfHits:
            condition = False
    return condition


def get_solution(listOfDicts, w, h, lasers, dictOfBlocks, targetList):
    '''
    This recieves a list of all the dictionaries of possible board permutations
    And calls the boardcheck function for each dictionary
    If a dictionary is a correct configuration of blocks, it returns true

    Inputs
        listOfDicts - a list of all possible block permutations in the
        form of a dictionary
        w - width
        h - height

    Returns
        It returns the solution (dictof blocks)
        number of tries
        listOfLazors. This will be used to make the Image of the correct board.
    '''
    soln = None
    tries = 0

    listOfLazors = []
    for i in lasers:
        listOfLazors.append(Lazor((i[0], i[1]), (i[2], i[3])))

    for dictOfBlocks in listOfDicts:

        # ReInitialze the listOfLazors to remove the data from old permutations
        listOfLazors = []
        for i in lasers:
            listOfLazors.append(Lazor((i[0], i[1]), (i[2], i[3])))

        for lazor in listOfLazors:
            lazor.path = []
        tries += 1

        result = boardCheck(w, h, listOfLazors, dictOfBlocks, targetList)
        # print(result)
        if result:
            # print(dictOfBlocks)
            soln = dictOfBlocks
            break

    if soln is None:
        print("No possible solution for the given parameters!")
        sys.exit()

    return(soln, tries, listOfLazors)


if __name__ == "__main__":

    
    # Assert unit test
    listOfDicts = [{(0, 0): 'A'}, {(1, 0): 'A'}]
    w = 2
    h = 2
    lasers = [(1, 0, 1, 1)]
    targetList = [(1, 2)]
    dictOfBlocks = {}

    soln, tries, listOfLazors = get_solution(listOfDicts, w, h,
                                             lasers, dictOfBlocks,
                                             targetList)
    assert soln == {(1, 0): 'A'}
    assert tries == 2
    assert len(listOfLazors) == 1

    pass

