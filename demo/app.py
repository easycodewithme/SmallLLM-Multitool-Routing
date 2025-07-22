import os
import sys

# Add root so that tools, agent, etc. are importable
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tools.summarizer import summarize_pdf
from tools.summarizer import summarize_url
from tools.stock_price import get_stock_price
from tools.calculator import calculate
from tools.search_tool import search
from tools.code_executor import execute_code
from tools.calculator import calculate_expression

from agent.planner import generate_subgoals
from agent.tool_router import route_tool
from agent.interaction import chat_response
from agent.memory import add_to_memory, load_memory

import streamlit as st
import re
from dotenv import load_dotenv
load_dotenv()


from agent.planner import generate_subgoals
from agent.tool_router import route_tool
from agent.interaction import chat_response
from agent.memory import add_to_memory, load_memory

from tools.calculator import calculate
from tools.search_tool import search
from tools.code_executor import execute_code
from tools.summarizer import summarize_pdf
from tools.stock_price import get_stock_price

st.set_page_config(page_title="Multitool Agent", layout="wide")
st.title("🧠 LLM Multitool Agent")

query = st.text_input("Enter your high-level goal here:")

if st.button("Run Agent") and query:
    st.markdown("### Subgoal Planning")
    subgoals = generate_subgoals(query)
    if hasattr(subgoals, 'content'):
        subgoals = subgoals.content
    subgoal_list = [line.strip() for line in subgoals.split("\n") if line.strip()]
    for i, line in enumerate(subgoal_list):
        st.markdown(f"**{i+1}. {line}**")

    st.markdown("### Execution Results")
    for i, line in enumerate(subgoal_list):
        st.markdown(f"**{i+1}. {line}**")

        tool = route_tool(line)
        st.markdown(f"🔧 Tool selected: `{tool}`")

        try:
            if tool == "calculator":
                result = calculate_expression(line)
            elif tool == "search":
                result = search(line)
            elif tool == "stock_price":
                result = get_stock_price(line)
            elif tool == "code_executor":
                result = execute_code(line)
            elif tool == "summarizer":
                result = summarize_url(line)
            else:
                from langchain.chat_models import ChatOpenAI
                from langchain.schema import HumanMessage
                llm = ChatOpenAI(temperature=0)
                result = llm([HumanMessage(content=line)]).content
        except Exception as e:
            result = f"❌ Error: {str(e)}"

        st.write(result)
        add_to_memory({"subgoal": line, "tool": tool, "result": result})

