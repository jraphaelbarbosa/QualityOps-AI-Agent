# Intelligent QA & Compliance Agent

An enterprise-grade AI agent powered by CrewAI and Google Gemini 2.0 Flash to audit customer support interactions for compliance and quality assurance.

## Features
- **Automated Auditing**: Detects security violations (e.g., PIN handling) and compliance gaps.
- **RAG Integration**: Uses Retrieval-Augmented Generation to check against specific support guidelines.
- **Interactive Dashboard**: Real-time auditing via Streamlit.

## Setup & Run

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment**
    - Copy `.env.example` to `.env`
    - Add your `GEMINI_API_KEY`.

3.  **Run the Dashboard**
    ```bash
    streamlit run src/app.py
    ```

    > **Tip:** Use the **"Load Bad Example"** button in the UI for a quick demonstration of security violations and coaching feedback.
