#!/usr/bin/env python3
# kata_word_search.py
# ---------------
# by Elmira Farrar

""" The coding solution to solve a word search problem.

Problem Description:Given a text file consisting of a list of words, and a series of rows 
of single-character lists representing the word search grid, this program should search for 
the words in the grid and return a set of x,y coordinates for each word found.

*This solution finds only the words which can be encountered in the grid of letters 
either horizontally or vertically.

Assumptions: 
1.The search grid of letters is square.
2.Both words and letters in the grid are CAPITAL (Uppercase)
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

def horizontal_left(words,letters):
    """Check for words encountered horizontally reading from left to right"""
    output_xyleft,words=search(words,letters)
    return output_xyleft,words

def horizontal_right(words,letters):
    """Check for words horizontally reading from right to left"""

    #the words are reversed, thats how one would encounter them while reading from right to left
    words=[x[::-1] for x in words]
    output_xyright,words=search(words,letters) 

    #reverse words into their normal position
    words=[x[::-1] for x in words]
    #reverse X positons (since X indexing starts from left)
    for i in range(len(output_xyright)):
        output_xyright[i][0]=output_xyright[i][0][::-1]
        output_xyright[i][1],output_xyright[i][2]=output_xyright[i][2],output_xyright[i][1]
    return output_xyright,words

def transpose_letters(letters):
    """Rotation 90 degrees clockwise of the grid of letters to read letters vertically""" 
    letters0=np.array([list(c) for c in letters])
    #generate a transpose matrix (analogous to rotation the whole grid +90degrees)
    transpose_grid=np.transpose(letters0)
    return transpose_grid

def vertical_up(words,letters):
    """Check for words vertically reading from up down"""
    #rotate the grid of letters so reading from up down is analogous to reading left to right    
    letters0=transpose_letters(letters)
    letters=[''.join(x) for x in letters0]
    output_xyup,words=search(words,letters)
    #fix X,Y positions since X,Y always start in upper left conner
    for i in range(len(output_xyup)):
        output_xyup[i][1]=(output_xyup[i][1])[::-1]
        output_xyup[i][2]=(output_xyup[i][2])[::-1]
    return output_xyup,words

def vertical_down(words,letters):
    """Check for words vertically reading from up down"""
    letters0=transpose_letters(letters)
    letters=[''.join(x) for x in letters0]
    #reverse words to immitate reading from down to up analogously to horizontal_right  
    words=[x[::-1] for x in words]  
    output_xydown,words=search(words,letters)    
    #reverse words back to their normal positions 
    words=[x[::-1] for x in words] 
    #reverse X positons (since X position indexing always starts from the left (0,0))
    for i in range(len(output_xydown)):
        for j in range(3):
            output_xydown[i][j]=output_xydown[i][j][::-1]
        output_xydown[i][1],output_xydown[i][2]=output_xydown[i][2],output_xydown[i][1]
    return output_xydown,words

def output_prep(words,letters):
    """ Preparing output list of words"""
    words1,letters1=retrieve_input(words,letters)
    if len(words1)>0:
        words_xy0,words0=horizontal_left(words1,letters)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    #if horizontal_left search didn't cover all words continue other searches,..
    if len(words0)>0:
        words_xy1,words1=horizontal_right(words0,letters)
    if len(words1)>0:
        words_xy2,words2=vertical_up(words1,letters)
    if len(words2)>0:
        words_xy3,words3=vertical_down(words2,letters)

    words_xy=words_xy0+words_xy1+words_xy2+words_xy3
    for i in range(len(words_xy)):
        m=words_xy[i]
        m0=[]
        if m[1][1]==m[2][1]:
            c0=m[1][0]
            c1=m[2][0]
            if c1>c0:
                c=list(range(c0,c1+1))
            else:
                c=(list(range(c1,c0+1)))[::-1]
            for j in range(len(c)):
                m0.append([c[j],m[1][1]])
        
        elif m[1][0]==m[2][0]:
            c0=m[1][1]
            c1=m[2][1]
            if c1>c0:
                c=list(range(c0,c1+1))
            else:
                c=(list(range(c1,c0+1)))[::-1]
            for j in range(len(c)):
                m0.append([m[1][0],c[j]])
        m0=[tuple(x) for x in m0]
        words_xy[i]=[m[0]]+m0
        m0=[]
    #prepare the output words found during horizonal/vertical search and the words for future diagonal search
    return words_xy,words3

def output():
    """ Output the search results into output *.txt files"""
    words_xy,diag_words=output_prep(words,letters)
    with open(output1, mode="w+") as outfile1:
        for s in words_xy:
            outfile1.write((s[0]+':'+str(s[1:])[1:-1]+'\n'))
    with open(output2, mode="w+") as outfile2:
        outfile2.write(','.join(diag_words))

if __name__ == '__main__':
    #run the main function
    input1="../input/kata_words_input.txt"  
    with open(input1, "r") as filename1: 
        #get the words to be found from the input:
        words = filename1.read().splitlines()
    input2="../input/kata_letters_input.txt"  
    with open(input2, "r") as filename2: 
        #get the letters grid from the input:
        letters = filename2.read().splitlines()
    # set up output files
    output1="../tests/intermediate_outputs/kata_words_output.txt"
    output2="../tests/intermediate_outputs/kata_words_diag_input.txt"
    output()
    #print('haha')

