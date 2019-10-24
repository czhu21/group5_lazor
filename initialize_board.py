# Software Carpentry
# Group Project - Lazor Game
# Group 5: Aditiya Suru, Casey Zhu, Lincoln Kartchner
# initialize_board.py

import sys

def read_board(filename):
    '''
    Reads in .bff file (filename)
    Parses for given board, including fixed blocks
    Parses for given available blocks
    Parses for lazers
    Parses for targets
    Initializes appropriate amount of each based on input numbers
    '''

    f = open(filename, "r")
    valid_grid = ['o', 'x', 'a', 'b', 'c']
    special_blocks = {
        'a': 'reflect',
        'b': 'opaque',
        'c': 'refract'
    }

    grid = []
    start = False
    for i in f.readlines():
        if start:
            if "GRID STOP" in i:
                break
            grid.append(i)
        else:
            if "GRID START" in i:
                start = True

    f.seek(0)
    start = False
    for i in f.readlines():
        if start:
            if i[0] == "#" or i[0] == '\n':
                continue

            elif i[0].upper() == 'A':
                line = ''.join(i.split())
                count = int(line[1:])
                for i in range(count):
                    pass
                    # Initialize reflect block

            elif i[0].upper() == 'B':
                line = ''.join(i.split())
                count = int(line[1:])
                for i in range(count):
                    pass
                    # Initialize opaque block

            elif i[0].upper() == 'C':
                line = ''.join(i.split())
                count = int(line[1:])
                for i in range(count):
                    pass
                    # Initialize refract block

            elif i[0].upper() == 'L':
                line = i.split()
                # Initialize lazor
                x = int(line[1])
                y = int(line[2])
                vx = int(line[3])
                vy = int(line[4])

            elif i[0].upper() == 'P':
                line = i.split()
                # Initialize target
                x = int(line[1])
                y = int(line[2])

            else:
                #print('Warning: line begins with an invalid character')
                continue
        else:
            if "GRID STOP" in i:
                start = True

    for i, v in enumerate(grid):
        grid[i] = v.split(' ')
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = grid[i][j].strip()
            grid[i][j] = grid[i][j].lower()

            if grid[i][j] in valid_grid:
                pass
            else:
                print('Error: Invalid block in grid!')
                sys.exit()

    NS = []
    EW = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in special_blocks:
                NS.append({(2*i+1, 2*j): special_blocks[grid[i][j]]})
                NS.append({(2*i+1, 2*j+2): special_blocks[grid[i][j]]})
                EW.append({(2*i, 2*j+1): special_blocks[grid[i][j]]})
                EW.append({(2*i+2, 2*j+2): special_blocks[grid[i][j]]})
    print(NS)
    print(EW)
    return(grid)
    f.close()


if __name__ == "__main__":
    x = read_board('yarn_5.bff')
    print(x)
