
from dotenv import load_dotenv
import os
import chromadb
from llama_index import GPTVectorStoreIndex
from llama_index.readers import TrafilaturaWebReader
from googleapiclient.discovery import build

from llama_index.llms import AzureOpenAI
from llama_index.embeddings import AzureOpenAIEmbedding
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
import logging
import sys
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
from llama_index import set_global_service_context
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.response.schema import Response


load_dotenv()


api_key = os.getenv("AZURE_CHATGPT_API_KEY")
azure_endpoint = os.getenv("AZURE_CHATGPT_ENDPOINT")

api_version = "2023-07-01-preview"

embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="text-embedding-ada-002",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

llm = AzureOpenAI(
    model="gpt-35-turbo",
    deployment_name="gpt-35-turbo",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embed_model,
)

set_global_service_context(service_context)

def create_embedding_store(name):
    chroma_client = chromadb.Client()
    return chroma_client.create_collection(name)
global collection

collection = create_embedding_store("supertype")

vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


def query_pages(collection, urls, questions):
    print("*****************************")
    docs = TrafilaturaWebReader().load_data(urls)
    
    print(docs)
    index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)
    print(index)
    print(1)
        
    query_engine = index.as_query_engine()
    answers = []
    print(questions)
    answer = query_engine.query(questions)

    # extract the response form the Response(response= "")
    
    if hasattr(answer, 'response'):
        extracted_response = answer.response
        print(extracted_response)

    print(extracted_response)
    return extracted_response

def google_search():
    query  = input("Enter the simple Query: ")
    ai_query = input("Enter the query to the AI: ")

    print(ai_query)
    GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
    GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

    num_of_links = 1

    service = build("customsearch", "v1", developerKey=GOOGLE_SEARCH_API_KEY)
    res = service.cse().list(q=query, cx=GOOGLE_SEARCH_ENGINE_ID, num=num_of_links).execute()
    url_list = [item['link'] for item in res['items']]
    print(url_list)

    answers = query_pages(collection, url_list, ai_query)
    print(answers)
    return (answers)

google_search()