from src.services.rag_service import answer_question
while True:

    question = input("\nYou: ")

    if question.lower() in ["exit", "quit"]:
        break

    result = answer_question(question)

    print("\nAI:")
    print(result["answer"])