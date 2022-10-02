'''
    Quick & dirty script to remove text from files
    Used to remove common strings (virus check, office address, etc...)
    which we don;t want included in text analysis.

    Usage:
    Set FOLDER_IN to folder with files to remove text from
    Set FOLDER_OUT to location to write cleaned up text
    '''

import re
import os

def check_data(msg:str):
    '''checkData - checks a string for text we want to ignore
    Used as a quick & dirty mechanism to remove common strings which muddy
    Cognative services keyword searches

    Returns 1 if the line of text does NOT contain text we want to ignore
    i.e. 1= text clean, go aheaad & write in cleaned output

    Parameters:
    txt - the text we want to test for a known string
        '''
    ret=1
    if re.search("^From:|Sent:|To:",msg):
        ret=0
    if re.search("^www.version1.com?",msg):
        ret=0
    if re.search("^Millennium House",msg):
        ret=0
    if re.search("\s<https://eur02.safelinks.protection.outlook.com",msg):
        ret=0
    if re.search("^\+44",msg):
        ret=0
    if re.search("^CAUTION:",msg):
        ret=0
    if re.search("^12 Cromac Place",msg):
        ret=0
    if re.search("^The information in this email may be confidential",msg):
        ret=0
    if re.search("^8-12 New Bridge Street",msg):
        ret=0
    if re.search("^4/5 Lochside View",msg):
        ret=0
    return ret

FOLDER_IN=".\\data_in"
FOLDER_OUT=".\\data_clean"

for file_name in os.listdir(FOLDER_IN):
    file_in_path=os.path.join(FOLDER_IN,file_name)
    file_out_path=os.path.join(FOLDER_OUT,file_name)
    f = open(file_in_path, "r", encoding='utf-8')
    w = open(file_out_path,"w", encoding='utf-8')
    for line in f:
        text_line = str(line)
        if check_data(text_line)==1:
            w.write(text_line)

print("done!")
