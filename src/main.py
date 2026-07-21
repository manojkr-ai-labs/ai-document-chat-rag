from src.llm_provider import llm

print("=" * 50)
print("Testing Ollama Connection")
print("=" * 50)

response = llm.call("Who are you?")

print("\nResponse:\n")
print(response)