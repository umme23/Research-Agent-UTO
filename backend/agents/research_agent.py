# agents/research_agent.py - research agent using web_search stub
from tools import web_search
from memory import SessionStore

class ResearchAgent:
    def __init__(self, name="research_agent", bus=None, session_store: SessionStore=None):
        self.name = name
        self.bus = bus
        self.session_store = session_store or SessionStore()

    def research(self, session_id, query, topk=3):
        results = web_search(query, max_results=topk)
        self.session_store.push_message(session_id, "research_agent", f"results:{results}")
        compact = [{"title": r["title"], "snippet": r["snippet"], "url": r.get("url")} for r in results]
        return compact
