# 🧠 AI Resume ATS Optimizer

An AI-powered resume optimization application built with **Streamlit**, **LangChain**, and **Hugging Face**.  
It helps job seekers optimize their resumes for specific job descriptions while staying **completely truthful, ATS-friendly, and recruiter-credible**.

The tool rewrites resumes using job-description-aligned language, analyzes ATS keyword coverage, highlights missing keywords, and generates a clean LaTeX resume ready for submission.

---

## ✨ Key Highlights

- 🔍 Job-description–specific resume optimization
- 📊 ATS keyword analysis & missing keyword detection
- 🛡️ Strict hallucination prevention (no fake skills or experience)
- 📄 LaTeX resume generation with live preview
- ⚙️ Production-grade architecture with schema validation
- 🧠 Recruiter-aligned and ATS-aware logic

---

## 🚀 Features

### ✅ Resume Optimization
- Rewrites professional summary to align with the job description
- Improves experience bullet points using strong action verbs
- Refines clarity, structure, and recruiter readability
- Preserves original experience, scope, and seniority
- General resume optimization mode (no job description required)

### 📊 ATS Keyword Analysis
- Extracts important ATS keywords from the job description
- Detects keywords present in the resume
- Highlights **missing ATS keywords**
- Calculates an ATS keyword match score (%)
- Conservative and honest keyword evaluation

### 📄 Resume Output
- Generates ATS-friendly LaTeX resumes
- In-app LaTeX source preview
- Downloadable `.tex` file
- Clean formatting (no tables, graphics, or columns)

### 🛡️ Production Quality
- Structured LLM output using Pydantic schemas
- JSON-only responses enforced
- Modular, maintainable codebase
- Easy to extend for SaaS or enterprise use

---

## 🧱 Tech Stack

- **Frontend**: Streamlit  
- **LLM Orchestration**: LangChain (LCEL)  
- **LLMs**: Hugging Face (Mistral / LLaMA / Zephyr)  
- **Validation**: Pydantic  
- **Resume Parsing**: pdfplumber  
- **Resume Rendering**: LaTeX + Jinja2  

---

## 📂 Project Structure

```
ai-resume-ats-optimizer/
│
├── app.py
├── requirements.txt
├── .env.example
│
├── chains/
│   └── resume_chain.py
│
├── prompts/
│   ├── job_specific.txt
│   └── general.txt
│
├── schemas/
│   └── resume_schema.py
│
├── parser/
│   └── resume_parser.py
│
├── latex/
│   └── resume_template.tex
│
├── utils/
│   └── latex_renderer.py
```

---

## 🛠️ Installation & Setup

### Clone the Repository
```bash
git clone https://github.com/your-username/ai-resume-ats-optimizer.git
cd ai-resume-ats-optimizer
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables
```env
HUGGING_FACE_TOKEN=your_huggingface_token
CHAT_HF_MODEL=mistralai/Mistral-7B-Instruct-v0.2
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Open http://localhost:8501

---

## 📜 License

MIT License
