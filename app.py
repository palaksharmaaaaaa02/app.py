import streamlit as st
import pdfplumber
import pandas as pd
from datetime import datetime

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- CUSTOM STYLING ---------------- #
st.markdown("""
<style>

.main {
    padding: 2rem;
}

.stApp {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
}

.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}

.skill {
    background-color: #334155;
    padding: 8px 14px;
    border-radius: 8px;
    display: inline-block;
    margin: 5px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.title("📄 AI Resume Analyzer")
st.write(
    "Upload your resume to receive ATS-style analysis, "
    "skill insights, and role recommendations."
)

# ---------------- ROLE DATABASE ---------------- #
roles = {

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "tailwind",
        "typescript"
    ],

    "Backend Developer": [
        "python",
        "java",
        "node",
        "sql",
        "api",
        "mongodb"
    ],

    "Data Scientist": [
        "python",
        "machine learning",
        "pandas",
        "numpy",
        "tensorflow",
        "sql"
    ],

    "AI Engineer": [
        "python",
        "deep learning",
        "nlp",
        "pytorch",
        "tensorflow",
        "machine learning"
    ]
}

# ---------------- FILE UPLOAD ---------------- #
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# ---------------- PDF TEXT EXTRACTION ---------------- #
def extract_text(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            content = page.extract_text()

            if content:
                text += content.lower()

    return text

# ---------------- ANALYSIS FUNCTION ---------------- #
def analyze_resume(text):

    best_role = ""
    best_score = 0
    detected_skills = []

    for role, skills in roles.items():

        matched = []

        for skill in skills:

            if skill in text:
                matched.append(skill)

        score = int(
            (len(matched) / len(skills)) * 100
        )

        if score > best_score:

            best_score = score
            best_role = role
            detected_skills = matched

    missing_skills = [

        skill for skill in roles[best_role]

        if skill not in detected_skills
    ]

    return (
        best_role,
        best_score,
        detected_skills,
        missing_skills
    )

# ---------------- MAIN APP ---------------- #
if uploaded_file:

    st.success("Resume uploaded successfully.")

    resume_text = extract_text(uploaded_file)

    (
        best_role,
        best_score,
        detected_skills,
        missing_skills
    ) = analyze_resume(resume_text)

    # ---------------- DASHBOARD ---------------- #
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="🎯 Recommended Role",
            value=best_role
        )

    with col2:
        st.metric(
            label="📊 ATS Score",
            value=f"{best_score}%"
        )

    with col3:
        st.metric(
    label="📌 Skills Identified",
    value=len(detected_skills)
)

    st.divider()

    # ---------------- SCORE BAR ---------------- #
    st.subheader("ATS Compatibility Score")

    st.progress(best_score / 100)

    if best_score >= 80:
        st.success(
            "Your resume is well optimized for ATS systems."
        )

    elif best_score >= 60:
        st.warning(
            "Your resume is good but can be improved further."
        )

    else:
        st.error(
            "Your resume requires more relevant technical skills."
        )

    st.divider()

    # ---------------- DETECTED SKILLS ---------------- #
    st.subheader("Detected Skills")

    for skill in detected_skills:

        st.markdown(
            f"<span class='skill'>✅ {skill}</span>",
            unsafe_allow_html=True
        )

    st.divider()

    # ---------------- MISSING SKILLS ---------------- #
    st.subheader("Suggested Skills to Add")

    if missing_skills:

        for skill in missing_skills:

            st.markdown(
                f"<span class='skill'>⚠️ {skill}</span>",
                unsafe_allow_html=True
            )

    else:
        st.success(
            "No major missing skills detected."
        )

    st.divider()

    # ---------------- ANALYTICS TABLE ---------------- #
    st.subheader("Skill Analysis Report")

    report_df = pd.DataFrame({

        "Detected Skills": pd.Series(
            detected_skills
        ),

        "Suggested Skills": pd.Series(
            missing_skills
        )
    })

    st.dataframe(
    report_df,
    use_container_width=True,
    hide_index=True
)

    st.divider()

    # ---------------- RESUME TIPS ---------------- #
    st.subheader("Professional Resume Tips")

    tips = [

        "Use measurable achievements in projects.",

        "Add GitHub and LinkedIn profile links.",

        "Keep formatting simple and ATS-friendly.",

        "Mention certifications and internships.",

        "Use strong action verbs such as "
        "'Developed', 'Built', and 'Implemented'."
    ]

    for tip in tips:
        st.write(f"• {tip}")

    st.divider()

    # ---------------- DOWNLOAD REPORT ---------------- #
    report = f"""
AI Resume Analyzer Report
Generated On: {datetime.now()}

Recommended Role:
{best_role}

ATS Score:
{best_score}%

Detected Skills:
{", ".join(detected_skills)}

Suggested Skills:
{", ".join(missing_skills)}
"""

    st.download_button(

        label="⬇ Download Analysis Report",

        data=report,

        file_name="resume_analysis_report.txt"
    )

else:
    st.info(
        "Upload a PDF resume to begin analysis."
    )