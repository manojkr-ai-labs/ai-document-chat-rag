RAG_PROMPT = """
You are an AI assistant.

Answer the user's question ONLY using the context below.

If the answer cannot be found in the context, say:

"I could not find the answer in the document."

-------------------------
Context:

{context}

-------------------------

Question:

{question}

Answer:
"""