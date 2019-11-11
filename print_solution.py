# Software Carpentry
# Lazor Project
# Group 5

from copy import deepcopy
import datetime


def text_soln(filename, initGrid, soln, tries, possible, runtime):
    fname = filename.split('.')[0]

    solnGrid = deepcopy(initGrid)
    for i in soln.keys():
        solnGrid[i[1]][i[0]] = soln[i]

    f = open(fname + '_solution.txt', 'w')

    f.write('Software Carpentry Lazor Project - Group 5\n')
    f.write(str(datetime.datetime.now()))
    f.write('\nPuzzle: ' + fname + '\n \n')

    f.write('Given board: \n')
    for i in initGrid:
        line = ' '.join(i)
        line = line + '\n'
        f.write(line)

    f.write('\nSolution board: \n')
    for i in solnGrid:
        line = ' '.join(i)
        line = line + '\n'
        f.write(line)

    f.write('\n%d guesses were made out of a possible %d boards.\n' % (tries, possible))
    f.write('Finding this solution took %f seconds.\n' % (runtime))
    f.write('Thanks for playing!\n')


if __name__ == "__main__":
    pass
