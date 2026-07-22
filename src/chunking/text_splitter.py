from langchain_text_splitters import RecursiveCharacterTextSplitter


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)


def split_documents(documents):
    """
    Split LangChain Documents while preserving metadata.
    """
    return text_splitter.split_documents(documents)