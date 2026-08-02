
# add Regenerate feature


Google Engineer Workflow

They typically evaluate using a matrix like this:

Test	Llama	GPT	Claude	Gemini
PDF Loading	✅	✅	✅	✅
Chunking	✅	✅	✅	✅
Retrieval	✅	✅	✅	✅
Hallucination	Medium	Low	Low	Low
Response Speed	Fast	Fast	Medium	Fast
Cost	Free	Paid	Paid	Paid

The application code stays the same; only the model changes.

llm = OllamaLLM(model="llama3.2")

LLM Interface
        │
 ┌──────┼────────┐
 │      │        │
Ollama OpenAI Claude Gemini


documents/ → PDFs and data for the RAG application.
docs/ → Documentation for developers.