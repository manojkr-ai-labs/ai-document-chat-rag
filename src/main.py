from src.services.rag_service import answer_question

question = "What is Kubernetes?"

# answer = answer_question(question)

# print("\nAI Answer:\n")
# print(answer)

result = answer_question(question)

print("\nAI Answer\n")
print(result["answer"])

print("\nSources\n")

for citation in result["citations"]:
    print(
        f"- {citation['source']} (Page {citation['page']})"
    )