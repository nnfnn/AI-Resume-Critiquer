# AI-Resume-Critiquer
# AI Resume Critiquer

An AI-powered resume screening and feedback system built with Python, Streamlit, and Google Gemini. Upload a resume, specify a target job role, and instantly receive structured feedback on resume quality, ATS compatibility, keyword coverage, and actionable improvement suggestions.

---

## Overview

Most job seekers apply with resumes that never make it past automated screening systems. This tool addresses that problem by combining NLP-based section and keyword extraction with a Google Gemini AI model to provide honest, role-specific feedback — the kind you would normally get from a professional resume coach.

The system scores resumes against ATS (Applicant Tracking System) criteria, identifies missing sections, detects relevant tech keywords, and returns a structured critique covering strengths, weaknesses, keyword gaps, and prioritized action items.

---

## Features

- PDF text extraction using PyPDF2
- NLP-based detection of key resume sections (Skills, Experience, Education, Projects, Summary)
- Tech keyword matching against a curated stack of 30+ industry-relevant terms
- ATS compatibility scoring (0 to 100) based on section completeness and keyword density
- AI-generated feedback via Google Gemini covering overall score, strengths, weaknesses, keyword gaps, and a final shortlist verdict
- Clean, two-column Streamlit UI with real-time analysis
- Resume text preview to verify extraction quality

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit |
| PDF Extraction | PyPDF2 |
| NLP / Pattern Matching | Python re (regex) |
| AI Feedback | Google Gemini 1.5 Flash |
| Language | Python 3.10+ |

---

## Project Structure

```
AI-Resume-Critiquer/
├── main.py              # Main application — all logic and UI
├── requirements.txt     # Dependencies
└── README.md            # Project documentation
```

---

## Setup and Installation

**Step 1 — Clone the repository**
```bash
git clone https://github.com/nnfnn/AI-Resume-Critiquer.git
cd AI-Resume-Critiquer
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Add your Gemini API key**

Open `main.py` and replace line 17:
```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```
Get a free key at: https://aistudio.google.com

**Step 4 — Run the app**
```bash
streamlit run main.py
```

The app will open at `http://localhost:8501`

---

## How It Works

```
User uploads PDF
      |
      v
PyPDF2 extracts raw text
      |
      v
Regex NLP scans for key sections and tech keywords
      |
      v
ATS score calculated based on section completeness + keyword density
      |
      v
Resume text sent to Google Gemini with role-specific prompt
      |
      v
Structured feedback returned: score, strengths, weaknesses,
keyword gaps, top fixes, and final shortlist verdict
      |
      v
Results displayed in Streamlit UI with metrics and checklist
```

---

## ATS Scoring Breakdown

| Section | Points |
|---|---|
| Skills | 20 |
| Experience | 20 |
| Education | 20 |
| Projects | 15 |
| Summary | 10 |
| Tech Keywords (2 pts each, max 15) | up to 15 |
| **Total** | **100** |

Score interpretation:
- 80 and above: Strong — should pass most ATS filters
- 60 to 79: Average — improvements recommended
- Below 60: Weak — high risk of being filtered out before human review

---

## AI Feedback Structure

The Gemini model returns feedback in seven structured sections:

1. Overall Score (out of 10 with reasoning)
2. What is Working (3 specific strengths)
3. What Needs Work (3 honest weaknesses)
4. Missing Sections
5. Keyword Gaps for the target role
6. Top 3 Things to Fix Right Now
7. Final Verdict (shortlist or not, and why)

---

## Requirements

```
streamlit==1.33.0
PyPDF2==3.0.1
google-generativeai==0.5.4
```

---

## Usage Notes

- PDF must contain selectable text. Scanned image-based PDFs will not extract correctly.
- Resumes are processed in real-time and are never stored or logged.
- The AI feedback is tailored to the specific job role entered by the user.
- For best results, ensure the resume is saved as a standard text-layer PDF from Word or Google Docs.

---

## Author

**Muhammed Nifan**
MSc Data Science and Analytics — Jain University, Bengaluru
GitHub: github.com/nnfnn
LinkedIn: linkedin.com/in/nifan-mk-/
