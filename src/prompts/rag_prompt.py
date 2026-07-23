def build_prompt(
    context,
    question,
    conversation,
):
    """
    Build the final RAG prompt with conversation history.
    """

    context_text = "\n\n".join(
        doc.page_content
        for doc in context
    )

    prompt = f"""
You are an AI assistant.

Answer ONLY from the provided context.

If the answer isn't available,
say you don't know.

=========================
Conversation History
=========================

{conversation}

=========================
Context
=========================

{context_text}

=========================
Question
=========================

{question}

=========================
Answer
=========================
"""

    return prompt