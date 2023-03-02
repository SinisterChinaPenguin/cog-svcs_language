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

    for file_name in os.listdir(p_folder_path):
        file_path=p_folder_path + "\\" + file_name
        file_extension=pathlib.Path(file_path).suffix
        if file_extension != ".txt":
            continue
        print("\n****************************************************\n")
        print("file is",file_path)
        with open(file_path) as fso:
            free_text=[fso.read()]
        print("\n")
        pprint(free_text)
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
                topfive=response.key_phrases[:5]
                key_phrases=[["Key Phrases"]]
                for phrase in topfive:
                    key_phrases.append([phrase])
                print("\n",tabulate(key_phrases,headers='firstrow'))
            else:
                print("Error getting Key Phrases from document")

            input("\nPress any key to continue....")
            os.system('cls')
        except Exception as err:
            print(F"Encountered exception. {err}")


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
entity_recognition_example(analytics_client,path_to_folder)
