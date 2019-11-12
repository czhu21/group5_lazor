# Software Carptentry
# Lazor Project
# Group 5
# Lazor Board Solver

'''
This imports all of the modules/functions involved in the lazor solver
Runs the functions necessary to solve the board
'''

from simulate_board import get_solution
from print_solution import text_soln
from initialize_board import readBoard, nperms
from board_generator import get_permute_list, generateBoards
import time
from image import place_blocks, plot_lazor_path

if __name__ == "__main__":
    # Initialize time
    t0 = time.time()

    # Read in board, get input parameters
    filename, initGrid, gridAsList, dictOfBlocks, openSpaces, \
        lasers, targetList, width, height, empty = readBoard()
    print('Input file read finished...')

    # Get permute list and count of possible boards
    plist = get_permute_list(gridAsList, dictOfBlocks, openSpaces)
    possible = nperms(plist)

    # Get list of all possible boards
    listOfDicts = generateBoards(plist, gridAsList, width)
    print('Board generation finished...')

    # Parse through possible boards, find solution
    soln, tries, listOfLazors = get_solution(
        listOfDicts, width, height, lasers, dictOfBlocks, targetList)
    print('Board solution found...')

    # Write solution to text file
    text_soln(filename, initGrid, soln, tries, possible, (time.time()-t0))
    print('Solution published...')


    # Generate solution image
    place_blocks(
        soln, 'image_files/board_images/background.png', width, height, empty)
    plot_lazor_path(listOfLazors, width, height, lasers, targetList, filename)


    # Finish up
    print('Solution image created...')
    runtime = time.time() - t0
    print('DONE! Total time: %0.5f sec' % (runtime))
    print('-=-' * 17)
