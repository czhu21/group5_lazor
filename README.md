# Lazor Solver

This repository contains the code necessary to solve any given 'board' from the Lazors game. The code was written in Python 3, and may or may not work on systems with Python 2.

## Getting Started

Download or clone this repository to your machine. 

### Solving

The lazor.py file contains the actual solver. bff_files contains .bff files which are plaintext representations of a given Lazors board. To solve a given board, execute the following: 

```
$ python3 lazor.py
```

You will then be asked to input the .bff file you wish to solve. For example, to solve the  yarn_5 board:

```
Welcome to the Lazor board solver!
Enter the name of the board (.bff file) you want to solve: bff_files/yarn_5.bff
```

### Output

The code will give you certain information about the solution, including a text solution, an image of the solution, how long it took to find the solution, and how many tries it took. Again, the following is the output from the yarn_5 board:

```
Input file read finished...
Board generation finished...
Board solution found...
Solution published...
Solution image created...
DONE! Total time: 35.20892 sec
```

The solution image will be found in "image_files/solution_images".


## Authors

* **Aditya Suru**
* **Casey Zhu**
* **Lincoln Kartchner**


## License

*

## Acknowledgments

* 
