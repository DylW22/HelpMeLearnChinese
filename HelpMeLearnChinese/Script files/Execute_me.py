# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 16:53:42 2022

@author: dylan
"""

import csv
import random
import dragonmapper.hanzi
from cedict_utils.cedict import CedictParser
from collections import Counter
import shutil
import find_words 
import data_conditioning as condition
import os
import sys

############################ INPUTS ##################################
    
input_file_name = 'pleco_dangdai.tsv'
# Main input file, based on vocabulary studied in NTNU MTC's textbook.
# Currently only has books 1-5 (of possible 6)

character_type = "traditional"
# Choose which character set to learn. Only traditional characters currently implemented.
highest_studied_MTC_book = 2
# Choose the highest book you have studied in MTC
# Future update to include studied chapters.


data_conditioning = True 
# Cleans and formats vocabulary from Taiwans' official list.

dictionary_list = True
# Allow suggestion of words from dragonmapper ChineseDictionary

TOCFL_list = True 
# Allow suggestion of words from CHOSEN TOCFL list

textbook_list = True

################## Word suggestion settings
max_unknown_chars = 0 
#Maximum unknown characters, if set to 0, words will only be suggested if all characters are known

your_TOCFL_level = 1
# Choose your TOCFL level [1-5] to define what possible words can be suggested

n_suggest_words = 5 
# How many daily words would you like to be added

days_selected = 3
# How many days worth of N_suggest_words would you like to be added to your list
 
########

##############################################################################
## Dictionary 
# Suggests words from dragonmapper dictionary of minimum N characters
min_char_length = 2 

# Suggests word from dragonmapper dictionary of maximum N characters
max_char_length = 12 

# NOTE: Dictionary suggested words do not currently allow unknown characters.
# Future update could implement this.

############################# Outputs #########################################

dest_file_name = 'pleco_dangdai_plus.tsv' #Output file to be used in Pleco

################## Suggest words from TOCFL Suggested Word List
#Debugging files
raw_output_file1 = "test_output_raw"
raw_output_file2 = "test_output_processed"
#######################################################################

########################## Updates ###########################################

## Updates to include removing words already been suggested.

##############################################################################




my_path = os.getcwd()
parent_path = os.path.dirname(my_path)
formatted_parent_path = r"%s/"%(parent_path)
input_file_directory = formatted_parent_path

highest_TOCFL_level = 5 
# Highest current level TOCFL offers, currently highest is level 5.
# Data sourced from https://tw.org/
# I recently came across an even more official list of vocabulary: https://tocfl.edu.tw/index.php/exam/
# to be implemented at a later date

# Global variables, to be removed at a later date
known_books = []
filtered_words_to_learn = []   

if(highest_studied_MTC_book >= 5):
    highest_studied_MTC_book = 5
elif(highest_studied_MTC_book <= 0):
    highest_studied_MTC_book = 1
    
for i in range(1,5+1):
    if(i <= highest_studied_MTC_book):
        known_books.append("Book %i"%i)


n_books = len(known_books)
raw_textbook_words_list = []
    
output_full_path = r"%s"%(input_file_directory + dest_file_name)
path=shutil.copy2(r"%s/%s"%(input_file_directory, input_file_name),output_full_path)


if('csv' in input_file_name):
    delim = ","
  #  print("file = csv")
elif('tsv' in input_file_name):
    delim = "\t"
   # print("file = csv")
else:
    delim = ""

def OpenFile(file_name,encoding_input,save):
    '''
    Opens files.
    '''
    output_list = []
    if(save):
        param = "wt"
    else:
        param = "r"
    with open(file_name,param,encoding = encoding_input) as csvfile: 
        tsvfile = csv.reader(csvfile,delimiter = delim)
        for indx, line in enumerate(tsvfile):
            output_list.append(line[0])
    return output_list

    
def searchDict(required_word,entries):
    '''
    This function searches the dragonmapper dictionary module for a specified word.
    Outputs the meaning, methods of writing it in pinyin.
    '''
    for idx, f in enumerate(entries):
        if(character_type == "traditional"):
            word = entries[idx].traditional
            if(word == required_word):
                meaning = entries[idx].meanings
                pinyin = dragonmapper.hanzi.to_pinyin(word)
                pinyin2 = entries[idx].pinyin
        else:
            print("Do something here later on.")
    return meaning, pinyin, pinyin2

def generate_dictionary_lists(input_entries):
    '''
    This function generates the complete list of possible words to be suggested.
    '''
    
    dict_available_word_list = []
    my_pinyin_list = []
    my_meanings_list = []
    my_pinyin_list2 = []

    for idx2,e in enumerate(input_entries):
        truths = []
        has_all = True
    
        if(character_type == "traditional"):
            word = entries[idx2].traditional
        else:
            word = entries[idx2].simplified
        if(len(word) >= min_char_length) and len(word) <= max_char_length:
            for j in range(0,len(word)):
                truth = word[j] in known_unique_textbook_characters
                truths.append(truth)
           
            for truth in truths:
                has_all = has_all and truth
            if(has_all):
                if word not in raw_textbook_words_list:
                    dict_available_word_list.append(word)
                    my_pinyin_list.append(dragonmapper.hanzi.to_pinyin(word))
                    my_meanings_list.append(entries[idx2].meanings)               
                    my_pinyin_list2.append(entries[idx2].pinyin)  

    return dict_available_word_list, my_pinyin_list, my_meanings_list

raw_textbook_words_list = OpenFile(r"%s/%s"%(input_file_directory,input_file_name),"utf8",False)   

## finds the index of known chapters within the MTC books
index_known_chapter_titles = [ind for ind, title in enumerate(raw_textbook_words_list) if any(x in title for x in known_books)]

## finds the index of all chapters within the MTC books
index_all_chapter_titles = [ind for ind, title in enumerate(raw_textbook_words_list) if "Book" in title]


min_index = min(index_known_chapter_titles)
max_index_find = index_all_chapter_titles.index(max(index_known_chapter_titles))

if(n_books == 5):
    max_index = len(raw_textbook_words_list)
else:
    max_index = index_all_chapter_titles[max_index_find+1]   

raw_known_textbook_vocabulary = raw_textbook_words_list[min_index:max_index]
#print(raw_known_textbook_vocabulary)


refined_known_textbook_vocabulary = [xx for xx in raw_known_textbook_vocabulary if "Book" not in xx]
length_refined_known_vocabulary = len(refined_known_textbook_vocabulary)                             
#print(refined_known_textbook_vocabulary)

raw_textbook_vocabulary_all = raw_textbook_words_list
refined_raw_vocabulary_list_textbook = [xx for xx in raw_textbook_vocabulary_all if "Book" not in xx]
length_refined_raw_vocabulary_list_textbook = len(refined_raw_vocabulary_list_textbook)

# Currently unused.
refined_unknown_vocab = [refined_raw_vocabulary_list_textbook[ind] for ind, i in enumerate(refined_raw_vocabulary_list_textbook) if i not in refined_known_textbook_vocabulary]
#print("My length")
#print("Length of refined raw vocab list textbook %i"%(len(refined_raw_vocabulary_list_textbook)))
#print('Length of refined known text book vocab %i'%(len(refined_known_textbook_vocabulary)))
#print((refined_unknown_vocab))

# All Chinese characters in the textbooks (non-unique)
all_characters_appended_textbook = ''.join(refined_raw_vocabulary_list_textbook)

# All unique Chinese characters in the textbooks
all_unique_characters_textbook = (list(set(all_characters_appended_textbook)))
known_characters_appended_textbook = ''.join(refined_known_textbook_vocabulary)
known_unique_textbook_characters = (list(set(known_characters_appended_textbook)))
##unknown_listed_characters = [xx for xx in all_characters_appended_textbook if xx not in known_characters_appended_textbook]


# Currently used.
##unknown_unique_textbook_characters = list(set(unknown_listed_characters))
# Gets frequency of unknown characters used in the textbook.
##freq_unknown_chars = Counter(unknown_listed_characters) 
#print(freq_unknown_chars)
#print(Counter(unknown_unique_textbook_characters))

parser = CedictParser()
entries = parser.parse()

if(data_conditioning) == True:
    if(your_TOCFL_level) > highest_TOCFL_level:
        your_TOCFL_level = 5
    elif(your_TOCFL_level <= 0):
        your_TOCFL_level = 1
    for i in range(1,highest_TOCFL_level+1):  
        if(i <= your_TOCFL_level):      
            level = i
            condition.clean_my_data(input_file_directory,level,raw_output_file1, raw_output_file2)
try:
    words_to_learn = find_words.find_words_to_learn(r"%s/Word list/%s.txt"%(input_file_directory,raw_output_file2),known_unique_textbook_characters, max_unknown_chars)
except FileNotFoundError:
     print("\nthe following file does not exist.")
     print(r"%s/Word list/%s.txt"%(input_file_directory,raw_output_file2))
     print("\nPlease configure data_conditioning = True\nPlease execute the script again.\n")
     sys.exit()

    
[filtered_words_to_learn.append(i) for i in refined_known_textbook_vocabulary if i not in words_to_learn]        


with open(r"%s/pleco_dangdai_plus.tsv"%(input_file_directory), 'at',encoding="utf-8") as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    if(TOCFL_list == True):
        print("\nGenerating TOCFL recommended words..")
        rnd_val_tracker = []
        for days in range(0,days_selected):
            tsv_writer.writerow(['///Additional words//TOCFL Recommended/Day %i'%(days+1)])            
            i = 1
            track_words_TOCFL = []           
            while True:
                rnd_val = random.randint(0,len(filtered_words_to_learn)-1)
                selected_word = filtered_words_to_learn[rnd_val]
                try:
                    word_meaning, pinyin_method1, pinyin_method2 = searchDict(selected_word,entries)
                    tsv_writer.writerow([selected_word,pinyin_method1,word_meaning[0]])
                    track_words_TOCFL.append(selected_word)
                    if(i >= n_suggest_words):
                      #  print('%i Words successfully added to TOCFL list.'%n_suggest_words)
                       # print("Added words are: %s"%track_words_TOCFL)
                        break
                except:    
                    i = i - 1
                    pass
                i += 1  
        print("\nDone!")
    else:
        print("No words added to TOCFL list.")
    if(dictionary_list == True):
        print("\nGenerated DragonMapper recommended words..")
        dict_word_list,pinyin_list,meanings_list = generate_dictionary_lists(entries)
        for days2 in range(0,days_selected):
            track_words_dict = []
            tsv_writer.writerow(['///Additional words//dictionary list/Day %i'%(days2+1)])
            for i in range(0,n_suggest_words):
                rnd_val = random.randint(0,len(dict_word_list))
                tsv_writer.writerow([dict_word_list[rnd_val],pinyin_list[rnd_val],meanings_list[rnd_val][0]])
                track_words_dict.append(dict_word_list[rnd_val])
            #print('%i Words successfully added to dictionary list.'%n_suggest_words)
            #print("Added words are: %s"%track_words_dict)
        print("\nDone!")
    else:
        print("No words added to dictionary list.")
    if(textbook_list == True):
        if not(len(refined_unknown_vocab) <= days_selected*n_suggest_words):
            print("\nGenerating textbook recommended words..")
            for days3 in range(0,days_selected):
                tsv_writer.writerow(['///Additional words//Textbook Bonus/Day %i'%(days3+1)])            
                i = 1
                track_words_textbook = []
                while True:
                    rnd_val = random.randint(0,len(refined_unknown_vocab)-1)
                    selected_word = refined_unknown_vocab[rnd_val]
                    try:
                        word_meaning, pinyin_method1, pinyin_method2 = searchDict(selected_word,entries)
                        tsv_writer.writerow([selected_word,pinyin_method1,word_meaning[0]])
                        track_words_textbook.append(selected_word)
                        if(i >= n_suggest_words):
                            #print('%i Words successfully added to Textbook bonus list.'%n_suggest_words)
                            #print("Added words are: %s"%track_words_textbook)
                            break
                    except:    
                        i = i - 1
                        pass
                    i += 1
            print("\nDone!")
        else:
            print("\nYou already know all the words!")
            print("No words added to Textbook bonus list.")
    else:
        print("No words added to Textbook bonus list.")
        
    print("\nYour file is ready to be to be used with Pleco.\n")
    print("Your file can be found at the following address: \t%s"%(input_file_directory))