import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-latest') 
    response = model.generate_content(prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Streamlit UI
st.title("📝 Smart ATS Analyzer")
st.markdown("### Boost Your Resume's Chances Against Applicant Tracking Systems")

jd = st.text_area("**Paste the Job Description Here**", height=150)
uploaded_file = st.file_uploader("**Upload Your Resume (PDF only)**", type="pdf")

submit = st.button("🔍 Analyze Resume")

if submit:
    if uploaded_file is not None and jd.strip() != "":
        text = input_pdf_text(uploaded_file)
        
        input_prompt = f"""
        ACT as a professional HR recruiter with 10+ years experience in technical hiring.
        Analyze this resume against the job description and provide detailed feedback.
        
        **RESUME CONTENT:**
        {text}
        
        **JOB DESCRIPTION:**
        {jd}
        
        Provide your analysis in this EXACT format with bold headings (markdown):
        
        **🏆 ATS Match Score:** [X/100]
        
        **🔍 JD Match Percentage:** XX% 
        
        **✅ Key Strengths:**
        - Strength 1 with explanation
        - Strength 2 with explanation
        - (3-5 bullet points)
        
        **⚠️ Missing Keywords/Skills:**
        - Missing keyword 1 (why it matters)
        - Missing keyword 2 (why it matters)
        - (List all important missing items)
        
        **📌 Critical Improvements Needed:**
        - Improvement 1 with specific suggestions
        - Improvement 2 with specific suggestions
        - (Actionable advice)
        
        **💡 Personalized Recommendations:**
        1. First recommendation to boost match
        2. Second recommendation to stand out
        3. Third recommendation for better formatting
        
        **📝 Professional Summary Suggestion:**
        [Write a 3-4 line professional summary that would work better for this specific job]
        
        Be brutally honest but constructive. Focus on technical requirements first, then soft skills.
        """
        
        response = get_gemini_response(input_prompt)
        
        st.markdown("---")
        st.markdown("## 🔬 Detailed Resume Analysis")
        st.markdown(response)  # This will render the markdown formatting
        
    else:
        st.warning("⚠️ Please provide both a job description and a PDF resume.")