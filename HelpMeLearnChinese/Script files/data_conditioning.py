# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 09:38:05 2022

@author: dylan
"""

from PyPDF2 import PdfReader
import re

def clean_my_data(input_path,word_level,raw_output_file1, raw_output_file2):
    '''    
    This function preprocesses files taken from:
    to be used later on for suggesting words for file generation.
    
    Although the vocabulary is sourced from the same website, they did not provide
    spreadsheets and so it had to read as a PDF. They also used three different formats;
    this function caters for this and cleans it up into a single, generic format
    consisting of only the raw word.
    
    For each word, the sourced meaning and word type are removed as it was difficult to
    get a single format across all three format types. The meaning will later be attached
    to each vocabulary unit by using a ChineseDictionary.    
    '''
    
    #Determines what level of vocabulary is to be used, and the appropriate formatting type
    if(word_level == 1):
        file_ending = 'word_beg'
        format_type = 3
    if(word_level == 2):
        file_ending = 'word_bas'
        format_type = 1
    if(word_level == 3):
        file_ending = 'word_level1'
        format_type = 2
    if(word_level == 4):
        file_ending = 'word_int'
        format_type = 1
    if(word_level == 5):
        file_ending = 'word_adv'
        format_type = 1 
    
    
    
    input_directory = r"%s\Word list\%s.pdf"%(input_path,file_ending)
    
    reader = PdfReader(input_directory)
    text = ""
    
   # print("There are a total of %i pages."%(len(reader.pages)))


    for count, page in enumerate(reader.pages):
        if(format_type == 2):
            if(count > 11):
                continue
        text += page.extract_text() + "\n"
            
###############################################################################
# Preprocessing of files are done here

    with open(r"%s\Word list\%s.txt"%(input_path,raw_output_file1),"wt",encoding = "utf") as out_file:
        out_file.writelines(text)     
        out_file.close()
    test_array = []
    with open(r"%s\Word list\%s.txt"%(input_path,raw_output_file1),"r",encoding = "utf") as file_edit: 
        for indx, line in enumerate(file_edit):
            if(line.startswith("國家華語")):
                continue
            elif "第" in line:
                continue
            elif "詞彙 拼音 等級 詞類 詞彙 拼音 等級 詞類" in line:
                continue
            elif "詞表" in line:
                continue
            elif "詞彙 拼音 詞類 詞彙 拼音 詞類 詞彙 拼音 詞類" in line:
                continue
            elif "詞彙 拼音 等級 詞類" in line:
                continue
            else:
                # Helps create a generic output format for later processing.
                if(format_type == 1):
                    y = [x + '\n' for x in re.findall(r'[\u4e00-\u9fff]+',line)]
                    y = '\n'.join(y) 
           
                if(format_type == 2):
                    line = line.replace(')','')
                    line = line.replace('(','')
                    y = [x for x in re.findall(r'[\u4e00-\u9fff]+',line)]
                    y = ''.join(y) + '\n'

                if(format_type == 3):
                    y = [x for x in re.findall(r'[\u4e00-\u9fff]+',line)]
                    y = '\n'.join(y) + '\n'                  
                    
                test_array.append(y)
            
###############################################################################
# Saves the pre-processed file for later access.
    with open(r"%s\Word list\%s.txt"%(input_path,raw_output_file2),"at",encoding = "utf") as out_file:
        out_file.writelines(test_array)  
        out_file.close()
