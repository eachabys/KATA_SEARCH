#!/usr/bin/env python3
# kata_word_search.py
# ---------------
# by Elmira Farrar

""" The coding solution to solve a word search problem.

Problem Description:Given a text file consisting of a list of words, and a series of rows 
of single-character lists representing the word search grid, this program should search for 
the words in the grid and return a set of x,y coordinates for each word found.

*This solution finds only the words which can be encountered in the grid of letters 
diagonally in parallel to the dexter diagonal (from upper left corner or XY[0,0] 
to lower right corner or XY[-1,-1].

Assumptions: 
1.The search grid of letters is square.
2.Both words and letters in the grid are Capital ( Uppercase)
3.No punctuation or other characters are present in the input data
4.No Duplicates of words are present
5.Each word will be present in the grid
6.No word in the input is a subset of another word. So no words like ONE, BONE can be in the list of words
7.Words at least 2 letters"""

import numpy as np
import copy

def retrieve_input(words,letters):
    """Retrieve input data: words to be found and letters"""
    words=words[0].split(',')
    for i in range(len(letters)):
        letters[i]=letters[i].replace(',','')
    return words,letters

def search(words,letters):
    """Search for words in a list of sublists of letters"""
    output_xy=[]
    c=[]
    x=0
    search_stop= False
    for i in range(len(letters)):
        for k in range(len(words)):
            if words[k] in letters[i]:
                m=len((letters[i].split(words[k]))[0])
                output_xy.append([words[k], [m,i],[m+len(words[k])-1,i]])
                c.append(words[k])
                x+=1
        #update the words list, since if any particular word is found it can be removed from the search 
        if x>0:
            for j in range(len(c)):
                words1=copy.deepcopy(words)
                words1.remove(c[j])
                words=copy.deepcopy(words1)
            if len(words)<1:
                search_stop= True
                break
            c=[]
            x=0
        if search_stop: 
            break                    
    return output_xy,words  

def diag_gridindleft(xy,letters): 
    """Generate indexes of letters grid for reading diagonals in parallel to  main dexter diagonal
    (from upper left corner to lower right corner of the letters grid""" 
    letters1=retrieve_input(words,letters)[1]
    xy1=copy.deepcopy(xy)
    for i in range(1,len(letters)):
        m=[]
        #each position diagonally is shifted 1 position up or right relative to the previous one
        if len(xy1)<2:
            k=len(xy1[-1])
        else:
            #going up from XY[0,-1] means each next Y position becomes more negative -1 
            k=len(xy1[-1])+1
        for j in range(i+1):
            #while X position starts at 0 and goes one position to the left or +1
            m.append([j,-k])
            k-=1
        #combine all  
        xy1.append(m)
    #xy1 covers diagonals left of main dexter (longest) diagonal of the letters grid
    #xy_cp covers the righ portion of the grid to the right from the main dexter (longest) diagonal
    xy_cp=copy.deepcopy(xy1[:-1])
    xy_cp[0]=(xy_cp[0])[::-1]
    for i in range(1,len(xy_cp)):
        n=xy_cp[i]
        for j in range(len(n)):
            #this list starts from position XY[-1,0].It is reverse  or YX positions of the xy list
            n[j]=(n[j])[::-1]
        xy_cp[i]=n
    #remove the first element of each list since it's' only one character, (not a word)
    xy1.pop(0)
    xy_cp.pop(0)
    xy_cp=xy_cp[::-1]
    xy1+=xy_cp
    return xy1

def diag_letters(xy,letters):
    """Generate grid of letters for diagonal search parallel to line from (0,0) to (14,14)""" 
    #using the indexes of the letters previously extracted in diag_gridindleft(xy,letters)
    xy_ind=diag_gridindleft(xy,letters)
    letters=retrieve_input(words,letters)[1]  
    letters_diaggrid=[]
    for i in range(len(xy_ind)):
        v=[]
        z=xy_ind[i]
        for j in range(len(z)):
            v.append(letters[z[j][0]][z[j][1]])
        v=''.join(v)
        letters_diaggrid.append(v)
    return letters_diaggrid

def diagonal_leftup(xy,words,letters):
    """Check for words in the list of diagonals in forward direction 
    (equal to reading the grid of letters from upper left corner to lower right corner) """
    words1=retrieve_input(words,letters)[0]
    letters_diag=diag_letters(xy,letters)
    output_diagleftup,words2=search(words1,letters_diag)
    return words2,output_diagleftup

def diagonal_leftdown(xy,words,letters):
    """Check for words in the list of diagonals in backward direction 
    (equal to reading the grid of letters from lower right corner to upper left corner)"""
    #reversing words to read in opposite direction
    letters1=retrieve_input(words,letters)[1]
    words1=diagonal_leftup(xy,words,letters)[0]
    words1=[x[::-1] for x in words1]

    letters_diagleftup=[]
    letters_diag=diag_letters(xy,letters)
    output_diagleftdown,words2=search(words1,letters_diag)
    #reversing words to their normal condition
    words2=[x[::-1] for x in words2]
    for i in range(len(output_diagleftdown)):
        output_diagleftdown[i][0]=(output_diagleftdown[i][0])[::-1]
    return words2,output_diagleftdown

def fix_diagxyleft(xy,words,letters):
    """ Preparing output list of words"""
    xy0,xy1,xy2=copy.deepcopy(xy),copy.deepcopy(xy),copy.deepcopy(xy)
    output_diagleftup=diagonal_leftup(xy0,words,letters)[1]
    output_diagleftdown=diagonal_leftdown(xy1,words,letters)[1]
    xy_left=diag_gridindleft(xy2,letters)   
    len1=len(letters)
    key_words,key_words1,key_wordsxy,key_wordsxy1=[],[],[],[]
    for i in range(len(output_diagleftdown)):
        key_words.append(output_diagleftdown[i][0])
        diag_rowxy1,diag_rowxy2=output_diagleftdown[i][1],output_diagleftdown[i][2]
        diag_row,diag_rowstart,diag_rowend=diag_rowxy1[1],diag_rowxy1[0],diag_rowxy2[0]
        xy_positions=xy_left[diag_row][diag_rowstart:diag_rowend+1]
        for j in range(len(xy_positions)):
            if xy_positions[j][1]<0:
                xy_positions[j][1]=len1+xy_positions[j][1]
                xy_positions[j][0],xy_positions[j][1]=xy_positions[j][1],xy_positions[j][0]
            if xy_positions[j][0]<0:
                xy_positions[j][0],xy_positions[j][1]=xy_positions[j][1],xy_positions[j][0]
                xy_positions[j][1]=len1+xy_positions[j][1]
            xy_positions[j]=(tuple(xy_positions[j]))
        key_wordsxy.append([output_diagleftdown[i][0]]+xy_positions[::-1])
    for i in range(len(output_diagleftup)):
        key_words1.append(output_diagleftup[i][0])
        diag_rowxy1,diag_rowxy2=output_diagleftup[i][1],output_diagleftup[i][2]
        diag_row,diag_rowstart,diag_rowend=diag_rowxy1[1],diag_rowxy1[0],diag_rowxy2[0]
        xy_positions=xy_left[diag_row][diag_rowstart:diag_rowend+1]
        for j in range(len(xy_positions)):
            xy_positions[j]=(xy_positions[j])[::-1]
            if xy_positions[j][0]<0:
                xy_positions[j][0]=len1+xy_positions[j][0]
            if xy_positions[j][1]<0:
                xy_positions[j][1]=len1+xy_positions[j][1]
            xy_positions[j]=(tuple(xy_positions[j]))
        key_wordsxy1.append([output_diagleftup[i][0]]+xy_positions)
    return key_wordsxy+key_wordsxy1

def output(xy):
    """ Output the search results into output *.txt files"""
    words1=diagonal_leftdown(xy,words,letters)[0]
    key_wordsxy=fix_diagxyleft(xy,words,letters)
    with open(output1, mode="a") as outfile:
        for s in key_wordsxy:
            outfile.write((s[0]+':'+str(s[1:])[1:-1]+'\n'))
    with open(output2, mode="w+") as outfile:
        outfile.write(','.join(words1))

if __name__ == '__main__':
    #run the main function

    #read input data
    input_file1="../tests/intermediate_outputs/kata_words_diag_input.txt"  
    with open(input_file1, "r") as filename1: 
        #get the words to be found from the input:
        words = filename1.read().splitlines()

    input_file2="../input/kata_letters_input.txt"  
    with open(input_file2, "r") as filename2: 
        #get the grid of letters from the input:
        letters = filename2.read().splitlines()
    # set up an output files  
    output1="../tests/intermediate_outputs/kata_words_output.txt"
    output2="../tests/intermediate_outputs/kata_words_diag_input2.txt"
    xy=[[0,-1]]
    output(xy)

    
