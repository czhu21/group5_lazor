# Software Carptentry
# Lazor Project
# Group 5
# Lazor Board Solver

from simulate_board import get_solution
from print_solution import text_soln
from initialize_board import readBoard, nperms
from board_generator import get_permute_list, generateBoards
import time

if __name__ == "__main__":
    t0 = time.time()

    filename, initGrid, gridAsList, dictOfBlocks, openSpaces, \
        lasers, targetList, width, height = readBoard()
    print('Input file read finished...')

    plist = get_permute_list(gridAsList, dictOfBlocks, openSpaces)
    possible = nperms(plist)

    listOfDicts = generateBoards(plist, gridAsList, width)
    print('Board generation finished...')

    soln, tries = get_solution(listOfDicts, width, height, lasers, dictOfBlocks, targetList)
    print('Board solution found...')

    text_soln(filename, initGrid, soln, tries, possible, (time.time()-t0))
    runtime = time.time() - t0
    print('Solution published. Total time: %0.5f sec' % (runtime))
    print('-=-' * 17)
