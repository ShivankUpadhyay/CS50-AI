This code implements an AI to generate crossword puzzles.

Given the structure of a crossword puzzle (i.e., which squares of the grid are meant to be filled in with a letter), and a list of words to use,
the problem becomes one of choosing which words should go in each vertical or horizontal sequence of squares.

We solve this problem as a constraint satisfaction problem. Hence we need to satisfy all the unary and binary constraints to provide a solution.

The code can be seen in action here: https://youtu.be/G8pEbAMlI4U