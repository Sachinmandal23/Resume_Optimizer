import streamlit as st
import spacy
import PyPDF2
import re

# NLP Model load
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")

nlp = load_nlp()

st.set_page_config(layout="wide", page_title="ATS Master Premium Optimizer")
st.title("🎯 ATS Master Premium: Full Diagnostic Report")

col1, col2 = st.columns(2)
with col1: 
    jd = st.text_area("Paste Full Job Description (JD):", height=350)
with col2: 
    uploaded = st.file_uploader("Upload Resume (PDF):", type=["pdf"])
    text = ""
    if uploaded:
        reader = PyPDF2.PdfReader(uploaded)
        for page in reader.pages: text += page.extract_text()
    res = st.text_area("Your Resume Content:", value=text, height=300)

if st.button("🚀 START PREMIUM SCAN"):
    if jd and res:
        jd_doc = nlp(jd.lower())
        res_doc = nlp(res.lower())
        
        # Keywords extraction
        jd_keywords = set([t.lemma_ for t in jd_doc if t.is_alpha and not t.is_stop and len(t.text) > 2])
        res_keywords = set([t.lemma_ for t in res_doc if t.is_alpha and not t.is_stop and len(t.text) > 2])
        
        missing = sorted(list(jd_keywords - res_keywords))
        score = max(0, 100 - (len(missing) * 3)) 
        
        # 1. Scorecard
        st.subheader(f"📊 Final ATS Match Score: {score}/100")
        st.progress(score/100)

        #2. Word Count Check (500-700 Range)
        word_count = len(res.split())
        st.subheader("📝 Word Count Analysis")
        if 500 <= word_count <= 700:
            st.success(f"✅ Word Count is Perfect: {word_count} words.")
        else:
            st.warning(f"⚠️ Word Count Warning: {word_count} words (Target: 500-700).")
        
        # 3. Detailed Gap Analysis
        st.subheader("⚠️ Missing Skills & Keywords (In-Depth)")
        if missing:
            st.warning(f"Total {len(missing)} words found in JD but missing in your resume:")
            st.text_area("Copy this list to your AI tool:", value=", ".join(missing), height=100)
        else:
            st.success("✅ Perfect! All keywords detected.")
            
        # 4. Section Audit (Premium)
        st.subheader("🏗 Section-by-Section Audit")
        
        # Experience Check
        st.write("---")
        if "experience" in res.lower():
            st.success("✅ Experience Section: Found")
            if any(char.isdigit() for char in res):
                st.write("✅ Metrics (Numbers) found in Experience.")
            else:
                st.error("❌ Action Required: Add numbers (e.g., 'Increased revenue by 20%') to experience bullet points.")
        else:
            st.error("❌ Experience Section: Missing (Crucial for ATS).")
            
        # Project Check
        if "project" in res.lower():
            st.success("✅ Projects Section: Found")
        else:
            st.error("❌ Projects Section: Missing (Add a 'Projects' section to showcase missing hard skills).")
            
        # Summary Check
        if any(x in res.lower() for x in ['summary', 'objective']):
            st.success("✅ Summary Section: Found")
        else:
            st.error("❌ Summary Section: Missing (Add a 3-line professional summary).")
            
        # 4. Expert Action Plan
        st.subheader("💡 Premium Optimization Guide")
        st.markdown("""
        **Aapko ab kya karna hai:**
        1. **Keywords Add Karein:** Upar di gayi missing list ko apne 'Skills' ya 'Projects' mein add karein.
        2. **Metrics Daalein:** Har bullet point mein numbers zaroor hone chahiye (e.g., 50%, 2 years, 10k users).
        3. **Section Align:** Agar resume mein 'Professional Experience' likha hai, toh check karein JD mein kya likha hai (Work History vs Experience).
        4. **AI Fix:** Resume ka content aur missing list copy karke kisi bhi AI (Claude/ChatGPT) ko dein aur kahein ki "in missing keywords ko naturally add karke resume re-write karo."
        """)
    else:
        st.error("Please provide both Job Description and Resume.")