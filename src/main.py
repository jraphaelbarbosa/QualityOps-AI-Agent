import sys
import os
import signal
import json
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = "NA" # Dummy key to bypass CrewAI check

# Windows compatibility patch for crewai
if sys.platform.startswith("win"):
    if not hasattr(signal, "SIGHUP"):
        signal.SIGHUP = 1  # Dummy value
    if not hasattr(signal, "SIGQUIT"):
        signal.SIGQUIT = 3 # Dummy value
    if not hasattr(signal, "SIGCONT"):
        signal.SIGCONT = 18 # Dummy value
    if not hasattr(signal, "SIGTSTP"):
        signal.SIGTSTP = 20 # Dummy value

# Add src to pythonpath
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.agents.crew import create_compliance_crew

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
LOGS_PATH = os.path.join(DATA_DIR, "mock_chat_logs.json")

def load_logs():
    with open(LOGS_PATH, 'r') as f:
        return json.load(f)

def run_audit():
    """
    CLI entry point to run audits on all logs in mock_chat_logs.json.
    """
    logs = load_logs()
    print(f"Loaded {len(logs)} chat logs for audit.\n")
    
    for log in logs:
        print("="*60)
        print(f"Starting Audit for ID: {log['id']} ({log['description']})")
        print("="*60)
        
        result = run_single_audit(log['audio_transcription'])
        
        print("\n--- Compliance Result ---")
        print(json.dumps(result, indent=2))
        print("\n" + "-"*60 + "\n")

def run_single_audit(chat_text: str) -> dict:
    """
    Exposes the audit logic for external tools (e.g., Streamlit).
    Returns the result as a Python dictionary.
    """
    try:
        crew = create_compliance_crew(chat_text)
        result = crew.kickoff()
        
        # result is a ComplianceResult pydantic model (due to output_pydantic)
        if hasattr(result, 'model_dump'):
            return result.model_dump()
        elif hasattr(result, 'to_dict'):
            return result.to_dict()
        else:
            # Fallback for unexpected types
            try:
                return json.loads(str(result))
            except:
                return {"error": "Could not parse result", "raw": str(result)}
                
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    run_audit()
