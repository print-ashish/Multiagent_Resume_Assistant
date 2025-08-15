from langgraph_supervisor import create_supervisor
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langgraph.prebuilt import create_react_agent
import uuid

from tools import read_pdf

load_dotenv()


class ResumeAnalysisMutiagent:
    def __init__(self, db_path: str = "checkpoints.sqlite"):
        """Initialize agents, memory, and supervisor."""
        # Resume Reader Agent
        self.resume_reader_agent = create_react_agent(
            model=ChatGoogleGenerativeAI(model="gemini-2.0-flash"),
            tools=[self.fetch_and_read_resume],
            prompt=(
                """
                You are a PDF resume fetching and reader agent.

                INSTRUCTIONS:
                - Use the fetch_and_read_resume tool to fetch resume content.
                - Analyze the resume content and pass it to the supervisor.
                """
            ),
            name="resume_reader_agent",
        )

        # Analysis Agent
        self.analysis_agent = create_react_agent(
            model=ChatGoogleGenerativeAI(model="gemini-2.0-flash"),
            tools=[],
            prompt=(
                """
                You are a job description analysis agent.

                INSTRUCTIONS:
                - Compare job description with the resume content.
                - Provide skill gaps, resume issues, and improvements.
                - Format your response as:
                  **Pros**, **Gaps**, **Improvement**, **Overall**
                """
            ),
            name="analysis_agent",
        )
        self.chat_agent = create_react_agent(
        model=ChatGoogleGenerativeAI(model="gemini-2.0-flash"),
        tools=[],
        prompt=(
            """
            You are a helpful chat agent.

            INSTRUCTIONS:
            - Engage in multi-turn conversation with the user.
            - Answer their queries based on job description and resume analysis.
            - Provide guidance, improvements, and career advice.
            """
        ),
        name="chat_agent",
    )

        # Database + Memory
        conn = sqlite3.connect(db_path, check_same_thread=False)
        self.memory = SqliteSaver(conn)

        # Thread ID for tracking
        self.thread_id = uuid.uuid4()
        self.config = {"configurable": {"thread_id": self.thread_id}}

        # Supervisor setup
        self.supervisor = create_supervisor(
            model=ChatGoogleGenerativeAI(model="gemini-2.5-flash"),
            agents=[self.resume_reader_agent, self.analysis_agent , self.chat_agent],
            prompt=(
                """
                You are a supervisor managing two agents:

                Workflow:
                1. Receive job description from user.
                2. Call resume_reader_agent to fetch resume.
                3. Pass resume + JD to analysis_agent.
                4. Return the final structured report.
                If user asks questions → forward to Chat Agent with context.
                """
            ),
            add_handoff_back_messages=True,
            output_mode="full_history",
        ).compile(checkpointer=self.memory)

    @staticmethod
    def fetch_and_read_resume():
        """Tool: Fetch and return resume content."""
        print("Fetching resume...")
        content = read_pdf()
        print("Resume content fetched.")
        return content

    def run(self, jd: str, thread_id:str) -> str:
        """Run pipeline on given job description."""
        config = {"configurable": {"thread_id": thread_id}}
        response = self.supervisor.invoke({"messages": [("user", jd)]}, config)
        return response["messages"][-1].content


# -------------------------------
# USAGE
# -------------------------------
# if __name__ == "__main__":
#     jd = """About the job
#     What You Will Do
#     · Build features end to end from backend services to frontend UIs to quick automation scripts.
#     · Prototype, test, and iterate quickly.
#     · Explore new tools, APIs, or frameworks to get the job done.
#     · Work across different problem areas – from product to data to devops.
#     · Think and shape the product, not just write code

#     Must have:
#     · Can code fluently in at least one language and are not afraid to learn others.
#     · Have built something end to end: a personal project, open-source tool, or internal tool at work.
#     · Are up to date on all things AI and experience of building AI solutions
#     · Love exploring new ideas and figuring out how to make them work.
#     · Experience with working & deploying solutions on any one of the cloud platforms.
#     · Good communication skills

#     Bonus points for:
#     · Working on side projects or hackathons.
#     · Being comfortable with AI tools, APIs, web scraping, automation.
#     · Having a GitHub portfolio, or something online we can see.

#     What we offer:
#     · Opportunity to plan, build & deploy products that have a real-world impact.
#     · Small team, no micromanagement, no fluff. Just smart people building things that matter.
#     · Remote/Hybrid Setup based on candidate’s preference with reasonable working hours.
#     · Compensation aligned with market standards.
#     """

#     agent = ResumeAnalysisMutiagent()
#     report = agent.run(jd)
#     print("\n--- FINAL REPORT ---\n")
#     print(report)
