# 🧠 LLM Multi-Tool Agent

[![Build](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Enabled-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Langchain](https://img.shields.io/badge/Langchain-Integrated-yellowgreen)](https://www.langchain.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

### 🔍 Overview

This project showcases a **modular, goal-driven LLM agent** designed to deconstruct complex natural language tasks into actionable subgoals — automatically selecting and executing the appropriate tools (search, calculator, code runner, summarizer, etc.) to fulfill them.

Built as part of an **AI Engineer recruitment assessment**, this project demonstrates:
- Prompt engineering
- Tool orchestration
- LLM reasoning
- Real-world API integration (e.g. stock prices, search, summarization)

---

### 🎯 Key Features

- ✅ **Subgoal Planning**: Natural language goals are parsed into step-wise subgoals
- 🧰 **Tool Selection**: Automatically chooses the right tool (search, calculator, code, summarizer, etc.) per subgoal
- 🧠 **LLM Agent Loop**: Iteratively executes subgoals, passes results into memory
- 🌐 **Web Search & Summarization**: Uses DuckDuckGo or external URLs with article summarization via `newspaper3k`
- 📈 **Live Stock Prices**: Real-time data retrieval using `yfinance`
- 🧮 **Math & Code Execution**: Inline code and calculator utilities for logical/computational tasks
- 📄 **Streamlit UI**: Interactive demo front-end for visual walkthrough

---

### 💡 Demo Showcase

> 🖥️ A full interactive run-through is included in the attached [demo video](#) (or `demo/app.py`)

Sample goals handled:

- ✅ _"Find the current stock price of Apple and calculate the value of 100 shares"_
- 🧮 _"Calculate compound interest on an investment"_
- 🧠 _"Search for an article on machine learning and summarize it"_
- 💻 _"Write and execute Python code to find prime numbers up to 50"_
- 📊 _"Analyze word frequency and compute average word length from a text"_
- ⚡ _"Implement an async web scraper and benchmark performance"_

---

### 🏗️ Tech Stack

| Component        | Tool/Library          |
|------------------|------------------------|
| LLM Orchestration | [LangChain](https://www.langchain.com/) |
| Language Model    | OpenAI GPT (via API)   |
| Interface         | [Streamlit](https://streamlit.io) |
| Data Retrieval    | `yfinance`, DuckDuckGo, `newspaper3k` |
| Tool Routing      | Custom tool_router module |
| Code Execution    | Secure sandbox using `exec()` |
| Memory/State      | Lightweight JSON logging |

---

### 🧠 Agent Architecture

```mermaid
graph TD
    A[User Goal] --> B[LLM Planner]
    B --> C[Subgoal 1]
    B --> D[Subgoal 2]
    C --> E[Tool Router]
    D --> E
    E --> F{Tool?}
    F -->|Search| G[Web Search]
    F -->|Stock| H[Price API]
    F -->|Calculator| I[Math Eval]
    F -->|Code| J[Execute Python]
    F -->|Summarizer| K[Article Parsing]
    F -->|LLM| L[LLM Fallback]
    G --> M[Memory]
    H --> M
    I --> M
    J --> M
    K --> M
    L --> M
````

---

### 🚀 Run Locally

```bash
git clone https://github.com/yourusername/llm-multitool-agent
cd llm-multitool-agent

# Recommended: use a virtualenv
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY=your-key-here

# Run the Streamlit app
streamlit run demo/app.py
```

---

### 📁 Repo Structure

```
llm-multitool-agent/
│
├── demo/              # Streamlit app entrypoint
├── agent/             # Core agent logic (planner, router, memory)
├── tools/             # Individual tools (calculator, code runner, stock, etc.)
├── prompts/           # Prompt templates
├── logs/              # JSON logs for memory/history
└── evaluation/        # Benchmark suite (optional)
```

---

### 📌 Why This Matters

This project demonstrates my ability to:

* Architect intelligent LLM-driven workflows
* Leverage modular design for tool augmentation
* Integrate real APIs with clean, testable code
* Build production-grade LLM pipelines from scratch

🛠️ It reflects not just technical ability, but **end-to-end ownership**, prompt strategy, and system thinking — essential for AI Engineering roles.

---

### 📄 License

MIT License
