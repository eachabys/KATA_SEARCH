# KATA_SEARCH
Solution to Kata_word_search problem

The problem description can be found [here](https://github.com/PillarTechnology/kata-word-search)

Given two text files in the Input directory consisting of a list of words, and a series of rows of single-character lists representing the word search grid, the solution searches for the words in the grid of letters and returns a set of x,y coordinates for each letter of a word found.

### Input

The first line of the text file (kata_words_input.txt) consists of the list of words to be found. 
  
    BONES,KHAN,KIRK,SCOTTY,SPOCK,SULU,UHURA

The second text file (kata_letters_input.txt) represents a grid of letters, corresponding to the letters grid below. It will always be square, and all words in the list will always be present in the grid. Words may be located horizontally, vertically, diagonally, and both forwards and backwards. Words will never "wrap" around the edges of the grid.

The following is an example of the format of the input file (kata_letters_input.txt) :
  
    U,M,K,H,U,L,K,I,N,V,J,O,C,W,E
    L,L,S,H,K,Z,Z,W,Z,C,G,J,U,Y,G
    H,S,U,P,J,P,R,J,D,H,S,B,X,T,G
    B,R,J,S,O,E,Q,E,T,I,K,K,G,L,E
    A,Y,O,A,G,C,I,R,D,Q,H,R,T,C,D
    S,C,O,T,T,Y,K,Z,R,E,P,P,X,P,F
    B,L,Q,S,L,N,E,E,E,V,U,L,F,M,Z
    O,K,R,I,K,A,M,M,R,M,F,B,A,P,P
    N,U,I,I,Y,H,Q,M,E,M,Q,R,Y,F,S
    E,Y,Z,Y,G,K,Q,J,P,C,Q,W,Y,A,K
    S,J,F,Z,M,Q,I,B,D,B,E,M,K,W,D
    T,G,L,B,H,C,B,E,C,H,T,O,Y,I,K
    O,J,Y,E,U,L,N,C,C,L,Y,B,Z,U,H
    W,Z,M,I,S,U,K,U,R,B,I,D,U,X,S
    K,Y,L,B,Q,Q,P,M,D,F,C,K,E,A,B

### Tests

This directory contains the [final output](https://github.com/eachabys/KATA_SEARCH/tree/master/tests/final_output) of the solution to the kata-word_problem. 
The output of the program is the location of each word found, each on a separate line. The location will be represented as a series of x,y coordinates, where both x and y start at zero at the top-left of the grid. From this position both x and y will increase, i.e. they will never be negative.

Given the example input above, the following output can be found in the directory tests/final_output, which represents the output to the word_search problem.  

    BONES: (0,6),(0,7),(0,8),(0,9),(0,10)
    KHAN: (5,9),(5,8),(5,7),(5,6)
    KIRK: (4,7),(3,7),(2,7),(1,7)
    SCOTTY: (0,5),(1,5),(2,5),(3,5),(4,5),(5,5)
    SPOCK: (2,1),(3,2),(4,3),(5,4),(6,5)
    SULU: (3,3),(2,2),(1,1),(0,0)
    UHURA: (4,0),(3,1),(2,2),(1,3),(0,4)

In addition to the final output presented above, the tests directory contains intermediate outputs, since the program was broken into 3 parts for ease. 

### SRC

The solution to this problem was written in Python v.3.6. It was broken into 3 parts which can be found in the [py_scripts](https://github.com/eachabys/KATA_SEARCH/tree/master/src/py_scripts) subdirectory of the [src](https://github.com/eachabys/KATA_SEARCH/tree/master/src) directory. Each python script performs a search in different directions:
kata_word_search_01.py (performs only horizontal and vertical searches)
kata_word_search_02.py (performs only diagonal search in the direction parallel to the main dexter diagonal)
kata_word_search_03.py (performs only diagonal search in the direction perpendicular to the main dexter diagonal)

To run the solutions one can use the command line and the script provided in the src directory, 

    sh main_command.sh

which would run the python scripts one by one.
The python scripts are supposed to run one by one, not simultaneously, since each script reduces the amount of the following searches. 
