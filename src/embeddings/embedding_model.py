import os

from langchain_aws import BedrockEmbeddings
from langchain_ollama import OllamaEmbeddings

from src.config.settings import BASE_URL, EMBEDDING_MODEL

if os.getenv("AWS_EXECUTION_ENV"):
    embedding_model = BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v2:0",
        region_name=os.getenv("AWS_REGION", "ap-south-1"),
    )
else:
    embedding_model = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=BASE_URL,
    )