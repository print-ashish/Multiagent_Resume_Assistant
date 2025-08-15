

https://github.com/user-attachments/assets/b2318ee2-d2de-48fc-be76-28c2a91a9206

# 📄 Resume vs Job Description Multi-Agent Analyzer

An **AI-powered multi-agent system** built with [LangGraph](https://python.langchain.com/docs/langgraph), [LangChain](https://www.langchain.com/), and [Streamlit](https://streamlit.io/).  
The system analyzes a candidate’s resume against a given Job Description (JD), identifies **skill gaps**, highlights **pros & improvements**, and allows **chat-based interaction** with an AI assistant for tailored career guidance.  

---

## 🚀 Features

- **Multi-Agent Architecture**:
  - **Resume Reader Agent** → extracts and preprocesses resume content.  
  - **Analysis Agent** → compares resume against JD and outputs Pros, Gaps, Improvements, and Overall Fit.  
  - **Chat Agent** → engages in interactive conversation with the user, answers queries, and suggests improvements.  
  - **Supervisor Agent** → orchestrates the workflow and coordinates between agents.  

- **Interactive Web UI** (Streamlit):
  - Upload your resume (PDF).  
  - Enter/paste a job description.  
  - Get a structured analysis report.  
  - Ask follow-up questions in a chat interface.  

- **Persistent Memory**:
  - Uses SQLite to checkpoint and maintain agent conversation history.  

---

## 🛠️ Tech Stack

- **LLM**: Google Gemini (`gemini-2.0-flash`) via `langchain-google-genai`  
- **Orchestration**: [LangGraph](https://python.langchain.com/docs/langgraph) + Supervisor Agent  
- **Frontend**: [Streamlit](https://streamlit.io/)  
- **Storage**: SQLite (via LangGraph’s `SqliteSaver`)  
- **PDF Parsing**: PyPDF2  

---

## 📂 Project Structure

```
📦 Resume-Agent-Assistant
│
├── resume_pipeline.py      # Class-based multi-agent pipeline
├── app.py                  # Streamlit frontend
├── tools.py                # Utility functions (e.g., PDF reader)
├── checkpoints.sqlite      # SQLite memory (auto-created)
├── resume/                 # Uploaded resumes stored here
├── README.md               # Documentation
└── requirements.txt        # Dependencies
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resume-assistant.git
   cd resume-assistant
   ```

2. **Create a virtual environment & install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate

   pip install -r requirements.txt
   ```

3. **Environment Variables**  
   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Run the Streamlit app**
   ```bash
   streamlit run main.py
   ```

---

## 🖥️ Usage

1. Open the Streamlit app in your browser.  
2. Upload your **resume.pdf** (saved automatically into `resume/`).  
3. Paste the **Job Description (JD)** in the text box.  
4. Click **Analyze** to get:
   - ✅ Pros  
   - ⚠️ Skill Gaps  
   - 🔧 Suggested Improvements  
   - 📊 Overall Fit  

5. Use the **chat interface** to:
   - Ask resume improvement suggestions  
   - Generate tailored summaries or cover letters  
   - Get advice on which skills to learn  

---

## 📊 Example Output

**Pros**  
- Strong Python + AI project background  
- Cloud deployment experience  

**Gaps**  
- Limited exposure to frontend frameworks mentioned in JD  
- Missing DevOps/automation tools  

**Improvements**  
- Add recent project details showcasing end-to-end AI solution building  
- Highlight collaboration/communication skills more strongly  

**Overall**  
- Good fit for AI Engineer roles with slight upskilling needed in cloud/DevOps.  

---

## 🧩 Future Enhancements
- Add a **Cover Letter Agent** to auto-generate tailored cover letters.  
- Integrate real **job postings APIs** (LinkedIn/Indeed) for live JD analysis.  
- Add **visualization dashboards** (e.g., skill radar charts).  
- Expand **memory** to support multi-session career coaching.  

---

## 🤝 Contributing

Pull requests are welcome! If you’d like to suggest improvements, open an issue first to discuss what you’d like to change.  

---

## 📜 License

This project is licensed under the MIT License.  

---

💡 Built with ❤️ by an aspiring **Generative AI & Multi-Agent Systems Engineer**
