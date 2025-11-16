# director.py - orchestrator that assigns tasks to agents
import threading, time
from a2a import A2ABus
from memory import SessionStore
from agents.document_agent import DocumentAgent
from agents.research_agent import ResearchAgent
from agents.code_agent import CodeAgent
from observability import record_metric

class Director:
    def __init__(self, session_store: SessionStore = None):
        self.bus = A2ABus()
        self.session_store = session_store or SessionStore()
        self.document_agent = DocumentAgent(bus=self.bus, session_store=self.session_store)
        self.research_agent = ResearchAgent(bus=self.bus, session_store=self.session_store)
        self.code_agent = CodeAgent(bus=self.bus, session_store=self.session_store)
        self.jobs = {}

    def create_session(self, session_id, user_id, meta=None):
        self.session_store.create_session(session_id, user_id, meta)
        self.jobs[session_id] = {"state":"created", "events": []}

    def start_job(self, session_id, goal_text, user_id, prefer_short=True):
        t = threading.Thread(target=self._orchestrate, args=(session_id, goal_text, user_id, prefer_short), daemon=True)
        t.start()

    def _orchestrate(self, session_id, goal_text, user_id, prefer_short):
        self.jobs[session_id] = {"state":"running", "goal":goal_text, "start": time.time(), "events":[]}
        record_metric("active_jobs", 1)
        try:
            research_query = f"{goal_text} background and best approaches"
            research_results = self.research_agent.research(session_id, research_query, topk=3)
            self.jobs[session_id]["events"].append({"research": research_results})

            history = self.session_store.get_history(session_id)
            uploaded_files = [m["content"].split("uploads/")[-1] for m in history if "uploads/" in m["content"]] if history else []
            doc_outputs = []
            for file_entry in uploaded_files:
                path = "uploads/" + file_entry
                doc_out = self.document_agent.analyze(session_id, path)
                doc_outputs.append(doc_out)
                self.jobs[session_id]["events"].append({"document": doc_out})

            plan = f"Plan to accomplish: {goal_text}\nSteps:\n1) Research summary\n2) If docs, extract insights\n3) Produce deliverables\n"
            code_test = "print('uto quick test: ok')"
            code_out = self.code_agent.execute(session_id, code_test)
            self.jobs[session_id]["events"].append({"code_test": code_out})

            self.session_store.push_message(session_id, "director", plan)
            self.jobs[session_id]["state"] = "completed"
            self.jobs[session_id]["completed_at"] = time.time()
            self.jobs[session_id]["plan"] = plan
        except Exception as e:
            self.jobs[session_id]["state"] = "failed"
            self.jobs[session_id]["error"] = str(e)
        finally:
            record_metric("active_jobs", -1)

    def enqueue_document(self, session_id, file_path):
        self.session_store.push_message(session_id, "upload", file_path)

    def get_session_status(self, session_id):
        return self.jobs.get(session_id, {"state":"unknown"})
