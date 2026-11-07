AI Interview Coach
An AI-powered mock interview application built with Python,
Streamlit, and the Google Gemini API. It helps candidates
compare their resume with a job description, practise personalized
interview questions, receive answer feedback, and generate an
improvement plan.

Features
- PDF resume upload: Extracts text from an uploaded PDF resume.
- Job description input: Accepts the job description for the
  target role.
- Resume-to-job analysis: Identifies matching skills, missing
  skills, a role summary, and an AI-generated match score.
- Additional resume analysis: Produces a more detailed comparison
  of the resume and job description.
- Personalized interview questions: Generates a configurable
  number of questions based on the candidate's resume, job
  description, and skill gaps.
- Interactive mock interview: Presents questions in a chat-style
  interface and records the candidate's answers.
- Answer evaluation: Evaluates each answer on relevance, depth,
  clarity, and examples, with feedback and suggestions.
- Final scorecard: Calculates an overall interview score and
  displays readiness guidance.
- Personalized improvement plan: Summarizes strengths, areas to
  improve, and a suggested study plan.
- Scorecard download: Allows the candidate to download the
  scorecard as a text file.
  
Technology Stack
  Component               Technology
  Programming language    Python
User interface          Streamlit
Generative AI           Google Gemini API
AI integration          Google GenAI Python SDK
PDF text extraction     PyPDF
Environment variables   python-dotenv

The model configured in llm.py is gemini-3.5-flash-lite.
Project Structure
AI-Interview-Coach/
│
├── app.py              # Streamlit application and interview workflow
├── coach.py            # Resume analysis, question generation and evaluation
├── llm.py               # Google Gemini API integration
├── requirements.txt     # Python dependencies
├── .env                 # API key (create locally; do not commit)
├── .gitignore
└── README.md

Prerequisites
- Python installed on your computer.
- A Google Gemini API key.
- Git installed (for pushing the project to GitHub).
Setup and Installation
1. Clone the repository
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
If you are setting up the project locally before creating a GitHub
repository, skip this step and open a terminal in the project folder.
2. Create and activate a virtual environment
Windows (Command Prompt):
python -m venv .venv
.venv\Scripts\activate
Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1
macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure the Gemini API key
Create a file named .env in the project root:
GEMINI_API_KEY=your_gemini_api_key_here
Replace the placeholder with your own API key. Keep this file private
and never upload it to GitHub.
5. Run the application
streamlit run app.py
Streamlit will display a local URL in the terminal. Open that URL in
your browser.

How to Use
1. Start the application.
2. Upload your resume in PDF format.
3. Paste the job description for the role you are targeting.
4. Select Analyze my profile to view the profile analysis and match
   score.
5. Optionally select Analyze Resume for an additional resume
   comparison.
6. Choose the number of interview questions and select Generate
   questions.
7. Select Start Interview and answer each question in the chat
   interface.
8. After completing the interview, select Evaluate my answers.
9. Review the answer-level feedback and final scorecard.
10. Select Get My Improvement Plan to view your strengths,
    improvement areas, and study plan.
11. Download the scorecard as a text file.
