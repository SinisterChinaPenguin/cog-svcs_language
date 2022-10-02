# cog-svcs_language

POC code for running Azure Cognitive Services language analysis

Specifically, this code was set up to look at a law enforcement scenario where we are interested in POL data 
(People, Organisations, Locations) which are often in large blocks of unstructured data submitted 
by memebers of the public.

Once data is extracted it can be included in an Elastic Search Index, combined with internal POL data.

Pre-reqs:

azure-ai-textanalytics Python Module

Tested on Python 3.9
