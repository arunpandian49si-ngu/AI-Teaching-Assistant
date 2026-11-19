
from langchain_ollama import ChatOllama


def get_llm():

    llm = ChatOllama(
        model="llama3.2:1b",
        temperature=0.2
    )

    return llm
