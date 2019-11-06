# Software Carpentry
# Lazor Project
# Group 5


def text_soln(filename, initGrid, soln, tries, runtime):
    fname = filename.split('.')[0]
    solnGrid = initGrid
    for i in soln.keys():
        solnGrid[i[1]][i[0]] = soln[i]

    f = open(fname + '_solution.txt', 'w')

    f.write('Software Carpentry Lazor Project - Group 5\n')
    f.write('Puzzle: ' + fname + '\n \n')

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

    f.write('\nTo get this solution, %d guesses were made, taking %1.5f seconds.\n' % (tries, runtime))
    f.write('Thanks for playing!\n')


if __name__ == "__main__":
    pass
