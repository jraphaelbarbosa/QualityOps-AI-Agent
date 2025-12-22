# QualityOps AI - Enterprise Compliance Auditor 🛡️

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-orange)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-magenta)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)

**QualityOps** is an autonomous AI agent designed to revolutionize Quality Assurance (QA) in Customer Support. Unlike traditional manual sampling (auditing ~2% of calls), QualityOps scales to audit **100% of interactions** in real-time, detecting security violations, PII leaks, and compliance gaps.

---

## 🚀 Key Features

* **⚡ High-Performance Auditing:** Powered by **LangChain LCEL** for low-latency analysis (<2s per audit).
* **🧠 Advanced Reasoning:** Utilizes **Google Gemini 2.5 Flash** to understand context, verifying not just keywords but logical security flows (e.g., "Did the agent verify PIN *before* sharing data?").
* **🛡️ Security First:** Detects PII leaks (Credit Cards, SSN) and enforces PCI-DSS/GDPR compliance protocols.
* **📊 Enterprise Dashboard:** A modern, Dark Mode UI built with Streamlit for real-time monitoring and feedback.
* **🎓 Automated Coaching:** Generates constructive, actionable feedback for human agents based on the detected errors.

---

## 🛠️ Tech Stack

* **Orchestration:** LangChain (LCEL - LangChain Expression Language)
* **LLM (Brain):** Google Gemini 2.5 Flash (via `langchain-google-genai`)
* **Frontend:** Streamlit (Custom Enterprise Theme)
* **Parsing:** Pydantic & JsonOutputParser for structured data extraction
* **Environment:** Python 3.11+

---

## ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/jraphaelbarbosa/QualityOps-AI-Agent.git
    cd QualityOps-AI-Agent
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    * Create a `.env` file in the root directory.
    * Add your Google API Key:
        ```ini
        GEMINI_API_KEY=AIzaSy...
        ```

4.  **Run the Dashboard**
    ```bash
    streamlit run src/app.py
    ```

---

## 🧪 How to Test

1.  Open the dashboard (usually `http://localhost:8501`).
2.  Click **"🚨 Load Bad Example"** in the sidebar to simulate a non-compliant chat (Security Failure).
3.  Click **"▶️ Run Audit"**.
4.  Observe the AI detecting the missing PIN verification and generating coaching feedback.

---

## 📸 Screenshots

*(Add your screenshots here)*

---

**Author:** João Raphael Barbosa
*Built publicly as part of an AI Engineering Portfolio.*
