from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0)

def chat_response(prompt):
    return llm.predict(prompt)