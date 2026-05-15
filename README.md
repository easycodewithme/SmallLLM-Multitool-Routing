# LLM Multi-Tool Agent

A goal-driven CLI agent that takes a natural-language query, classifies the
intent, and routes the query to the most appropriate tool (calculator, web
search, stock price, code executor, URL summarizer, or a direct LLM answer).

- **Intent classifier:** DistilBERT (zero-shot, runs on CPU, deterministic)
- **Chat / fallback LLM:** Gemma 3 1B running locally via Ollama
- **No paid APIs.** No cloud LLM. The classifier is local. The chat model is local.

---

## Architecture

```
                              user query
                                  |
                                  v
                +-----------------+----------------+
                |       Hybrid Intent Router       |
                +----------------------------------+
                | Stage 1 - Deterministic patterns |
                |   summarize+URL  -> summarizer   |
                |   "execute code:"-> code_executor|
                +----------------------------------+
                | Stage 2 - Keyword router         |
                |   greetings      -> llm          |
                |   math/operators -> calculator   |
                |   "stock price"  -> stock_price  |
                |   weather/news/  -> search       |
                |   "search for X" -> search       |
                +----------------------------------+
                | Stage 3 - DistilBERT zero-shot   |
                |  (typeform/distilbert-base-      |
                |   uncased-mnli, ~250 MB, CPU)    |
                |  used only for ambiguous cases   |
                +-----------------+----------------+
                                  |
        +---------+--------+------+------+---------+--------+
        v         v        v             v         v        v
   calculator search  stock_price   code_exec  summarizer  llm
    (eval)  (DDG)   (yfinance)    (exec)    (newspaper3k) (Gemma 3 1B)
```

The agent is **single-shot per query** — it runs one tool and returns one
answer. No multi-step planning, no subgoal decomposition.

---

## Why a hybrid router?

A pure LLM classifier on a small model is unreliable. A pure keyword router
misses semantic nuance. The hybrid approach:

1. **Deterministic patterns** absorb unambiguous cases (URL + summarize, code
   execution prefix). 100% accuracy by construction.
2. **Keyword router** handles strong-signal patterns (math operators, "stock",
   "weather", greetings). Fast, transparent, no model inference.
3. **DistilBERT zero-shot** disambiguates the rest — typically open questions
   like *"tell me about X"* where the line between *search* and *llm* is fuzzy.

In practice this gives near-perfect routing on the demo set with sub-second
latency on CPU.

---

## Models

| Component | Model | Size | Runtime |
|---|---|---|---|
| Intent classifier | `typeform/distilbert-base-uncased-mnli` | ~250 MB | Hugging Face `transformers` (CPU) |
| Chat / `llm` fallback | `gemma3:1b` (Google Gemma 3 1B IT) | ~815 MB | Ollama (local server) |

Both models can be swapped via env vars in `.env`:

```
LLM_MODEL=gemma3:1b              # Ollama tag
INTENT_MODEL=typeform/distilbert-base-uncased-mnli   # HF model id
INTENT_CONFIDENCE=0.30            # threshold below which we fall back
OLLAMA_HOST=http://localhost:11434
```

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **Python 3.10+** | Tested on Python 3.14 (Windows 11) |
| **Ollama** | Free local LLM runtime — https://ollama.com/download |
| **Disk** | ~1 GB Gemma 3 1B + ~250 MB DistilBERT + deps ≈ 2 GB total |
| **RAM** | 4 GB minimum |
| **Internet (one-time)** | Model downloads only |

---

## Setup (Windows)

### 1. Install Ollama

Download from <https://ollama.com/download> and run the installer. The Ollama
service auto-starts on `http://localhost:11434`.

```cmd
ollama --version
```

### 2. Pull the Gemma 3 1B model

```cmd
ollama pull gemma3:1b
```

~815 MB. One-time download.

```cmd
ollama list
```

You should see `gemma3:1b`.

### 3. Install Python dependencies

```cmd
cd llm-multitool-agent
pip install -r requirements.txt
```

This installs `transformers` and `torch` for the DistilBERT classifier — first
import will trigger an automatic ~250 MB model download from Hugging Face.

### 4. Download NLTK data (one-time, for the URL summarizer)

```cmd
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

### 5. Run

```cmd
python main.py
```

Or one-shot:

```cmd
python main.py "calculate 132 + 345"
```

---

## Usage

### Interactive mode

```cmd
python main.py
```

```
================================================================
  LLM Multitool Agent  |  Model: gemma3:1b
  Runtime: Ollama @ http://localhost:11434
================================================================
Interactive mode. Type 'exit' or 'quit' to leave.

Available tools & capabilities:
  - calculator    : evaluates arithmetic expressions
  - search        : DuckDuckGo web search for general queries
  - stock_price   : live stock price via yfinance
  - code_executor : runs Python code snippets
  - summarizer    : extracts/summarizes a web article from a URL
  - llm fallback  : reasons over the goal when no tool fits

>
```

Type `exit` or `quit` to leave.

### One-shot mode

```cmd
python main.py "find current stock price of Apple"
```

Output:

```
[tool: stock_price]
The current stock price of AAPL is $269.74.
```

---

## Tools

| Tool | Library | API key? | Example query |
|---|---|---|---|
| `calculator` | `eval` (sandboxed) | No | `what is square of 10` |
| `search` | `ddgs` (DuckDuckGo) | No | `what is the weather in london` |
| `stock_price` | `yfinance` | No | `find current stock price of Apple` |
| `code_executor` | `exec` (sandboxed stdout) | No | `execute code: print(sum(range(1,11)))` |
| `summarizer` | `newspaper3k` | No | `summarize https://en.wikipedia.org/wiki/Python_(programming_language)` |
| `llm` | `gemma3:1b` via Ollama | No (local) | `explain recursion in one sentence` |

The calculator understands natural-language phrasing:
`square of 10`, `8 cubed`, `5 to the power of 3`, `100 divided by 4`,
`7 plus 13`, `25 times 18`, `10^2`.

---

## Demo script

Each line: query (left) → expected tool (right). The `[tool: …]` line printed
by the agent confirms the routing.

```
hi                                                                     -> llm
hello there                                                            -> llm
calculate 132 + 345                                                    -> calculator
what is square of 10                                                   -> calculator
what is 25 times 18                                                    -> calculator
7 plus 13                                                              -> calculator
find current stock price of Apple                                      -> stock_price
search for what is langchain                                           -> search
what is the weather in london                                          -> search
latest news about openai                                               -> search
execute code: print(sum(range(1, 11)))                                 -> code_executor
summarize https://en.wikipedia.org/wiki/Python_(programming_language)  -> summarizer
explain recursion in one sentence                                      -> llm
tell me about quantum computing                                        -> llm
```

All 14 queries above were verified end-to-end on the reference setup.

---

## Project layout

```
llm-multitool-agent/
├── main.py                       # CLI entry point
├── agent/
│   ├── intent_classifier.py      # DistilBERT zero-shot classifier
│   ├── tool_router.py            # Hybrid 3-stage router
│   ├── interaction.py            # Direct LLM answer (no-tool path) via Ollama
│   └── memory.py                 # Per-session JSON log
├── tools/
│   ├── calculator.py             # Natural-language arithmetic
│   ├── search_tool.py            # DuckDuckGo (top-3 snippets)
│   ├── stock_price.py            # yfinance live price
│   ├── code_executor.py          # Python exec, captures stdout
│   ├── summarizer.py             # PDF (PyMuPDF) and URL (newspaper3k) summaries
│   └── text_analysis.py          # (Standalone helper, not used by router)
├── logs/                         # Session memory (auto-generated)
├── requirements.txt
├── .env
└── README.md
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ConnectError: connection refused` | Ollama service not running. Open the Ollama app. |
| `model 'gemma3:1b' not found` | `ollama pull gemma3:1b` |
| `model requires more system memory` | The Gemma model is too big for your free RAM. Try `gemma3:1b` (smallest). |
| Summarizer error about `punkt_tab` | `python -c "import nltk; nltk.download('punkt_tab')"` |
| `UnicodeEncodeError` on Windows `cmd` | Already handled — `main.py` reconfigures stdout to UTF-8. |
| First query is slow | DistilBERT loads lazily on first classification call (~3-5 s). Subsequent calls are <1 s. |
| HF Hub rate-limit warnings | Set `HF_TOKEN` env var with a free Hugging Face token, or ignore the warning. |

---

## License

MIT
