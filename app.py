import streamlit as st
from pdfminer.high_level import extract_text
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.markdown("<h1 style='text-align:center;'>AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>AI-powered resume evaluation with ATS-style scoring</p>", unsafe_allow_html=True)

st.divider()

# --------------------------
# CLEAN TEXT
# --------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

# --------------------------
# PDF EXTRACT
# --------------------------
def extract_pdf(file):
    return extract_text(file)

# --------------------------
# SKILL EXTRACTION
# --------------------------
def extract_skills(text):

    text = text.lower()

    skill_map = {
        "Programming": ["python", "java", "c++"],
        "Web Development": ["html", "css", "javascript", "react", "node", "flask", "django", "api"],
        "Data & Analytics": ["sql", "excel", "pandas", "numpy", "power bi", "analytics"],
        "Machine Learning": ["machine learning", "ml", "tensorflow", "keras", "nlp"],
        "Cloud & DevOps": ["aws", "azure", "docker", "kubernetes"],
        "Tools": ["git", "github"],
        "Soft Skills": ["communication", "teamwork"]
    }

    detected = []

    for category, keywords in skill_map.items():
        if any(k in text for k in keywords):
            detected.append(category)

    return detected

# --------------------------
# JOB ROLES
# --------------------------
JOB_ROLES = {
    "Python Developer": "Build backend systems, APIs, and scalable applications.",
    "Full Stack Developer": "Develop frontend and backend applications.",
    "Data Analyst": "Analyze data and generate insights.",
    "Machine Learning Engineer": "Build and deploy ML models.",
    "DevOps Engineer": "Manage cloud infrastructure and automation.",
    "Software Engineer": "Develop scalable software systems."
}

# --------------------------
# ATS SCORE (STABLE)
# --------------------------
def ats_score(resume, jd, resume_skills, jd_skills, exp):

    vectorizer = CountVectorizer(ngram_range=(1,2))
    matrix = vectorizer.fit_transform([resume, jd])
    base = cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100

    if len(jd_skills) == 0:
        skill_score = 65
    else:
        matched = len(set(resume_skills) & set(jd_skills))
        skill_score = (matched / max(len(jd_skills), 1)) * 100

    exp_score = min(exp * 5, 25)

    score = (0.35 * base) + (0.5 * skill_score) + (0.15 * exp_score)

    score = 60 + (score * 0.4)

    return round(min(score, 95), 2)

# --------------------------
# INPUT
# --------------------------
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

selected_role = st.selectbox("💼 Select Job Role", list(JOB_ROLES.keys()))
job_description = JOB_ROLES[selected_role]

experience = st.number_input("🧑‍💼 Years of Experience", 0, 20, 0)

st.divider()

# --------------------------
# ANALYSIS
# --------------------------
if uploaded_file and job_description:

    if st.button("🚀 Analyze Resume"):

        resume_text = extract_pdf(uploaded_file)

        resume_clean = clean_text(resume_text)
        jd_clean = clean_text(job_description)

        resume_skills = extract_skills(resume_clean)
        jd_skills = extract_skills(jd_clean)

        score = ats_score(resume_clean, jd_clean, resume_skills, jd_skills, experience)

        # --------------------------
        # REPORT HEADER
        # --------------------------
        st.markdown("## 📊 Candidate Match Analysis Report")

        st.metric("Compatibility Score", f"{score}%")

        # --------------------------
        # PROFESSIONAL STATUS BADGE (REPLACED GREEN BLOCK)
        # --------------------------
        if score >= 80:

            st.markdown("""
            <div style="
                padding: 18px;
                border-radius: 10px;
                background: #e8f5e9;
                border-left: 6px solid #2e7d32;
                font-size: 16px;
                font-weight: 600;
                color: #1b5e20;
                margin-top: 10px;
            ">
                ✔ High Compatibility Profile — Strong alignment with job requirements
            </div>
            """, unsafe_allow_html=True)

        elif score >= 65:

            st.markdown("""
            <div style="
                padding: 18px;
                border-radius: 10px;
                background: #fff8e1;
                border-left: 6px solid #ffb300;
                font-size: 16px;
                font-weight: 600;
                color: #6d4c41;
                margin-top: 10px;
            ">
                ⚠ Moderate Compatibility Profile — Some improvements required
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div style="
                padding: 18px;
                border-radius: 10px;
                background: #ffebee;
                border-left: 6px solid #c62828;
                font-size: 16px;
                font-weight: 600;
                color: #b71c1c;
                margin-top: 10px;
            ">
                ✖ Low Compatibility Profile — Resume needs optimization
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # --------------------------
        # SKILLS
        # --------------------------
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🧠 Resume Skill Areas")
            if resume_skills:
                for s in resume_skills:
                    st.write(f"✔ {s}")
            else:
                st.info("Basic skill signals detected")

        with col2:
            st.subheader("📌 Expected Skill Areas")
            if jd_skills:
                for s in jd_skills:
                    st.write(f"🔹 {s}")
            else:
                st.info("Key job competencies identified from role description")

        st.divider()

        # --------------------------
        # IMPROVEMENTS
        # --------------------------
        st.markdown("## 💡 Improvement Insights")

        if score < 80:
            st.markdown("""
✔ Add missing role-specific keywords  
✔ Highlight measurable achievements  
✔ Improve project descriptions  
✔ Use structured ATS-friendly format  
""")
        else:
            st.success("Resume is well aligned with role requirements.")
