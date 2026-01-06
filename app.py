import streamlit as st
import tempfile
import os

from chains.resume_chain import run_resume_chain
from parser.resume_parser import extract_resume_text
from utils.latex_renderer import render_latex


st.set_page_config(
    page_title="AI Resume Optimizer",
    layout="wide",
)

st.title("🧠 AI Resume Optimizer")
st.caption("ATS-aware, recruiter-trusted resume optimization")


mode = st.selectbox(
    "Optimization Mode",
    [
        "Job-Specific Optimization",
        "General Optimization",
    ],
)


resume_file = st.file_uploader(
    "Upload Resume (PDF or TXT)",
    type=["pdf", "txt"],
)

job_desc = None
if mode == "Job-Specific Optimization":
    job_desc = st.text_area(
        "Paste Job Description",
        height=220,
        placeholder="Paste the full job description here...",
    )


if st.button("🚀 Optimize Resume") and resume_file:

    with st.spinner("🔍 Analyzing resume and optimizing with AI..."):
        resume_text = extract_resume_text(resume_file)
        optimized_resume = run_resume_chain(resume_text, job_desc)

    
    with tempfile.TemporaryDirectory() as tmp:
        tex_path = os.path.join(tmp, "resume.tex")

        render_latex(
            optimized_resume.model_dump(),
            tex_path,
        )

        latex_code = open(tex_path).read()

    st.success("✅ Resume optimized successfully!")


    left, right = st.columns([1.2, 1])

  
    with left:
        st.subheader("📄 LaTeX Resume Preview")
        st.code(latex_code, language="latex")

        st.download_button(
            "⬇️ Download LaTeX",
            latex_code,
            file_name="resume.tex",
        )


    if mode == "Job-Specific Optimization":
        with right:
            st.subheader("📊 ATS Keyword Analysis")

            ats = optimized_resume.ats_keywords

            if hasattr(ats, "match_score"):
                st.metric(
                    label="ATS Keyword Match Score",
                    value=f"{ats.match_score}%",
                )

            st.subheader("🚨 Missing Keywords")

            missing = ats.missing_keywords

            if missing:
                if len(missing) > 10:
                    st.error("⚠️ High ATS risk — many required keywords are missing.")
                elif len(missing) > 5:
                    st.warning("⚠️ Medium ATS risk — consider adding relevant keywords.")
                else:
                    st.info("ℹ️ Low ATS risk — a few keywords are missing.")

                st.markdown(
                    "**Only add these if you genuinely have the experience:**"
                )

                for kw in missing:
                    st.markdown(f"- ❌ **{kw}**")
            else:
                st.success(
                    "🎉 Your resume already covers all major ATS keywords!"
                )

            with st.expander("✅ Keywords Already Covered"):
                for kw in ats.present_keywords:
                    st.markdown(f"- {kw}")
