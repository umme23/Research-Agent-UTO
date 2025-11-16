# agents/code_agent.py - simple code execution agent
from tools import run_python_code
from memory import SessionStore

class CodeAgent:
    def __init__(self, name="code_agent", bus=None, session_store: SessionStore=None):
        self.name = name
        self.bus = bus
        self.session_store = session_store or SessionStore()

    def execute(self, session_id, code_snippet):
        out = run_python_code(code_snippet)
        self.session_store.push_message(session_id, "code_agent", f"exec:{out}")
        return out
