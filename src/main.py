from src.services.rag_service import answer_question

question = "What is Kubernetes?"

answer = answer_question(question)

print("\nAI Answer:\n")
print(answer)