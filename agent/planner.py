# agent/planner.py

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment.")

# Initialize LLM
llm = ChatOpenAI(temperature=0, openai_api_key=api_key)

# Prompt Template
template = """
You are a task planner AI. Break the following task into smaller subgoals.

Task: {task}

Respond with a numbered list, one subgoal per line.
"""
prompt = PromptTemplate.from_template(template)

def generate_subgoals(task):
    return llm.invoke(prompt.format(task=task)).content  # Return plain string
