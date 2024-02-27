## C++ Implementation of the Binary Kiwi-Soto/Lueker Algorithm
The code for the implementation of the Binary Case Kiwi-Soto/Lueker algorithm are held in this branch.
See their papers here:

(Kiwi and Soto) https://www.cambridge.org/core/journals/combinatorics-probability-and-computing/article/abs/on-a-speculated-relation-between-chvatalsankoff-constants-of-several-sequences/7982322390D3236DC7BC96E42855768A

(Lueker) https://dl.acm.org/doi/10.1145/1516512.1516519


The versions are:
1. Binary-RAMOnly.cpp contains a parallelized version that works only off of RAM. It is by far the fastest one, but does not work once arrays become too large to fit in RAM. For additional explanations, see its supporting markdown document.
2. Binary-ExtnMem.cpp contains a version where vectors are written/read to/from external memory in sequential chunks. As the length of the strings increase, it becomes impossible for the vectors to fit in RAM. As such, writing to external memory becomes necessary for calculating high bounds. Doing this in sequential order (which is much faster than non-sequentially) is non-trivial, however. This verion will only work on Linux machines. For additional explanations, see its supporting markdown document.
3. Binary-KiwiSotoAlgorithm.py contains a *much* slower version of the algorithm, implemented in python. This is the easiest version to understand and write in, so we occasionally use this for testing out new ideas (e.g. implementing new symmetries). This version is not recommended for use.

NOTE: the contents of eigen-3.4.0 are NOT written by us. This is the location of the Eigen 3 library (which has been imported directly into the repository, as recommended). Eigen 3 is licensed under MPL2. See Eigen 3 documentation [here](https://eigen.tuxfamily.org/index) and source code [here](https://gitlab.com/libeigen/eigen).


We have not yet created a Makefile. To run, make sure you have a C++ compiler installed. Then, clone this repository, edit the USER PARAMETERS in each file as desired, navigate to this directory, and run `g++ -O3 -I -pthread ./eigen-3.4.0/ ./Binary-RAMOnly.cpp -o Binary-RAMOnly` and then run `./Binary-RAMOnly` (or `./Binary-RAMOnly.exe` on Windows). (Change the file name depending on which version you want to run).
**NOTE: The version that reads and writes from external memory works only on Linux systems.**
