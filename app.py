import streamlit as st
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from groq import Groq
import re

# Load environment variables
load_dotenv()

def get_groq_response(prompt):
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            st.error("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
            return None
        
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.3,
            max_tokens=4000,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting response from Groq: {str(e)}")
        st.error("Make sure you have installed the groq library: pip install groq")
        return None

def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {str(e)}")
        return ""

# Streamlit UI
st.set_page_config(page_title="Smart ATS Analyzer", page_icon="📝") # Removed layout="wide"

st.title("📝 Smart ATS Analyzer")
st.markdown("### Boost Your Resume's Chances Against Applicant Tracking Systems")

# Main form container (optional, but can help with styling if needed later)
with st.container():
    jd = st.text_area("**Paste the Job Description Here**", height=200, placeholder="Paste the full job description...")
    uploaded_file = st.file_uploader("**Upload Your Resume (PDF only)**", type="pdf")

    submit = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)

if submit:
    if uploaded_file is not None and jd and jd.strip() != "":
        with st.spinner("🤖 Analyzing your resume against the JD... This might take a moment!"):
            resume_text = input_pdf_text(uploaded_file)
            
            if not resume_text:
                st.error("Could not extract text from the uploaded PDF. Please try another PDF or check the file content.")
                st.stop()

            input_prompt = f"""
            ACT as an expert ATS (Applicant Tracking System) and a professional HR recruiter with 15+ years of experience in technical hiring for multinational companies.
            Your task is to meticulously analyze the provided resume against the given job description.

            **RESUME CONTENT:**
            ```
            {resume_text}
            ```

            **JOB DESCRIPTION:**
            ```
            {jd}
            ```

            Provide your analysis in the following EXACT Markdown format, ensuring all headings are bold. Do not add any introductory or concluding remarks outside this format.

            **🏆 ATS Match Score:** [Calculate a score out of 100, e.g., 85/100. Be realistic.]

            **🔍 JD Match Percentage:** [Calculate a percentage match, e.g., 75%. This should reflect how well the resume aligns with the JD requirements.]
            
            **✅ Key Strengths (Relevant to JD):**
            - Strength 1: [Specific skill/experience from resume] - [Brief explanation of why it's a strength for this JD]
            - Strength 2: [Specific skill/experience from resume] - [Brief explanation]
            - (List 3-5 key strengths directly aligning with the JD)
            
            **⚠️ Missing Keywords/Critical Skills (from JD):**
            - Missing Keyword/Skill 1: [e.g., "Python"] - (Briefly explain its importance based on the JD and suggest where it could be incorporated if applicable)
            - Missing Keyword/Skill 2: [e.g., "Agile Methodology"] - (Briefly explain its importance)
            - (List all significant keywords or skills mentioned in the JD that are absent or not prominent in the resume)
            
            **📌 Critical Improvements Needed for ATS & Recruiter Appeal:**
            - Improvement 1: [Specific actionable advice, e.g., "Quantify achievements in Project X using the STAR method..."]
            - Improvement 2: [Specific actionable advice, e.g., "Add a dedicated 'Technical Skills' section listing proficiency in A, B, C..."]
            - (Provide 2-4 critical, actionable improvements)
            
            **💡 Personalized Recommendations to Stand Out:**
            1. Recommendation 1: [e.g., "Tailor the 'Projects' section to highlight experience with [Specific Tech from JD]..."]
            2. Recommendation 2: [e.g., "Consider adding a brief portfolio link if applicable for [Type of Role] roles."]
            3. Recommendation 3: [e.g., "Ensure consistent formatting for dates and job titles for better readability."]
            
            **📝 Professional Summary Suggestion (Tailored for this JD):**
            [Compose a concise and impactful 3-4 line professional summary specifically tailored to the provided job description, incorporating key skills and experiences from the resume that match the JD.]

            Be brutally honest but always constructive. Focus on concrete, actionable feedback. Prioritize technical requirements and quantifiable achievements.
            """
            
            response = get_groq_response(input_prompt)
        
        if response:
            # CSS will apply to elements within the centered layout
            st.markdown("""
            <style>
            /* .main-container removed as Streamlit's default centered layout is used */
            .analysis-container {
                background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%);
                padding: 1.5rem; /* Adjusted padding for narrower layout */
                border-radius: 15px; margin: 1rem 0;
                box-shadow: 0 8px 25px rgba(0,0,0,0.2); color: white;
            }
            .analysis-container h1, .analysis-container h2, .analysis-container h3 { color: white; }
            .score-display {
                background: rgba(255,255,255,0.15); backdrop-filter: blur(8px);
                border: 1px solid rgba(255,255,255,0.25); border-radius: 10px;
                padding: 1rem; /* Adjusted padding */
                margin-bottom: 1rem; /* Adjusted margin */
                text-align: center; color: white;
            }
            .score-display h1 { font-size: 2.5rem; margin: 0.2em 0; } /* Slightly smaller font for narrower view */
            .score-display h2 { font-size: 1.1rem; margin-bottom: 0.5em; opacity: 0.9; }
            .section-card, .warning-card, .recommendation-card, .summary-card {
                border-radius: 8px; padding: 1.2rem; margin: 1rem 0; /* Adjusted padding */
                color: white;
            }
            .section-card {
                background: rgba(255,255,255,0.08); backdrop-filter: blur(5px);
                border-left: 5px solid #00e676;
            }
            .warning-card {
                background: rgba(255,100,100,0.1);
                border-left: 5px solid #ff6347;
            }
            .recommendation-card {
                background: rgba(66,139,202,0.1);
                border-left: 5px solid #428bca;
            }
            .summary-card {
                background: linear-gradient(45deg, #ff7e5f, #feb47b);
                border-left: 5px solid #ff6a00;
                box-shadow: 0 5px 15px rgba(0,0,0,0.15);
            }
            .section-card h3, .warning-card h3, .recommendation-card h3, .summary-card h4 { 
                margin-top: 0; margin-bottom: 1rem; padding-bottom: 0.5rem; 
                border-bottom: 1px solid rgba(255,255,255,0.2); color: white;
            }
            .summary-card p { font-style: italic; font-size: 1.0rem; line-height: 1.6; } /* Adjusted font size */

            .section-card ul, .warning-card ul, .recommendation-card ul,
            .section-card ol, .warning-card ol, .recommendation-card ol {
                padding-left: 20px;
            }
            .section-card li, .warning-card li, .recommendation-card li {
                margin-bottom: 0.75em; line-height: 1.6;
            }
            .pulse { animation: pulse 2.5s infinite ease-in-out; }
            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.02); opacity: 0.85; } /* Subtler pulse */
            }
            /* Ensure tab headers are clearly visible */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px; /* Space between tab buttons */
            }
            .stTabs [data-baseweb="tab"] {
                height: 44px; /* Adjust tab height */
                white-space: pre-wrap;
                background-color: rgba(230, 230, 250, 0.1); /* Light background for inactive tabs */
                border-radius: 8px 8px 0 0;
                padding: 10px 16px;
            }
            .stTabs [aria-selected="true"] {
                background-color: #6e8efb; /* Match analysis container gradient start */
                color: white;
                font-weight: bold;
            }
            </style>
            """, unsafe_allow_html=True)
            
            def extract_section(pattern, text, default="Not found or couldn't parse."):
                match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                return match.group(1).strip() if match and match.group(1) else default

            ats_score_text = extract_section(r'\*\*🏆 ATS Match Score:\*\*\s*\[?([^\]\n]+)\]?', response)
            jd_percentage_text = extract_section(r'\*\*🔍 JD Match Percentage:\*\*\s*([^\n]+)', response)
            
            strengths = extract_section(r'\*\*✅ Key Strengths(?: \(Relevant to JD\))?:\*\*(.*?)(?=\n\n\*\*|\Z)', response)
            missing_skills = extract_section(r'\*\*⚠️ Missing Keywords/Critical Skills(?: \(from JD\))?:\*\*(.*?)(?=\n\n\*\*|\Z)', response)
            improvements = extract_section(r'\*\*📌 Critical Improvements Needed(?: for ATS & Recruiter Appeal)?:\*\*(.*?)(?=\n\n\*\*|\Z)', response)
            recommendations = extract_section(r'\*\*💡 Personalized Recommendations(?: to Stand Out)?:\*\*(.*?)(?=\n\n\*\*|\Z)', response)
            summary = extract_section(r'\*\*📝 Professional Summary Suggestion(?: \(Tailored for this JD\))?:\*\*(.*)', response)

            ats_score_val = "N/A"
            if ats_score_text and "/" in ats_score_text:
                score_part = ats_score_text.split('/')[0].strip()
                if score_part.isdigit():
                    ats_score_val = score_part

            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Overview", 
                "✅ Strengths", 
                "⚠️ Improvements", 
                "💡 Recommendations"
            ])
            
            with tab1:
                st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
                st.markdown("<h2 style='text-align: center; margin-bottom: 1.5rem;'>🎯 Resume Analysis Overview</h2>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div class="score-display pulse">
                        <h2>🏆 ATS Match Score</h2>
                        <h1>{ats_score_text}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="score-display pulse">
                        <h2>🔍 JD Match</h2>
                        <h1 style="color: #00e676;">{jd_percentage_text}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                if ats_score_val.isdigit():
                    st.progress(int(ats_score_val) / 100)
                elif ats_score_val != "N/A":
                    st.caption("ATS score progress bar unavailable due to format.")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                # Using st.markdown directly for content for better list rendering
                st.subheader("✅ Your Key Strengths")
                st.markdown(f'<div class="section-card"><h3>🌟 What\'s Working Well:</h3>{strengths}</div>', unsafe_allow_html=True)

            with tab3:
                st.subheader("⚠️ Areas for Improvement")
                st.markdown(f'<div class="warning-card"><h3>🔍 Missing Keywords & Critical Skills:</h3>{missing_skills}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="warning-card"><h3>📌 Critical Action Items:</h3>{improvements}</div>', unsafe_allow_html=True)
            
            with tab4:
                st.subheader("💡 Personalized Recommendations & Summary")
                st.markdown(f'<div class="recommendation-card"><h3>🚀 Your Action Plan:</h3>{recommendations}</div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="summary-card">
                    <h4>✨ Suggested Professional Summary:</h4>
                    <p>{summary.replace('\n', '<br>')}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.download_button( # This will be centered by default in the narrower layout
                label="📥 **Download Full Analysis Report (TXT)**",
                data=response,
                file_name="SmartATS_Resume_Analysis.txt",
                mime="text/plain",
                use_container_width=True # Makes it span the centered container width
            )
            
            with st.expander("🔧 View Raw LLM Response (for debugging)"):
                st.text_area("Raw Response:", response, height=300)

        else:
            st.error("Failed to get a response from the analysis service. Please check the error messages above.")
        
    else:
        if submit:
            missing_items = []
            if uploaded_file is None:
                missing_items.append("your resume PDF")
            if not jd or jd.strip() == "":
                missing_items.append("the job description")
            
            if missing_items:
                st.warning(f"⚠️ Please provide { ' and '.join(missing_items) } to proceed with the analysis.")