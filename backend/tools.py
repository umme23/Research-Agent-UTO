# tools.py - PDF extraction, web search stub, code executor
import os, subprocess, json
from pdfminer.high_level import extract_text

def web_search(query, max_results=5):
    # Replace with SerpAPI/Bing integration for production
    return [{"title": f"Result for {query}", "snippet": "This is a stub. Replace with SerpAPI results", "url": "http://example.com"}]

def extract_text_from_pdf(path):
    try:
        text = extract_text(path)
        return text
    except Exception as e:
        return f"PDF extraction error: {e}"

def run_python_code(code: str):
    try:
        proc = subprocess.run(["python","-c", code], capture_output=True, text=True, timeout=10)
        return {"stdout": proc.stdout, "stderr": proc.stderr, "returncode": proc.returncode}
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Timeout", "returncode": -1}
