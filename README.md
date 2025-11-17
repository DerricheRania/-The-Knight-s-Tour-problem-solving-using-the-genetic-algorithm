# 🧠 Project Description — Knight’s Tour Using a Genetic Algorithm + Pygame Animation

This project solves the Knight’s Tour problem using a **genetic algorithm** and **visualizes the final solution with Pygame.**

**The Knight’s Tour** is a classic chess problem where a knight **must visit all 64 squares of the board exactly once**. Instead of using traditional backtracking or heuristics, this project applies an evolutionary approach inspired by natural selection.

Each possible solution is represented as a chromosome, containing 63 genes, where each gene encodes one of the knight’s 8 possible moves. A population of random chromosomes is created, and at each generation:

The quality (fitness) of every knight path is evaluated (number of unique squares visited).

The best individuals are selected using tournament selection.

New offspring are produced through crossover and random mutations.

The population evolves until a full 64-square tour is found.

Once the genetic algorithm discovers an optimal or near-optimal tour, the solution is displayed using a Pygame animation that shows:

The chessboard

All visited squares

The order of movements

The drawn path

A moving knight icon

Real-time controls (pause, speed change, reset, quit)

This project combines artificial intelligence, evolutionary computation, and interactive visualization to demonstrate how genetic algorithms can approximate complex combinatorial problems.
