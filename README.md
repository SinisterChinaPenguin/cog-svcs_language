# cog-svcs_language

POC code for running Azure Cognitive Services language analysis

Specifically, this code was set up to look at a law enforcement scenario where we are interested in POL data 
(People, Organisations, Locations) which are often in large blocks of unstructured data submitted 
by members of the public.

Once data is extracted it can be combined with internal POL data to give investigation teams quick access to information provided by the public which might be relevent to an investigation.

Pre-reqs:

azure-ai-textanalytics Python Module
azure.core 
tabulte
pprint
pathlib

Tested on Python 3.9
