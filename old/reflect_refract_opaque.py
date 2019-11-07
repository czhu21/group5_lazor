# Need to check if this works for "adjoining blocks"
# This does work for multiple lazers, multiple blocks though.
import operator

class Lazor():

    def __init__(self, pos_x, pos_y, dir_x, dir_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.dir_x = dir_x
        self.dir_y = dir_y


if __name__ == "__main__":
    
    # Input the board size info (from parse)
    I = 5
    J = 5
    width = 2 * I + 1
    height = 2 * J + 1

    listOfBlocks = {(3, 1):'C', (2, 2):'C', (4, 4):'C'}
    # print(listOfBlocks[(3, 1)])
    # print(list(listOfBlocks.keys()))

    listOfLazors = []
    listOfLazors.append( Lazor(8, 5, -1, -1) )
    listOfLazors.append( Lazor(2, 7, 1, -1))
    listOfLazors.append( Lazor(10, 1, -1, 1))

    NS = {}
    EW = {}

    for block in listOfBlocks:
        m = block[0]
        n = block[1]
        m = block[0]
        n = block[1]
        typ = listOfBlocks[block]
        NS[(2*m + 1, 2*n)] = typ
        NS[(2*m + 1, 2*n + 2)] = typ
        EW[(2*m, 2*n + 1)] = typ
        EW[(2*m + 2, 2*n + 1)] = typ

    print(list(NS.keys()))
    print(list(EW.keys()))

    lazorPath = []

    # Takes care of Reflect and Opaque

    for lazor in listOfLazors:
        cx = lazor.pos_x
        cy = lazor.pos_y
        dx = lazor.dir_x
        dy = lazor.dir_y

        lazerPosition = (cx, cy)
        lazerDirection = (dx, dy)

        condition  = False
        while condition == False:
            if lazerPosition in list(NS.keys()):
                if NS[lazerPosition] == 'B':
                    condition = True
                lazerDirection = tuple(map(operator.mul, lazerDirection, (1, -1)))
            elif lazerPosition in list(EW.keys()):
                if EW[lazerPosition] == 'B':
                    condition = True
                lazerDirection = tuple(map(operator.mul, lazerDirection, (-1, 1)))
            else:
                pass

            lazorPath.append(lazerPosition)
            lazerPosition = tuple(map(operator.add, lazerPosition, lazerDirection))

            if lazerPosition[0] == -1 or lazerPosition[0] == width or lazerPosition[1] == -1 or lazerPosition[1] == height:
                condition = True

    # Takes care of refract and relfect
    
    for lazor in listOfLazors:
        cx = lazor.pos_x
        cy = lazor.pos_y
        dx = lazor.dir_x
        dy = lazor.dir_y

        lazerPosition = (cx, cy)
        lazerDirection = (dx, dy)

        condition  = False
        while condition == False:
            if lazerPosition in list(NS.keys()):
                if NS[lazerPosition] == 'C':
                    lazerDirection = tuple(map(operator.mul, lazerDirection, (1, 1)))
                else:
                    lazerDirection = tuple(map(operator.mul, lazerDirection, (1, -1)))
                
            elif lazerPosition in list(EW.keys()):
                if EW[lazerPosition] == 'C':
                    lazerDirection = tuple(map(operator.mul, lazerDirection, (1, 1)))
                else:
                    lazerDirection = tuple(map(operator.mul, lazerDirection, (-1, 1)))
                
            else:
                pass

            lazorPath.append(lazerPosition)
            lazerPosition = tuple(map(operator.add, lazerPosition, lazerDirection))

            if lazerPosition[0] == -1 or lazerPosition[0] == width or lazerPosition[1] == -1 or lazerPosition[1] == height:
                condition = True




    print(lazorPath)
