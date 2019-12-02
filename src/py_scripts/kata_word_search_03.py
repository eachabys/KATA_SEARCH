#!/usr/bin/env python3
# kata_word_search.py
# ---------------
# by Elmira Farrar

""" The coding solution to solve a word search problem.

Problem Description:Given a text file consisting of a list of words, and a series of rows 
of single-character lists representing the word search grid, this program should search for 
the words in the grid and return a set of x,y coordinates for each word found.

*This solution finds only the words which can be encountered in the grid of letters 
diagonally in perpendicular to the dexter diagonal (from upper left corner or XY[0,0] 
to lower right corner or XY[-1,-1].

Assumptions: 
1.The search grid of letters is square.
2.Both words and letters in the grid are Capital ( Uppercase)
3.No punctuation or other characters are present in the input data
4.No Duplicates of words are present
5.Each word will be present in the grid fo letters
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

def diag_gridindright(xy,letters): 
    """Generate indexes of letters grid for reading diagonals perpendicular to  main dexter diagonal
    (from upper left corner to lower right corner of the letters grid""" 

    letters1=retrieve_input(words,letters)[1]
    xy1=copy.deepcopy(xy)
    len1=len(letters)
    for i in range(1,len1):
        m=[]
        #each position diagonally is shifted 1 position down or right relative to the previous one
        if len(xy1)<2:
            k=len(xy1[-1])-1
        else:
            #going down from XY[0,0] means each next Y position becomes more positive 
            k=len(xy1[-1])
        for j in range(i+1):
            #while X position starts at 0 and goes one position to the right or +1
            m.append([k,j])
            k-=1
        xy1.append(m)
    #xy1 covers diagonals left of main (longest) diagonal of the letters grid, including the main diagonal
    #xy_cp covers the righ portion of the grid to the right from the main dexter (longest) diagonal
    xy_cp=copy.deepcopy(xy1)[:-1]

    for i in range(1,len(xy_cp)):
        m=xy_cp[i]
        for j in range(len(m)):
            m[j][0]=len1-m[j][0]-1
            m[j][1]=len1-m[j][1]-1
        xy_cp[i]=m[::-1]
    #remove the first element of each list since it's' only one character, (not a word)
    xy1.pop(0)
    xy_cp.pop(0)
    xy_cp=xy_cp[::-1]
    xy1+=xy_cp
    return xy1

def diag_letters(xy,letters):
    """Generate grid of letters for diagonal search parallel to line from (0,0) to (14,14)""" 
    #using the indexes of the letters previously extracted in diag_gridindleft(xy,letters)
    xy_ind=diag_gridindright(xy,letters)
    letters=retrieve_input(words,letters)[1]  
    letters_diaggrid=[]
    for i in range(len(xy_ind)):
        v=[]
        z=xy_ind[i]
        for j in range(len(z)):
            v.append(letters[z[j][1]][z[j][0]])
        v=''.join(v)
        letters_diaggrid.append(v)
    return letters_diaggrid

def diagonal_rightup(xy,words,letters):
    """Check for words in the list of diagonals in forward direction 
    (equal to reading the grid of letters from lower right corner to upper left corner) """
    words0,letters0=retrieve_input(words,letters)
    letters=copy.deepcopy(letters0)
    words=copy.deepcopy(words0)
    #letters_diagrightdown=[]
    letters_diag=diag_letters(xy,letters)
    output_diagrightup,words1=search(words,letters_diag)
    return words1,output_diagrightup

def diagonal_rightdown(xy,words,letters):
    """Check for words in the list of diagonals in backward direction 
    (equal to reading the grid of letters from upper right corner to lower left corner)"""
    letters0=retrieve_input(words,letters)[1]
    letters=copy.deepcopy(letters0)
    xy0=copy.deepcopy(xy)
    words1=diagonal_rightup(xy,words,letters)[0] 
    #reversing words to read in opposite direction
    words=[x[::-1] for x in words1]
    #letters_diagleftdown=[]
    letters_diag=diag_letters(xy0,letters)
    output_diagrightdown,words=search(words,letters_diag)
    #reversing words to their normal condition
    words=[x[::-1] for x in words]
    for i in range(len(output_diagrightdown)):
        output_diagrightdown[i][0]=(output_diagrightdown[i][0])[::-1]
    return words,output_diagrightdown

def fix_diagxyright(xy):
    """ Preparing output list of words"""
    xstart=-1*xy[0][1]

    xy0,xy1,xy2=copy.deepcopy(xy),copy.deepcopy(xy),copy.deepcopy(xy)
    words1=diagonal_rightdown(xy,words,letters)[0]
    output_diagrightup=diagonal_rightup(xy0,words,letters)[1]
    output_diagrightdown=diagonal_rightdown(xy1,words,letters)[1]
    xy_right=diag_gridindright(xy2,letters)
    key_wordsxy=[]
    for i in range(len(output_diagrightup)):
        k=output_diagrightup[i][0]
        diag_rowxy1,diag_rowxy2=output_diagrightup[i][1],output_diagrightup[i][2]       
        diag_rowxy=diag_rowxy1[1]
        diag_row=[]
        for j in range(diag_rowxy1[0],diag_rowxy2[0]+1):
            diag_row.append(xy_right[diag_rowxy1[1]][j])
        diag_row=[tuple(x) for x in diag_row]
        key_wordsxy.append([output_diagrightup[i][0]]+diag_row)
        diag_row=[]

    for i in range(len(output_diagrightdown)):
        k=output_diagrightdown[i][0]
        diag_rowxy1,diag_rowxy2=output_diagrightdown[i][1],output_diagrightdown[i][2]       
        diag_rowxy=diag_rowxy1[1]
        diag_row=[]
        for j in range(diag_rowxy1[0],diag_rowxy2[0]+1):
            diag_row.append(xy_right[diag_rowxy1[1]][j])
        diag_row=[tuple(x) for x in diag_row[::-1]]   
        key_wordsxy.append([output_diagrightdown[i][0]]+diag_row)
        diag_row=[]    
    return key_wordsxy

def output(xy,words,words_all):
    """ Output the search results into output *.txt files"""
    #prior to output sort the results acording to the input list
    words_all=words_all[0].split(',')

    key_wordsxy=fix_diagxyright(xy)
    with open(output1, "r") as filename: 
        #get the data from the output(contains previous outputs (horizontal,vertical,... searches):
        output_prev= filename.read().splitlines()
    output_prev=[x.split(':') for x in output_prev]+key_wordsxy
    outputx=[]
    #sort output 
    for i in range(len(words_all)):
        for j in range(len(output_prev)):
            if words_all[i] in output_prev[j]:
                outputx.append(output_prev[j])

    with open(output1, mode="w+") as outfile:
        for s in outputx:
            if len(s)<3:
                outfile.write((s[0]+':'+s[1]+'\n'))
            else:
                outfile.write((s[0]+':'+str(s[1:])[1:-1]+'\n'))

if __name__ == '__main__':
    #run the main function

    #retrieve the input data
    input_file1="../tests/intermediate_outputs/kata_words_diag_input2.txt"  
    with open(input_file1, "r") as filename1: 
        #get the words to be found from the input:
        words = filename1.read().splitlines()    
    input_file2="../input/kata_letters_input.txt"  
    with open(input_file2, "r") as filename2: 
        #get the data from the input:
        letters = filename2.read().splitlines()
    input_file3="../input/kata_words_input.txt"  
    with open(input_file3, "r") as filename3: 
        #get the data from the input:
        words_all= filename3.read().splitlines()
    len1=len(letters)
    xy=[[0,0]]
    output1="../tests/final_output/kata_words_output.txt"
    output(xy,words,words_all)
    
