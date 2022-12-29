# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 21:39:17 2022

@author: dylan
"""

'''
This file contains functions for processesing the pre-processed file,
and generates a list of all possible suggested words that satisfy the 
input parameters specified in Execute_me.py
'''
import os


## Global variables. Ideally not used.
# To be fixed later.
matched_list = []
unmatched_list = []
summary_idx = []



def count(str1, str2,line_idx) :
    '''
    This function counts the number of characters already studied, in a given word.
    Studied characters are based on vocabulary associated with the MTC book that the
    student has studied (configured in Execute_me.py)
    '''
    if not str2:
        print("I do not exist")
    matched = 0; unmatched = 0;  
    for idy, xyz in enumerate(str2):        
        if(xyz in str1):
            matched +=1
        unmatched = len(str2) - matched
        if(unmatched == 0):
            summary_idx.append(line_idx)
    unmatched_list.append(unmatched)
    
def find_indices(list_to_check, max_unknown_limit):
    '''
    Finds all the indices of known characters in a given word.
    'max_unknown_limit' allows suggested words to have up to N unknown
    characters.
    '''
    items_to_find = [0]
    if(max_unknown_limit !=0):
        for i in range(max_unknown_limit):
            items_to_find.append(i+1)
    indices = []
    for idx, value in enumerate(list_to_check): # changed from '==' to 'in'
        if value in items_to_find:
            indices.append(idx)
    return indices


def find_words_to_learn(input_file,known_characters,allowed_unknown_chars):
    '''
    Main function of the file.
    Outputs the complete list of possible words to be suggested, based on all
    the input parameters specified.
    '''
    debug = False #allows generated of .txt files for debugging purpose 
    f = open(input_file, "r", encoding="utf8")
   
    lines = set(f.readlines())
    lines = [line.replace('\n','') for line in lines ]
    lines = [string for string in lines if string != ""]
    
    if(debug):
        test_output_file('setted_lines',lines)
        test_output_file('unmatched_list_after_count',str(unmatched_list))
    
    for idx,current_line in enumerate(lines):
        count(known_characters,current_line,idx)
        
    useful_indices = find_indices(unmatched_list, allowed_unknown_chars)
    list_lines = [i.strip('\n') for i in list(lines)]

    words_to_learn = [list_lines[i] for i in useful_indices]
    #print("There are %i words to learn!"%(len(words_to_learn)))
    return(words_to_learn)

def test_output_file(file_name,input_lines):
    '''
    Quick way of generating new txt files for debugging purposes.
    '''
    my_path = os.getcwd()
    parent_path = os.path.dirname(my_path)
    formatted_parent_path = r"%s/"%(parent_path)

    with open(r"%s\Word list\%s.txt"%(formatted_parent_path,file_name),"at",encoding = "utf") as test_output:
        test_output.writelines(input_lines)  