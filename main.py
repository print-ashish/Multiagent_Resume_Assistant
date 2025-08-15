import os
import uuid
import streamlit as st
from pathlib import Path
from multiagent import ResumeAnalysisMutiagent  # <-- Import your class

# Ensure resume folder exists
RESUME_DIR = Path("resumes")
RESUME_DIR.mkdir(exist_ok=True)

# Page config
st.set_page_config(page_title="Resume vs JD Analyzer", page_icon="📄", layout="centered")

# Generate thread_id once per session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())  # Unique ID for current page session

# Sidebar instructions
with st.sidebar:
    st.title("ℹ️ How to Use")
    st.markdown(
        """
        1. **Upload** your resume (PDF).  
        2. **Paste** the Job Description.  
        3. Click **Analyze** to generate a comparison.  

        ✅ Pro tip: Use a detailed JD for better results.
        """
    )
    st.info(f"🔗 Session Thread ID: `{st.session_state.thread_id}`")

# Main title
st.title("📄 Resume vs Job Description Analyzer")
st.caption("Compare your resume with the given JD using AI-powered multi-agent analysis")

st.divider()

# Upload Resume
uploaded_file = st.file_uploader("📤 Upload your Resume", type=["pdf"])

resume_path = None
if uploaded_file is not None:
    resume_path = RESUME_DIR / "resume.pdf"   # always save as resume.pdf
    with open(resume_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Resume saved successfully!")

# JD Input
jd = st.text_area("📝 Paste the Job Description here or Ask the Question", height=250, placeholder="Enter the full job description...")

# Analyze Button
analyze_clicked = st.button("Send", key="analyze_btn")

if analyze_clicked:
    if resume_path and jd.strip():
        with st.spinner("⏳ Processing your request... please wait"):
            pipeline = ResumeAnalysisMutiagent()
            # Pass thread_id here
            report = pipeline.run(jd, thread_id=st.session_state.thread_id)

        st.divider()
        st.subheader("📊 Multiagent Response")
        st.markdown(report)

        # st.success("✨  complete successfully!")

    else:
        st.error("⚠️ Please upload a resume and enter a job description before analyzing.")
