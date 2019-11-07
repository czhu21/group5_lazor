class Block:

    def __init__(self, ctr_x, ctr_y):
        self.ctr_x = ctr_x
        self.ctr_y = ctr_y

    def __call__(self, typ):
        self.typ = typ

    def interact(self, cx, cy, dx, dy):

        typ = self.typ
        if typ == 'N':
            return [(cx + dx, cy + dy, dx, dy)]
        elif typ == 'A':
            if cx % 2 == 1:
                return [(cx, cy, dx, -dy)]
            else:
                return [(cx, cy, -dx, dy)]
        elif typ == 'B':
            return 'END'
        elif typ == 'C':
            if cx % 2 == 1:
                return [(cx, cy, dx, -dy), (cx + dx, cy + dy, dx, dy)]
            else:
                return [(cx, cy, -dx, dy), (cx + dx, cy + dy, dx, dy)]
        else:
            pass


class Lazor:
    def __init__(self, cx, cy, dx, dy):
        self.cx = cx
        self.cy = cy
        self.dx = dx
        self.dy = dy
        self.path = []


if __name__ == '__main__':

    # From the parsed data
    width = 4
    height = 4
    # Lazor list initializing
    listOfLazors = []
    listOfLazors.append(Lazor(2, 1, 1, -1))
    # From the permute function
    dictOfBlocks = {(0, 0): 'B', (1, 0): 'C'}

    # Block initializing
    blockList = [[0 for i in range(2 * width + 1)] for j in range(2 * height + 1)]

    # Initialize all the blocks to 'N' which are normal / "let is pass" blocks
    for i in range(width):
        for j in range(height):
            blockList[2 * i + 1][2 * j + 1] = Block(2 * i + 1, 2 * j + 1)
            blockList[2 * i + 1][2 * j + 1].typ = 'N'

    for blk in dictOfBlocks:
        ctr_x = 2 * blk[0] + 1
        ctr_y = 2 * blk[1] + 1
        blockList[ctr_x][ctr_y].typ = dictOfBlocks[blk]

    # Lazor information initialize


    for lazor in listOfLazors:
        lazor.path.append((lazor.cx, lazor.cy, lazor.dx, lazor.dy))

        condition = False
        ctr = 0
        while condition == False:

            cx = lazor.path[-1][0]
            cy = lazor.path[-1][1]
            dx = lazor.path[-1][2]
            dy = lazor.path[-1][3]

            if cx + dx < 0 or cx + dx > 8 or cy + dy < 0 or cy + dy > 8:
                break

            if cx % 2 == 0:
                new = blockList[cx + dx][cy].interact(cx, cy, dx, dy)
            else:
                new = blockList[cx][cy + dy].interact(cx, cy, dx, dy)

            if new == 'END':
                break
            else:
                lazor.path.append(new[0])

            if len(new) == 2:
                listOfLazors.append(Lazor(new[1][0], new[1][1], new[1][2], new[1][3]))
            
            # Break out of the for loop if the lazor reaches the boundary
            if new[0][0] + new[0][2] > 8 or new[0][0] + new[0][2] < 0 or new[0][1] + new[0][3] > 8 or new[0][1] + new[0][3] < 0:
                condition = True

            # Break out of the loop if the lazor goes into an infinite loop (max points = 100)
            if len(lazor.path) > 100:
                condition = True

        print(lazor.path)
        
        # How to reduce time
        '''
        1) Infinite loop max iteration limit. Find patters in the "inifinite loop". But that will lead to searching. What is the maximum max value that we can have ?
        2) Do not "save value" and then pass it. Pass it as it is.
        3) Minimizde search operations (Rather than searching for NS / EW, this code directly interacts with the Blocks)
        4) Minimize FLOPS / any arithmetic operations
        5) Minimize any logical operations
        '''



