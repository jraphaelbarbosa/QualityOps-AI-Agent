import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from google.api_core.exceptions import NotFound

load_dotenv()

# Setup Parser
parser = JsonOutputParser()

def run_audit_chain(chat_text: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {
            "score": 0,
            "security_violation": True,
            "violations": ["Configuration Error: GEMINI_API_KEY missing"],
            "coaching_feedback": "Check .env file.",
            "corrected_response": "N/A"
        }

    try:
        # Initialize Gemini 2.5 Flash
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
            max_retries=1
        )

        # Define Prompt
        prompt = PromptTemplate(
            template="""
            You are a QA Compliance Auditor. Analyze the following Customer Support interaction.
            
            TRANSCRIPT:
            "{chat_log}"
            
            INSTRUCTIONS:
            1. Check if the Agent asked for a PIN/verification before accessing account data.
            2. Check for PII leaks.
            3. Rate the interaction from 0 to 100.
            
            OUTPUT FORMAT (Strict JSON):
            {{
                "score": int,
                "security_violation": boolean,
                "violations": [list of strings],
                "coaching_feedback": string,
                "corrected_response": string
            }}
            """,
            input_variables=["chat_log"]
        )

        # Execute Chain
        chain = prompt | llm | parser
        return chain.invoke({"chat_log": chat_text})

    except NotFound:
        return {
            "score": 0,
            "security_violation": True,
            "violations": ["System Error: Model 'gemini-1.5-flash' not found. Please run 'pip install -U langchain-google-genai'"],
            "coaching_feedback": "Library update required.",
            "corrected_response": "N/A"
        }
    except Exception as e:
        return {
            "score": 0,
            "security_violation": True,
            "violations": [f"Error: {str(e)}"],
            "coaching_feedback": "See terminal logs.",
            "corrected_response": "N/A"
        }
