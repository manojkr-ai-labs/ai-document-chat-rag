from src.services.rag_service import ask_document

# question = "What is NDSAP?"
# question = "Who published this document?"
question = "Explain version history."

answer = ask_document(question)

print("=" * 60)
print("QUESTION")
print("=" * 60)
print(question)

print()

print("=" * 60)
print("ANSWER")
print("=" * 60)
print(answer)