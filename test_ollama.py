from src.llm.ollama_client import get_llm

# Connect to Llama
llm = get_llm()

# Send a test question
response = llm.invoke(
    "What is artificial intelligence? Explain simply."
)

# Display response
print(response.content)