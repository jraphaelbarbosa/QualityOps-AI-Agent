
import os
import sys
import signal

# Windows compatibility patch for crewai
if not hasattr(signal, 'SIGHUP'):
    signal.SIGHUP = 1
if not hasattr(signal, 'SIGTSTP'):
    signal.SIGTSTP = 1
if not hasattr(signal, 'SIGCONT'):
    signal.SIGCONT = 1
if not hasattr(signal, 'SIGQUIT'):
    signal.SIGQUIT = 1



# Ensure src is in path
sys.path.append(os.path.join(os.getcwd()))

try:
    from src.agents.crew import create_compliance_crew, get_llm
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def test_config():
    print("Testing LLM Configuration...")
    
    # Check if GEMINI_API_KEY is present (it should be in .env)
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY not found in .env")
        # We can't proceed without a key, but for the sake of the user's request,
        # verifying the code LOGIC is correct is the main thing.
        # But to run it, we need the key.
    else:
        print("GEMINI_API_KEY found.")

    try:
        crew = create_compliance_crew("Test transcription")
        print("Crew created successfully.")
        
        # Verify agents have the LLM
        for agent in crew.agents:
            print(f"Agent {agent.role} LLM: {agent.llm} (Type: {type(agent.llm)})")
            # If it's a string, it's correct for our new config
            if agent.llm == "gemini/gemini-1.5-flash":
                 print("SUCCESS: Agent using configured Gemini string.")
            elif hasattr(agent.llm, "model") and "gemini" in str(agent.llm.model):
                 print(f"SUCCESS: Agent using Gemini model: {agent.llm.model}")
            else:
                 print(f"INFO: Check if this is openai? {agent.llm}")

                
    except Exception as e:
        print(f"Error creating crew: {e}")

if __name__ == "__main__":
    test_config()
