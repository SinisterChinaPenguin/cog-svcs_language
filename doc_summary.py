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

def summarise_doc(p_client:str,file_path:str):
    '''Summarises a txt doc passed in

    Analyses all files found in folder_path

    Parameters:
    client (TextAnalyticsClient): Instance of Azure TextAnalyticsClient
    folder_path (str): Path to folder containing file to be analysed

    Returns: VOID - just prints results
'''

    print("\n****************************************************\n")
    print("file is",file_path)
    with open(file_path) as fso:
        free_text=[fso.read()]
#        print("\n")
#        pprint(free_text)
    print("\n")
    input("\nPress any key to continue....")
    print("\n**************EXTRACTIVE Summary ***************\n")
    try:
        # Start with sentement Analysis
        poller=p_client.begin_extract_summary(free_text)
        extract_summary_results = poller.result()
        for result in extract_summary_results:
            if result.kind == "ExtractiveSummarization":
                print("Summary extracted: \n{}".format(
                    " ".join([sentence.text for sentence in result.sentences]))
                )
            elif result.is_error is True:
                print("...Is an error with code '{}' and message '{}'".format(
                    result.error.code, result.error.message
                ))
        # [END extract_summary]
        input("\nPress any key to continue....")
        print("\n**************ABSTRACTIVE Summary ***************\n")

        poller = p_client.begin_abstract_summary(free_text)
        abstract_summary_results = poller.result()
        for result in abstract_summary_results:
            if result.kind == "AbstractiveSummarization":
                print("Summaries abstracted:")
                [print(f"{summary.text}\n") for summary in result.summaries]
            elif result.is_error is True:
                print("...Is an error with code '{}' and message '{}'".format(
                    result.error.code, result.error.message
                ))
            # [END abstract_summary]
        input("\nPress any key to continue....")
    


    except Exception as err:
        print(F"Encountered exception. {err}")


if len(sys.argv) < 4:
    print("Provide 3 arguments - "
          "<Language Service Endpoint> <key> <path to file with txt to be summarised>")
    sys.exit()
else:
    endpoint=sys.argv[1]
    key=sys.argv[2]
    path_to_folder=sys.argv[3]
    os.system('cls')
    print("\nAnalysing text in folder",path_to_folder)
    #print(endpoint)

analytics_client = authenticate_client(endpoint,key)
list_full_results=summarise_doc(analytics_client,path_to_folder)

