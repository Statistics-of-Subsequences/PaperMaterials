## Implementations of the Kiwi-Soto/Lueker Algorithms
This repository contains implementations of the algorithms discussed in the paper "Improved Lower Bounds on the Expected Length of Longest Common Subsequences." The algorithms are adapted from papers by Kiwi and Soto as well as Lueker.
See the papers here:

(Kiwi and Soto) https://www.cambridge.org/core/journals/combinatorics-probability-and-computing/article/abs/on-a-speculated-relation-between-chvatalsankoff-constants-of-several-sequences/7982322390D3236DC7BC96E42855768A

(Lueker) https://dl.acm.org/doi/10.1145/1516512.1516519

(ours) https://arxiv.org/abs/2407.10925


This directory contains multiple different implementations of the algorithms. Each version is described below. The bolded versions have an additional supporting document that gives more detail into additional optimizations.

Binary Versions
1. **Binary-RAMOnly.cpp** contains a parallelized version of the binary case (two strings, binary alphabet only) that works only off of RAM. It is by far the fastest one, but does not work once arrays become too large to fit in RAM. This version should be used for smaller string lengths (generally, <=15, though it depends on the specs of the machine it is run on). For additional explanations, see its supporting markdown document.
  
2. **Binary-ExtnMem.cpp** contains a version for the binary case where vectors are written/read to/from external memory in sequential chunks. As the length of the strings increase, it becomes impossible for the vectors to fit in RAM. As such, writing to external memory becomes necessary for calculating high bounds. Doing this in sequential order (which is much faster than non-sequentially) is non-trivial, however. This version should be used for larger string lengths (generally, >15), as a typical computer does not have the RAM necessary to run the code for large length strings. For additional explanations, see its supporting markdown document. **This verion will only work on Linux machines.**
  
3. Binary-KiwiSotoAlgorithm.py contains a *much* slower version of the binary algorithm, implemented in python. This is the easiest version to understand and write in, so we occasionally use this for testing. This version is not recommended for use.
   
 

General Versions

1. **ParallelMulti.cpp** contains a parallelized version of the generalized case (any number of strings, any alphabet size) that works only off of RAM. For additional explanations, see its supporting markdown document.
   
2. Multi-KiwiSotoAlgorithm.py contains a *much* slower version of the general algorithm, implemented in python. This is the easiest version to understand and write in, so we occasionally use this for testing. This version is not recommended for use.

NOTE: the contents of eigen-3.4.0 are NOT written by us. This is the location of the Eigen 3 library (which has been imported directly into the repository, as recommended). Eigen 3 is licensed under MPL2. See Eigen 3 documentation [here](https://eigen.tuxfamily.org/index) and source code [here](https://gitlab.com/libeigen/eigen).

## How to run
All code necessary should be included in this repository. First, download all files in this repository (if you downloaded the .zip file: extract it, and it should contain everything, this document included).

Before running a program, you may want to look at its supporting Markdown document and the `PARAMETERS` section at the top of the program. The parameters here determine what lower bound is calculated and what resources (memory, threads) are used to do so. At the moment, these variables must be edited in the program itself; they are not command-line parameters. Keep in mind that these algorithms are highly exponential, creating and modifying multiple vectors with $alphabet\_ size^{string\_ count*length}$ elements. Be careful not to set alphabet_size, string_count, or length too large.

To compile a program, open the terminal where one of the C++ files is saved (this directory), and run

`g++ -O3 -pthread -I #EIGEN_PATH# ./#FILENAME#.cpp -o #FILENAME#`

where `#EIGEN_PATH#` should replaced by the path to the Eigen C++ library version 3.4.0 (if you downloaded this repository without modification, you should replace `#EIGEN_PATH#` with `./eigen-3.4.0/`), and `#FILENAME#` is either `Binary-RAMOnly`, `Binary-ExtnMem`, or `ParallelMulti`.

This compilation command assumes you have g++ installed, but a slightly modified command should work with gcc or any other standard C++ compiler. The compiler should also be added to your system's PATH if you experience issues. **Note: Binary-ExtnMem will only work on Linux machines.**

This should have created the file `#FILENAME#` (or `#FILENAME#.exe` on Windows) in the same folder the command was ran. With the terminal still in this folder, run

`./#FILENAME#` (or `.\#FILENAME#.exe` on Windows)

to run the algorithm.

Please note: these files have only been tested on Linux and Windows systems. They should still work on Mac systems, but we cannot guarantee it with certainty.
