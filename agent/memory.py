import os
import json

SESSION_FILE = "logs/session_memory.json"

def load_memory():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except json.JSONDecodeError:
            print("⚠️ Warning: session_memory.json is invalid. Starting with empty memory.")
    return []

def save_memory(memory):
    with open(SESSION_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def add_to_memory(entry):
    memory = load_memory()
    memory.append(entry)
    save_memory(memory)
