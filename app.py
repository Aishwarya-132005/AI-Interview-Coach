
import streamlit as st
from pypdf import PdfReader
from llm import ask_ai
# from coach import analyze_profile, generate_questions, evaluate_answers
from coach import (
    analyze_profile,
    generate_questions,
    evaluate_answers,
    final_report
)
import json

# Display application title
st.title("AI Interview Coach")


# Read PDF resume
def read_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# Upload resume
Resume_file = st.file_uploader(
    "Upload your resume (PDF)!!",
    type="pdf"
)

# Enter job description
job_description = st.text_area(
    "Paste the job description",
    height=200
)


# Process uploaded resume
resume_text = ""

if Resume_file:
    resume_text = read_pdf(Resume_file)

    if resume_text.strip() == "":
        st.error("Resume is empty or could not be read. Try another file.")
    else:
        st.success("Resume uploaded successfully!")

        with st.expander("See extracted text"):
            st.text(resume_text)


# Analyze candidate profile
if Resume_file and resume_text.strip():
    if st.button("Analyze my profile"):
        if job_description.strip() == "":
            st.warning("Please paste a job description first.")
        else:
            with st.spinner("Analyzing your profile..."):
                st.session_state.pop("questions", None)
                st.session_state.pop("analysis", None)
                st.session_state.pop("interview_started", None)

                st.session_state.resume_text = resume_text
                st.session_state.job_description = job_description

                st.session_state.analysis = analyze_profile(
                    resume_text,
                    job_description
                )


# Additional resume analysis
if Resume_file and resume_text.strip() and job_description.strip():
    if st.button("Analyze Resume"):
        prompt = f"""
        You are an expert interview coach.
        Analyze the candidate's resume against the job description.

        RESUME:
        {resume_text}

        JOB DESCRIPTION:
        {job_description}

        Provide:
        1. A short summary of the candidate.
        2. Key skills found in the resume.
        3. Skills required by the job description.
        4. Matching skills.
        5. Missing skills.
        6. Overall suitability for the role.
        7. Areas the candidate should prepare for the interview.
        """

        with st.spinner("Analyzing resume..."):
            analysis = ask_ai(prompt)

        st.subheader("Resume analysis")
        st.write(analysis)


# Display profile analysis
if "analysis" in st.session_state:
    a = st.session_state.analysis

    st.header(f"Profile analysis: {a.get('Role', 'Role')}")

    st.metric(
        "Match score",
        f"{a.get('Match score', 0)}%"
    )

    st.write(a.get("Summary", ""))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Matching skills")

        for skill in a.get("Matching skills", []):
            st.write("-", skill)

    with col2:
        st.subheader("Missing skills")

        for skill in a.get("Missing skills", []):
            st.write("-", skill)

    with st.expander("View full JSON response"):
        st.json(a)


# Generate interview questions
if "analysis" in st.session_state:
    st.divider()
    st.header("Interview questions")

    num = st.slider(
        "How many questions",
        min_value=3,
        max_value=10,
        value=5
    )

    if st.button("Generate questions"):
        st.session_state.pop("questions", None)
        st.session_state.pop("evaluations", None)
        st.session_state.interview_started = False

        with st.spinner("Generating questions..."):
            result = generate_questions(
                st.session_state.analysis,
                st.session_state.resume_text,
                st.session_state.job_description,
                num
            )

            # Extract questions from JSON response
            if isinstance(result, dict):
                st.session_state.questions = result.get(
                    "questions", []
                )
            else:
                st.session_state.questions = []

        if not st.session_state.questions:
            st.error(
                "No questions were generated. "
                "Please try generating them again."
            )


# Display generated questions and start interview
if (
    "questions" in st.session_state
    and st.session_state.questions
):
    questions = st.session_state.questions

    st.success(f"{len(questions)} questions are ready.")

    if not st.session_state.get("interview_started", False):
        if st.button("Start Interview"):
            st.session_state.pop("evaluations", None)

            st.session_state.interview_started = True
            st.session_state.current_q = 0
            st.session_state.answers = []
            st.session_state.message = []

            st.session_state.message.append({
                "role": "assistant",
                "contents": "Let's Begin"
            })

            first_q = questions[0].get("questions", "")

            st.session_state.message.append({
                "role": "assistant",
                "contents": f"**Q1.** {first_q}"
            })

            st.rerun()


# Interview flow
if (
    "questions" in st.session_state
    and st.session_state.get("interview_started", False)
):
    st.divider()
    st.header("Interview")

    questions = st.session_state.questions
    current = st.session_state.current_q
    total = len(questions)

    if total > 0:
        st.progress(
            min(current / total, 1.0),
            text=f"Answered {current} of {total}"
        )

        # Display conversation
        for msg in st.session_state.message:
            with st.chat_message(msg["role"]):
                st.markdown(msg["contents"])

        # Collect candidate answer
        if current < total:
            answer = st.chat_input("Type your answer:")

            if answer:
                q = questions[current]

                st.session_state.message.append({
                    "role": "user",
                    "contents": answer
                })

                st.session_state.answers.append({
                    "question": q.get("questions", ""),
                    "type": q.get("type", ""),
                    "skill": q.get("skill", ""),
                    "answer": answer
                })

                st.session_state.current_q += 1
                nxt = st.session_state.current_q

                if nxt < total:
                    next_text = (
                        f"**Q{nxt + 1}.** "
                        f"{questions[nxt].get('questions', '')}"
                    )

                    st.session_state.message.append({
                        "role": "assistant",
                        "contents": next_text
                    })
                else:
                    st.session_state.message.append({
                        "role": "assistant",
                        "contents": (
                            "That's the end of the interview. Thank you!"
                        )
                    })

                st.rerun()

        else:
            st.success("Interview complete!")

            # Evaluate interview answers
            if st.button("Evaluate my answers"):
                with st.spinner("Evaluating your answers..."):
                    st.session_state.evaluations = evaluate_answers(
                        st.session_state.answers,
                        st.session_state.analysis.get("Role", "this role")
                    )

            # Display evaluation
            
            if "evaluations" in st.session_state:
                st.subheader("Interview evaluation")

                result = st.session_state.evaluations

                if isinstance(result, dict):
                    evals = result.get("evaluations", [])
                else:
                    evals = result

                st.session_state.evaluations = evals

                for i, e in enumerate(evals, start=1):
                    st.markdown(f"### Answer {i}")

                    for area in ["relevance", "depth", "clarity", "examples"]:
                        st.write(f"**{area.title()}:** {e.get(area, 0)}/10")

                    st.write("**Feedback:**", e.get("feedback", ""))
                    st.write("**Suggestion:**", e.get("suggestion", ""))
                    st.divider()

    else:
        st.warning("No questions are available. Generate questions again.")


# Final scorecard and improvement plan
if (
    st.session_state.get("interview_started", False)
    and "evaluations" in st.session_state
):
    st.divider()
    st.header("Final Scorecard")

    evals = st.session_state.evaluations

    if evals:
        # Calculate each answer's average out of 10
        answer_scores = [
            sum(e.get(area, 0) for area in
                ["relevance", "depth", "clarity", "examples"]) / 4
            for e in evals
        ]

        overall = round(sum(answer_scores) / len(answer_scores), 1)

        if overall >= 7.5:
            readiness = "Ready for interviews"
        elif overall >= 5:
            readiness = "Almost ready; more practice recommended"
        else:
            readiness = "More practice needed"

        analysis = st.session_state.analysis

        col1, col2 = st.columns(2)

        col1.metric("Interview Score", f"{overall}/10")
        col2.metric(
            "Resume Match",
            f"{analysis.get('Match score', 0)}%"
        )

        st.subheader(readiness)

        st.markdown("### Score by Rubric Area")

        for area in ["relevance", "depth", "clarity", "examples"]:
            avg = sum(e.get(area, 0) for e in evals) / len(evals)
            st.write(f"{area.title()}: {avg:.1f}/10")
            st.progress(min(max(avg / 10, 0.0), 1.0))

        # Generate personalized improvement plan
        if st.button("Get My Improvement Plan"):
            with st.spinner("Preparing your personal feedback..."):
                report = final_report(
                    analysis,
                    st.session_state.answers,
                    evals
                )
                st.session_state.report = report

        # Display improvement plan
        if "report" in st.session_state:
            report = st.session_state.report

            st.markdown("### Strengths")
            for item in report.get("strengths", []):
                st.write("-", item)

            st.markdown("### Areas to Improve")
            for item in report.get("improvements", []):
                st.write("-", item)

            st.markdown("### Study Plan")
            for item in report.get("study_plan", []):
                st.write("-", item)

            st.success(report.get("message", "Keep practising!"))

            # Prepare downloadable scorecard
            lines = [
                "AI INTERVIEW COACH - SCORECARD",
                f"Role: {analysis.get('Role', '')}",
                f"Interview Score: {overall}/10",
                f"Resume Match: {analysis.get('Match score', 0)}%",
                f"Readiness: {readiness}",
                "",
                "ANSWER SCORES:"
            ]

            for i, score in enumerate(answer_scores, start=1):
                lines.append(f"Answer {i}: {score:.1f}/10")

            lines.extend(["", "STRENGTHS:"])
            lines.extend(
                f"- {x}" for x in report.get("strengths", [])
            )

            lines.extend(["", "AREAS TO IMPROVE:"])
            lines.extend(
                f"- {x}" for x in report.get("improvements", [])
            )

            lines.extend(["", "STUDY PLAN:"])
            lines.extend(
                f"- {x}" for x in report.get("study_plan", [])
            )

            st.download_button(
                "Download Scorecard",
                data="\n".join(lines),
                file_name="interview_scorecard.txt",
                mime="text/plain"
            )

    else:
        st.warning("No evaluations found. Please evaluate your answers first.")