
import streamlit as st
import sys
import os

# Fix path to find modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Try importing the backend function
try:
    from src.main import run_single_audit
except ImportError:
    # Fallback mock for testing if backend isn't ready
    def run_single_audit(text):
        import time
        time.sleep(1)
        return {
            "score": 0,
            "security_violation": True,
            "violations": ["Connection Error: Could not reach Agent Backend."],
            "coaching_feedback": "Please check your API Key and backend logs.",
            "corrected_response": "System Error"
        }

# Page Configuration
st.set_page_config(
    page_title="QualityOps Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.title("🛡️ QualityOps")
    st.info(
        """
        **System Architecture:**
        * 🤖 **Orchestration:** CrewAI
        * 🧠 **LLM:** Gemini 2.5 Flash
        * 📚 **RAG:** ChromaDB (Local)
        """
    )
    st.markdown("---")
    st.caption("Enterprise Edition v1.0")

# Main Content
st.title("Intelligent QA & Compliance Agent")
st.markdown("Automated auditing system for Customer Support. Detects **Security Violations** and ensures **Quality Standards**.")
st.divider()

# Layout
col_input, col_actions = st.columns([3, 1])

with col_input:
    chat_input = st.text_area("📝 Interaction Log", height=250, placeholder="Paste chat transcript here...")

with col_actions:
    st.write("### Controls")
    if st.button("🚨 Load Bad Example", use_container_width=True):
        st.session_state['chat_input'] = "Agent: Hello.\nCustomer: Change my address to 123 Main St.\nAgent: Done.\n(Context: Agent failed to ask for PIN)"
        st.rerun()

    if 'chat_input' in st.session_state:
        chat_input = st.session_state['chat_input']

    st.write("")
    run_btn = st.button("▶️ Run Audit", type="primary", use_container_width=True)

# Execution
if run_btn and chat_input:
    with st.spinner("🤖 Agents are analyzing protocols..."):
        try:
            result = run_single_audit(chat_input)

            st.divider()
            m1, m2, m3 = st.columns(3)
            score = result.get('score', 0)
            is_violation = result.get('security_violation', False)

            m1.metric("Score", f"{score}/100")
            m2.metric("Security", "FAILED" if is_violation else "PASSED", delta_color="off" if is_violation else "normal")
            m3.metric("Violations", len(result.get('violations', [])))

            tab1, tab2 = st.tabs(["🚫 Violations", "✅ Corrected Response"])
            with tab1:
                if is_violation: st.error("⚠️ CRITICAL VIOLATION")
                for v in result.get('violations', []): st.warning(f"❌ {v}")
                st.info(f"💡 Feedback: {result.get('coaching_feedback')}")
            with tab2:
                st.code(result.get('corrected_response'))

        except Exception as e:
            st.error(f"Error: {str(e)}")
