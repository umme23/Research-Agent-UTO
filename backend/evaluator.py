# evaluator.py - basic integration test
import time
from director import Director
from memory import SessionStore

def run_unit_tests():
    ss = SessionStore()
    d = Director(session_store=ss)
    sid = "test-session-1"
    d.create_session(sid, "tester")
    d.enqueue_document(sid, "sample_docs/sample_report.pdf")
    d.start_job(sid, "Generate executive summary for uploaded PDF and list 5 action items", "tester")
    time.sleep(3)
    status = d.get_session_status(sid)
    print("Status:", status)

if __name__ == "__main__":
    run_unit_tests()

frontend/package.json
{
  "name": "uto-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "13.4.10",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "tailwindcss": "^3.4.7",
    "postcss": "^8.4.23",
    "autoprefixer": "^10.4.14",
    "axios": "^1.4.0",
    "clsx": "^1.2.1",
    "framer-motion": "^10.12.16",
    "@headlessui/react": "^1.8.8",
    "@heroicons/react": "^2.0.18"
  }
}
