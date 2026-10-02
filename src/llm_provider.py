import os

from src.config.settings import LLM_MODEL, BASE_URL


if os.getenv("AWS_EXECUTION_ENV"):
    from langchain_aws import ChatBedrockConverse

    llm = ChatBedrockConverse(
        model="meta.llama3-8b-instruct-v1:0",
        region_name=os.getenv("AWS_REGION", "ap-south-1"),
        temperature=0,
        max_tokens=512,
    )
else:
    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model=LLM_MODEL,
        base_url=BASE_URL,
        temperature=0,
    )