import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

llm = ChatOllama(
    model=os.getenv("LLM_MODEL", "gemma3:1b"),
    base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    temperature=0,
)

SYSTEM = (
    "You are a concise assistant. Answer in 1-3 short sentences. "
    "No headers, no bullet lists, no markdown formatting, no examples unless asked. "
    "If you don't know, say so briefly."
)


def chat_response(prompt: str) -> str:
    return llm.invoke(
        [SystemMessage(content=SYSTEM), HumanMessage(content=prompt)]
    ).content
