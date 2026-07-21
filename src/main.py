from src.readers.pdf_reader import read_pdf
from src.chunking.text_splitter import split_text
from src.embeddings.embedding_model import embedding_model

from src.vectorstore.chroma_store import vector_db

# print("=" * 60)
# print("Loading PDF")
# print("=" * 60)

text = read_pdf("data/NDSAP Implementation Guidelines 2.4.pdf")

chunks = split_text(text)

vectors = embedding_model.embed_documents(chunks)

# print(f"\nCharacters : {len(text)}")
# print(f"Chunks     : {len(chunks)}")
# print(f"Vectors    : {len(vectors)}")
# print(f"Dimensions : {len(vectors[0])}")

# print("\nFirst Chunk:\n")
# print(chunks[0][:200])

# print("\nFirst Vector (first 10 values):\n")
# print(vectors[0][:10])

# print("\nCheck permanent storage:\n")
# print(vector_db._collection.count())

# vector_db.add_texts(chunks)

# print("Stored Successfully!")
from src.retriever.document_retriever import retrieve_documents

# query = "What is NDSAP?"
query = "What is metadata?"
# What is metadata?

# Who is responsible for implementation?

# What is the objective of NDSAP?

# Which ministry issued the policy?

# Explain version history. //similarity_search_with_score

# results = retrieve_documents(query)

# print("=" * 60)
# print("QUESTION")
# print("=" * 60)

# print(query)

# print("\n")

# print("=" * 60)
# print("TOP RESULTS")
# print("=" * 60)

# for index, doc in enumerate(results, start=1):

#     print(f"\nResult {index}")

#     print("-" * 60)

#     print(doc.page_content[:400])

#     print()

results = vector_db.similarity_search_with_score(
    query=query,
    k=5
)

for document, score in results:

    print(score)

    print(document.page_content[:200])