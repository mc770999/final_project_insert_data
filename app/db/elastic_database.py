import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

# Load environment variables from .env file
load_dotenv(verbose=True)

# Create the Elasticsearch client
es_client = Elasticsearch(
    [os.getenv("ELASTIC_URL_DB")],
    verify_certs=False
)

