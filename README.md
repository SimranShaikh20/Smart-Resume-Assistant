# Smart ATS

## Here is Application Link :

**Application Link**: [Interview Preparation Q&A Chatbot](https://smart-resume-assistant-stxn4ic8g3ycaewftvcykt.streamlit.app/)



## Description
The **Smart ATS (Applicant Tracking System)** is a Streamlit-based web application that helps job seekers optimize their resumes based on a given job description (JD). By using Google's Gemini AI and modern text-processing techniques, it evaluates resumes, provides a match percentage, identifies missing keywords, and generates a profile summary for better alignment with job requirements. This tool is ideal for improving resumes and standing out in competitive job markets.

---

## Features
- **Resume Evaluation:** Analyze uploaded resumes to determine their match with the provided job description.
- **Keyword Matching:** Identify missing keywords critical to aligning resumes with the JD.
- **Profile Summary:** Generate a concise summary highlighting the resume's key strengths.
- **Interactive Interface:** User-friendly web interface built with Streamlit.

---

## How It Works

1. **Input Job Description:**
   - The user pastes the job description (JD) into the text area provided in the app.

2. **Upload Resume:**
   - The user uploads their resume in PDF format.

3. **Text Extraction from PDF:**
   - The app uses the PyPDF2 library to extract text from the uploaded PDF file.

4. **Prompt Generation:**
   - A custom prompt template is populated with the extracted resume text and the provided job description.

5. **AI Analysis:**
   - The prompt is sent to Google’s Gemini AI (via `google.generativeai` package), which evaluates the resume, calculates the match percentage, identifies missing keywords, and generates a profile summary.

6. **Output Results:**
   - The results, including the JD match percentage, missing keywords, and profile summary, are displayed in the app interface for the user to review.

---

## Installation

### Prerequisites
- Python 3.8+
- Pip

### Libraries Used
- `streamlit`
- `google-generativeai`
- `PyPDF2`
- `python-dotenv`

### Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```bash
   cd smart-ats
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file in the project directory.
   - Get your Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey):
     1. Visit the link and sign in with your Google account.
     2. Generate a new API key if you don’t already have one.
     3. Copy the API key.
   - Add your API key to the `.env` file:
     ```env
     GOOGLE_API_KEY=your_api_key_here
     ```

5. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## Usage
1. Launch the app in your browser.
2. Paste the job description into the provided text area.
3. Upload your resume in PDF format.
4. Click the **Submit** button to analyze your resume.
5. Review the detailed results, including:
   - JD Match Percentage
   - Missing Keywords
   - Profile Summary

---
---

## Project Structure
```
smart-ats/
├── app.py            # Main application file
├── requirements.txt  # List of dependencies
├── .env              # Environment variables file
├── README.md         # Project documentation
```

---

## Technologies Used
- **Streamlit:** Frontend framework for building the user interface.
- **Google Gemini AI:** For advanced natural language processing and content generation.
- **PyPDF2:** For extracting text from PDF resumes.
- **Python-dotenv:** To manage environment variables securely.

---

## Future Enhancements
- Support for multiple file formats (e.g., Word, TXT).
- Integration with other AI models for comparison.
- Export results as a downloadable report.
- Multi-language support for global users.

---

## Author
This project was created by **Simran Shaikh**.

---

## License
This project is licensed under the MIT License.
