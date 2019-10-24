# Software Carpentry
# Group Project - Lazor Game
# Group 5: Aditiya Suru, Casey Zhu, Lincoln Kartchner
# initialize_board.py


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
    spacial_blocks = ['a', 'b', 'c']
    grid = []

    for i in f.readlines():
        if i == 'GRID START':
            break
        else:
            continue

    for i in f.readlines():
        if i == 'GRID STOP':
            break
        else:
            grid.append(i)
            continue

    f.seek(0)
    for i in f.readlines():
        if i[0] == "#" or i[0] == '\n':
            continue

        # elif i[0].lower() in valid_grid:
        #     grid.append(i.strip())

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

    for i, v in enumerate(grid):
        grid[i] = v.split(' ')

    NS = []
    EW = []

    # for i in range(len(grid)):
    #     for j in range(len(grid[0])):
    #         print(grid[i][j])

    return(grid)
    f.close()


if __name__ == "__main__":
    x = read_board('mad_4.bff')
    print(x)
