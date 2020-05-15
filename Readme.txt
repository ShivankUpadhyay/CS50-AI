In this problem we represent the "Knights and Knaves" puzzles using propositional logic, such that an AI running a model-checking algorithm could solve these puzzles for us.

In a Knights and Knaves puzzle, the following information is given: Each character is either a knight or a knave. A knight will always tell the truth: if knight states a sentence, then that sentence is true. Conversely, a knave will always lie: if a knave states a sentence, then that sentence is false.

The objective of the puzzle is, given a set of sentences spoken by each of the characters, determine, for each character, whether that character is a knight or a knave.

We have two files:

1. logic.py- this file defines several classes for different types of logical connectives. It also has a model-check that takes a knowledge base and a query. 
2. puzzle.py- this file loops over all puzzles, and uses model checking to compute, given the knowledge for that puzzle, whether each character is a knight or a knave, printing out any conclusions that the model checking algorithm is able to make.

The program can be seen in action here: https://youtu.be/4gJI1Ltqph8