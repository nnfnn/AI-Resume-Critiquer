import streamlit as st
import PyPDF2
import google.generativeai as genai
import re
import io

# ─────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────

st.set_page_config(
    page_title="AI Resume Critiquer",
    page_icon="📄",
    layout="wide"
)

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


# ─────────────────────────────────────────
#  FUNCTIONS
# ─────────────────────────────────────────

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def extract_sections(text):
    keywords = {
        "Skills":      r"(skills|technical skills|core competencies)",
        "Experience":  r"(experience|work history|employment|internship)",
        "Education":   r"(education|academic|qualification|degree)",
        "Projects":    r"(projects|portfolio|case study)",
        "Summary":     r"(summary|objective|profile|about me)"
    }
    return {section: bool(re.search(pattern, text.lower()))
            for section, pattern in keywords.items()}


def extract_keywords(text):
    tech_stack = [
        "python", "sql", "power bi", "tableau", "excel",
        "machine learning", "deep learning", "nlp", "pandas",
        "numpy", "scikit-learn", "langchain", "streamlit",
        "flask", "django", "react", "aws", "azure", "gcp",
        "tensorflow", "pytorch", "rag", "chromadb", "etl",
        "mongodb", "postgresql", "opencv", "keras", "spark"
    ]
    return [kw for kw in tech_stack if kw in text.lower()]


def calculate_ats_score(sections, keywords):
    score = 0
    weights = {"Skills": 20, "Experience": 20, "Education": 20,
               "Projects": 15, "Summary": 10}
    for section, found in sections.items():
        if found:
            score += weights.get(section, 0)
    score += min(len(keywords) * 2, 15)
    return score


def get_ai_feedback(resume_text, job_role):
    prompt = f"""
You are a friendly but honest resume coach helping a job seeker land their dream role.

Analyze the resume below for someone applying to: {job_role}

Give feedback in this exact format — keep it conversational, warm, and human (not robotic):

1. OVERALL SCORE
   Give a score out of 10 and one honest sentence on why.

2. WHAT'S WORKING
   3 genuine strengths you noticed. Be specific, not generic.

3. WHAT NEEDS WORK
   3 honest weaknesses. Don't sugarcoat — be direct but kind.

4. MISSING SECTIONS
   List any important sections that are absent from this resume.

5. KEYWORD GAPS
   List important keywords for a {job_role} role that are missing from this resume.

6. TOP 3 THINGS TO FIX RIGHT NOW
   Actionable, specific improvements — tell them exactly what to do.

7. FINAL VERDICT
   One honest sentence — would you shortlist this resume or not, and why?

Resume:
{resume_text[:3000]}
"""
    response = model.generate_content(prompt)
    return response.text


# ─────────────────────────────────────────
#  UI
# ─────────────────────────────────────────

# Header
st.title("📄 AI Resume Critiquer")
st.markdown("##### Drop your resume. Get honest, AI-powered feedback in seconds.")
st.markdown("No fluff. No generic tips. Just real feedback that actually helps.")
st.divider()

# Input section
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👇 Start here")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type=["pdf"],
        help="Make sure your PDF has selectable text, not just a scanned image"
    )
    job_role = st.text_input(
        "What role are you applying for?",
        placeholder="e.g. Data Analyst, ML Engineer, Business Analyst"
    )
    st.markdown("")
    analyze_btn = st.button(
        "🔍 Analyze My Resume",
        type="primary",
        use_container_width=True
    )

with col2:
    st.markdown("### 💡 How it works")
    st.markdown("""
    1. **Upload** your resume as a PDF
    2. **Tell us** the role you're targeting
    3. We **extract** and scan your resume using NLP
    4. Our **AI coach** gives you honest, structured feedback
    5. You **fix it** and apply with confidence
    """)
    st.info("Your resume is analyzed in real-time and never stored anywhere.")


# ─────────────────────────────────────────
#  ANALYSIS
# ─────────────────────────────────────────

if analyze_btn:

    if not uploaded_file:
        st.warning("⚠️ Please upload your resume first.")
        st.stop()

    if not job_role:
        st.warning("⚠️ Please tell us what role you're applying for.")
        st.stop()

    with st.spinner("Reading your resume and thinking hard... give us a moment 🤔"):

        resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text:
            st.error("❌ We couldn't read text from this PDF. Try a different file.")
            st.stop()

        sections   = extract_sections(resume_text)
        keywords   = extract_keywords(resume_text)
        ats_score  = calculate_ats_score(sections, keywords)
        ai_feedback = get_ai_feedback(resume_text, job_role)

    st.divider()
    st.markdown(f"## Results for: **{job_role}** role")
    st.markdown("")

    # Metric cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ATS Score",          f"{ats_score}/100",
              delta="Good" if ats_score >= 70 else "Needs work")
    m2.metric("Tech Keywords Found", len(keywords))
    m3.metric("Sections Detected",   f"{sum(sections.values())}/5")
    m4.metric("Pages Scanned",
              f"{PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue())).pages.__len__()} pages")

    st.divider()

    left, right = st.columns([1, 1])

    with left:

        # Section checklist
        st.markdown("### 📋 Section Checklist")
        st.caption("These are the 5 sections every strong resume should have.")
        for section, found in sections.items():
            if found:
                st.success(f"✅  {section} — found")
            else:
                st.error(f"❌  {section} — missing")

        st.markdown("")

        # Keywords
        st.markdown("### 🔑 Tech Keywords Detected")
        st.caption("Keywords your resume already has that match industry expectations.")
        if keywords:
            keyword_display = "  ".join([f"`{kw}`" for kw in keywords])
            st.markdown(keyword_display)
        else:
            st.warning("😬 No common tech keywords detected. This will hurt your ATS score.")

        st.markdown("")

        # ATS score explanation
        st.markdown("### 📈 ATS Score Breakdown")
        st.caption("Applicant Tracking Systems scan resumes before a human sees them.")
        if ats_score >= 80:
            st.success(f"🟢 {ats_score}/100 — Strong. Your resume should pass most ATS filters.")
        elif ats_score >= 60:
            st.warning(f"🟡 {ats_score}/100 — Average. Some improvements needed.")
        else:
            st.error(f"🔴 {ats_score}/100 — Weak. High risk of getting filtered out.")

        st.markdown("")

        # Raw text preview
        with st.expander("🔎 See what we extracted from your PDF"):
            st.caption("This is the raw text our system read from your resume.")
            st.text(resume_text[:2000] + "\n\n... (truncated)" if len(resume_text) > 2000 else resume_text)

    with right:

        # AI feedback
        st.markdown("### 🤖 Your Personal AI Feedback")
        st.caption(f"Tailored specifically for a **{job_role}** role.")
        st.markdown("")
        st.markdown(ai_feedback)

    st.divider()

    # Footer CTA
    st.markdown("### 🚀 What to do next")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("**Step 1** — Fix the missing sections flagged above")
    with col_b:
        st.info("**Step 2** — Add the missing keywords naturally into your resume")
    with col_c:
        st.info("**Step 3** — Come back and re-analyze to see your improved score")

    st.markdown("")
    st.caption("Built with Python · Streamlit · Google Gemini · PyPDF2 · NLP")
