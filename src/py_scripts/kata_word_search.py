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
    #generate a transpose matrix (analogous to rotation the whole grid +90degrees counterclockwise)
    transpose_grid=np.transpose(letters0)
    return transpose_grid

def vertical_up(words,letters):
    """Check up for words encountered vertically reading from up down"""
    #rotate the grid of letters so reading from up down is analogous to reading left to right    
    letters0=transpose_letters(letters)
    letters=[''.join(x) for x in letters0]
    output_xyup,words=search(words,letters)
    #fix X,Y positions since now X becomes Y and start point(0,0) is in the bottom left corner
    for i in range(len(output_xyup)):
        output_xyup[i][1]=(output_xyup[i][1])[::-1]
        output_xyup[i][2]=(output_xyup[i][2])[::-1]
    return output_xyup,words

def vertical_down(words,letters):
    """Check for words vertically reading from down up"""
    letters0=transpose_letters(letters)
    letters=[''.join(x) for x in letters0]
    #reverse words to immitate reading from down to up analogously to horizontal_right  
    words=[x[::-1] for x in words]  
    output_xydown,words=search(words,letters)    
    #reverse words back to their normal positions 
    words=[x[::-1] for x in words] 
    #fix X,Y positions relative to the normal start point(0,0)
    for i in range(len(output_xydown)):
        for j in range(3):
            output_xydown[i][j]=output_xydown[i][j][::-1]
        output_xydown[i][1],output_xydown[i][2]=output_xydown[i][2],output_xydown[i][1]
    return output_xydown,words

def horver_output_prep(words,letters):
    """Prepareoutput list of words (found during horizontal/vertical search)"""
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
    #prepare the output words found during horizonal/vertical search and the words for diagonal search
    return words_xy,words3

def diag_gridindleft(xyl,letters): 
    """Generate indexes of letters grid for reading diagonals in parallel to  main dexter diagonal
    (from upper left corner to lower right corner of the letters grid""" 
    letters1=retrieve_input(words,letters)[1]
    xy1=copy.deepcopy(xyl)
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

def diagleft_letters(xyl,letters):
    """Generate grid of letters for diagonal search parallel to line from (0,0) to (14,14)""" 
    #using the indexes of the letters previously extracted in diag_gridindleft(xy,letters)
    xy_ind=diag_gridindleft(xyl,letters)
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

def diag_gridindright(xyr,letters): 
    """Generate indexes of letters grid for reading diagonals perpendicular to  main dexter diagonal
    (from upper left corner to lower right corner of the letters grid""" 
    letters1=retrieve_input(words,letters)[1]
    xy1=copy.deepcopy(xyr)
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

def diagright_letters(xyr,letters):
    """Generate grid of letters for diagonal search parallel to line from (0,0) to (14,14)""" 
    #using the indexes of the letters previously extracted in diag_gridindleft(xy,letters)
    xy_ind=diag_gridindright(xyr,letters)
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

def diagonal_leftup(xyl,words,letters):
    """Check for words in the grid reading parallel to main dexter (0,0) to (n,n) diagonal in forward direction 
    (equal to reading the grid of letters from upper left corner to lower right corner) """
    words1=horver_output_prep(words,letters)[1]
    letters_diag=diagleft_letters(xyl,letters)
    output_diagleftup,words2=search(words1,letters_diag)
    return words2,output_diagleftup

def diagonal_leftdown(xyl,words,letters):
    """Check for words in the grid reading parallel to main dexter (0,0) to (n,n) diagonal in backward direction 
    (equal to reading the grid of letters from lower right corner to upper left corner)"""    
    letters1=retrieve_input(words,letters)[1]
    words1=diagonal_leftup(xyl,words,letters)[0]
    #reverse words to read backwards
    words1=[x[::-1] for x in words1]
    letters_diagleftup=[]
    letters_diag=diagleft_letters(xyl,letters)
    output_diagleftdown,words2=search(words1,letters_diag)
    #reverse words to their normal condition
    words2=[x[::-1] for x in words2]
    for i in range(len(output_diagleftdown)):
        output_diagleftdown[i][0]=(output_diagleftdown[i][0])[::-1]
    return words2,output_diagleftdown

def diagonal_rightup(xyr,words,letters):
    """Check for words in the grid reading perpendicular to main dexter (0,0) to (n,n) diagonal in forward direction 
    (equal to reading the grid of letters from lower right corner to upper left corner) """
    words0=diagonal_leftdown(xyr,words,letters)[0]
    letters0=retrieve_input(words,letters)[1]
    letters=copy.deepcopy(letters0)
    words=copy.deepcopy(words0)
    letters_diag=diagright_letters(xyr,letters)
    output_diagrightup,words1=search(words,letters_diag)
    return words1,output_diagrightup

def diagonal_rightdown(xyr,words,letters):
    """Check for words in the list of diagonals in backward direction 
    (equal to reading the grid of letters from upper right corner to lower left corner)"""
    letters0=retrieve_input(words,letters)[1]
    letters=copy.deepcopy(letters0)
    xy0=copy.deepcopy(xyr)
    words1=diagonal_rightup(xyr,words,letters)[0] 
    #reverse words to read backwards
    words=[x[::-1] for x in words1]
    #letters_diagleftdown=[]
    letters_diag=diagright_letters(xy0,letters)
    output_diagrightdown,words=search(words,letters_diag)
    #reverse words to their normal condition
    words=[x[::-1] for x in words]
    for i in range(len(output_diagrightdown)):
        output_diagrightdown[i][0]=(output_diagrightdown[i][0])[::-1]
    return words,output_diagrightdown



def fix_diagxyleft(xyl,words,letters):
    """Prepare output (words found during diagonal_left search) list of words"""
    xy0,xy1,xy2=copy.deepcopy(xyl),copy.deepcopy(xyl),copy.deepcopy(xyl)
    output_diagleftup=diagonal_leftup(xy0,words,letters)[1]
    output_diagleftdown=diagonal_leftdown(xy1,words,letters)[1]
    xy_left=diag_gridindleft(xy2,letters)   
    len1=len(letters)
    key_wordsxy=[]
    for i in range(len(output_diagleftdown)):
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
        key_wordsxy.append([output_diagleftup[i][0]]+xy_positions)
    return key_wordsxy

def fix_diagxyright(xyr,words,letters):
    """Prepare output (words found during diagonal_right search) list of words"""
    xstart=-1*xyr[0][1]
    xy0,xy1,xy2=copy.deepcopy(xyr),copy.deepcopy(xyr),copy.deepcopy(xyr)
    words1=diagonal_rightdown(xyr,words,letters)[0]
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


def output(xyl,xyr,words):
    """ Output the search results into output *.txt files"""
    #prior to output sort the results acording to the input list
    #words_all=words_all[0].split(',')

    key_wordsxy=horver_output_prep(words,letters)[0]+ fix_diagxyleft(xyl,words,letters)
    key_wordsxy+=fix_diagxyright(xyr,words,letters)

    output_words=[]
    words0=retrieve_input(words,letters)[0]
    #sort output 
    for i in range(len(words0)):
        for j in range(len(key_wordsxy)):
            if words0[i] in key_wordsxy[j]:
                output_words.append(key_wordsxy[j])
    with open(output1, mode="w+") as outfile:
        for s in output_words:
            outfile.write((s[0]+':'+str(s[1:])[1:-1]+'\n'))

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
    output1="../tests/test1_output/kata_words_output.txt"
    xyl=[[0,-1]]
    xyr=[[0,0]]
    output(xyl,xyr,words)


