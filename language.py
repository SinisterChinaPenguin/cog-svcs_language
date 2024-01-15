''' how to use:
1) install the text analytics library
pip install azure-ai-textanalytics==5.1.0
2) Stand up Azure Cog Svcs & Language Service in portal
get the language key & endpoint
3) Run code passing in endpoint, key & folder with txt files to be analysed
e.g. py .\language.py "https://<resname>.cognitiveservices.azure.com/" "<key>" ".\myfiles"
'''

import os
import sys

#pip install azure-ai-textanalytics
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from tabulate import tabulate
from pprint import pprint
import pathlib

def remove_key_words(word_list):
    remove_words=['Key Phrases','value','people','the financial conduct authority','new window']
    for wd in remove_words:
        if wd in word_list:
            word_list.remove(wd)
    return word_list

def list_to_lists(my_list):
    return [[el] for el in my_list]

def dedupe_string(my_text):
    words = my_text.lower().split()
    txt_dedupe=" ".join(sorted(set(words), key=words.index))
    return txt_dedupe

def remove_trailing_opens(string1):
    '''
    Checks if a string ends in "opens" & removes unless a space preceeds "opens"
    e.g. "Consumer Contracts RegulationOpens" becomes "Consumer Contracts Regulation"
    this is becase we have "opens in a new window" floating around a lot

    Parameters:
    string1: the string to clean up

    Returns: string (cleaned up text or the original if no work done)
'''
    end_str=string1[-5:] # last 5 chars of string
    if end_str.lower() == 'opens':
        char_before=string1[-6:-5] # check what character before opens is (is it a space?)
        if char_before != ' ':
            string1 = string1[:-5] # remove last 5 characters (i.e. opens from opens in new window)
    return string1


# Authenticate the client using your key and endpoint
def authenticate_client(p_endpoint:str,p_key:str):
    '''
    Creates a textAnalyticsClient object to allow us
    to interact with the Cog Svc API

    Parameters:
    p_endpoint - Cog Svcs language REST endpoint
    p_key - Cog svcs authorisation key

    Returns: TextAnalyticsClient object
'''
    ta_credential = AzureKeyCredential(p_key)
    ta_client = TextAnalyticsClient(
            endpoint=p_endpoint,
            credential=ta_credential)
    return ta_client

def entity_recognition_example(p_client:str,p_folder_path:str):
    '''Returns known entities & keywords found from
    analysiing free text using Azure Conitive Services.

    Analyses all files found in folder_path

    Parameters:
    client (TextAnalyticsClient): Instance of Azure TextAnalyticsClient
    folder_path (str): Path to folder containing files to be analysed

    Returns: VOID - just prints results
'''
    key_phrases_global=["Key Phrases"]
    for file_name in os.listdir(p_folder_path):
        file_path=p_folder_path + "\\" + file_name
        file_extension=pathlib.Path(file_path).suffix
        if file_extension != ".txt":
            continue
        print("\n****************************************************\n")
        print("file is",file_path)
        with open(file_path) as fso:
            free_text=[fso.read()]
#        print("\n")
#        pprint(free_text)
        print("\n")
        input("\nPress any key to continue....")
        try:
            # Start with sentement Analysis
            result=p_client.analyze_sentiment(free_text, show_opinion_mining=True)
            docs = [doc for doc in result if not doc.is_error]
            for idx, doc in enumerate(docs):
            #  print(f"Document text: {myMail[idx]}")
                print(f"Overall sentiment: {doc.sentiment}\n")

            # Entity recognition - categorises known entities e.g.
            #  People, Organisations, Events, Dates, Numbers etc...
            # you can create your own with RegEx, keywords, ML learning etc...
            analysis_results=[["Entity","Value","confidence"]]
            result = p_client.recognize_entities(documents = free_text)[0]
            for entity in result.entities:
                if float(entity.confidence_score) > 0.8:
                    if entity.category == "Person":
                        analysis_results.append(["Person",entity.text,round(entity.confidence_score, 2)])
                    if entity.category == "PersonType":
                        analysis_results.append(["Person Role",entity.text,round(entity.confidence_score, 2)])
                    if entity.category == "Location" and\
                    entity.text != "Grosvenor House" and\
                    entity.text != "Prospect Hill":
                        analysis_results.append(["Location",entity.text,round(entity.confidence_score, 2)])
                    if entity.category == "Organization" and\
                    entity.text != "Microsoft":
                        analysis_results.append\
                        (["Organisation",entity.text,round(entity.confidence_score, 2)])
                    if entity.category == "Event" and entity.text != "meeting" and entity.text != "Meeting":
                        analysis_results.append(["Event",entity.text,round(entity.confidence_score, 2)])
            print(tabulate(analysis_results,headers='firstrow'))

            # key phrase analysis - we do top 5 (they are ordered in importance)
            response=p_client.extract_key_phrases(documents = free_text)[0]
            if not response.is_error:
                topfive=response.key_phrases[:8]
                key_phrases=[["Key Phrases"]]
                for phrase in topfive:
                    phrase=remove_trailing_opens(phrase)
                    phrase=dedupe_string(phrase)
                    key_phrases.append([phrase])
                    key_phrases_global.append(phrase)
                print("\n",tabulate(key_phrases,headers='firstrow'))
            else:
                print("Error getting Key Phrases from document")

            input("\nPress any key to continue....")
            os.system('cls')
        except Exception as err:
            print(F"Encountered exception. {err}")
    
    return key_phrases_global


if len(sys.argv) < 4:
    print("Provide 3 arguments - "
          "<Language Service Endpoint> <key> <path to folder with txt to be analysed>")
    sys.exit()
else:
    endpoint=sys.argv[1]
    key=sys.argv[2]
    path_to_folder=sys.argv[3]
    os.system('cls')
    print("\nAnalysing text in folder",path_to_folder)
    #print(endpoint)

analytics_client = authenticate_client(endpoint,key)
list_full_results=entity_recognition_example(analytics_client,path_to_folder)
list_full_results = list(set(list_full_results))
list_full_results = remove_key_words(list_full_results)
list_full_results = list_to_lists(list_full_results)
list_full_results.insert(0,["Key Phrases"])
print("\n",tabulate(list_full_results,headers='firstrow'))
