import streamlit as st
import tempfile
import os

from chains.resume_chain import run_resume_chain, llm
from parser.resume_parser import extract_resume_text
from utils.latex_renderer import render_latex
from chains.jd_validator import validate_job_description
from utils.ats_guard import enforce_jd_only_keywords


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Resume Optimizer",
    layout="wide",
)

st.title("🧠 AI Resume Optimizer")
st.caption("ATS-aware, recruiter-trusted resume optimization")


# --------------------------------------------------
# MODE SELECTION
# --------------------------------------------------
mode = st.selectbox(
    "Optimization Mode",
    [
        "Job-Specific Optimization",
        "General Optimization",
    ],
)


# --------------------------------------------------
# INPUTS
# --------------------------------------------------
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


# --------------------------------------------------
# BUTTON ENABLE / DISABLE LOGIC
# --------------------------------------------------
disable_optimize = False
disable_reason = None

if not resume_file:
    disable_optimize = True
    disable_reason = "Please upload a resume."

if mode == "Job-Specific Optimization":
    if not job_desc or len(job_desc.strip()) < 30:
        disable_optimize = True
        disable_reason = (
            "Please paste a full job description (minimum 30 characters)."
        )

if disable_reason:
    st.info(disable_reason)


optimize_clicked = st.button(
    "🚀 Optimize Resume",
    disabled=disable_optimize,
)


# --------------------------------------------------
# MAIN ACTION (SINGLE SOURCE OF TRUTH)
# --------------------------------------------------
if optimize_clicked:

    # ----------------------------------------------
    # JOB DESCRIPTION VALIDATION (HARD BLOCK)
    # ----------------------------------------------
    if mode == "Job-Specific Optimization":

        if not job_desc or len(job_desc.strip()) < 30:
            st.error(
                "❌ Invalid Job Description.\n\n"
                "Please paste the complete job description "
                "(minimum 30 characters)."
            )
            st.stop()

        with st.spinner("🔍 Validating job description..."):
            is_valid_jd = validate_job_description(job_desc, llm)

        if not is_valid_jd:
            st.error(
                "❌ The provided text does not appear to be a valid job description.\n\n"
                "Please paste a real job description including responsibilities, "
                "requirements, and skills."
            )
            st.stop()

    # ----------------------------------------------
    # RESUME OPTIMIZATION
    # ----------------------------------------------
    with st.spinner("🔍 Analyzing resume and optimizing with AI..."):
        resume_text = extract_resume_text(resume_file)
        optimized_resume = run_resume_chain(resume_text, job_desc)

        ats_cleaned = enforce_jd_only_keywords(optimized_resume.ats_keywords)

        optimized_resume.ats_keywords.jd_keywords = ats_cleaned["jd_keywords"]
        optimized_resume.ats_keywords.present_keywords = ats_cleaned["present_keywords"]
        optimized_resume.ats_keywords.missing_keywords = ats_cleaned["missing_keywords"]
        optimized_resume.ats_keywords.match_score = ats_cleaned["match_score"]


    # ----------------------------------------------
    # LATEX GENERATION
    # ----------------------------------------------
    with tempfile.TemporaryDirectory() as tmp:
        tex_path = os.path.join(tmp, "resume.tex")

        render_latex(
            optimized_resume.model_dump(),
            tex_path,
        )

        latex_code = open(tex_path).read()

    st.success("✅ Resume optimized successfully!")


    # --------------------------------------------------
    # LAYOUT
    # --------------------------------------------------
    left, right = st.columns([1.2, 1])


    # --------------------------------------------------
    # LEFT: LATEX PREVIEW
    # --------------------------------------------------
    with left:
        st.subheader("📄 LaTeX Resume Preview")

        st.code(
            latex_code,
            language="latex",
        )

        st.download_button(
            "⬇️ Download LaTeX",
            latex_code,
            file_name="resume.tex",
        )


    # --------------------------------------------------
    # RIGHT: ATS ANALYSIS (JOB-SPECIFIC ONLY)
    # --------------------------------------------------
    if mode == "Job-Specific Optimization":
        with right:
            st.subheader("📊 ATS Keyword Analysis")

            ats = optimized_resume.ats_keywords

            # ATS match score (optional)
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
