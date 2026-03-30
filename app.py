import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. SETTINGS & PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="IDEMI Digital Evaluation")

# --- 2. API SETUP (Via Streamlit Secrets) ---
# We will set this up in the Streamlit Cloud dashboard later
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("Please set the GEMINI_KEY in Streamlit Secrets.")

model = genai.GenerativeModel('gemini-1.5-pro')

# --- 3. UI HEADER ---
st.title("🎓 IDEMI Mumbai - Digital Evaluation Platform")
st.markdown("### Subject: IDAS204 Design Thinking")
st.divider()

# --- 4. DASHBOARD LAYOUT (3 COLUMNS) ---
col_marks, col_script, col_ai = st.columns([1, 2, 1.2])

with col_marks:
    st.subheader("📝 Marking Panel")
    with st.container(border=True):
        st.write("**Q1: MCQs (10 Marks)**")
        q1_score = st.number_input("Enter Q1 Total", 0, 10, value=0)
        
        st.divider()
        st.write("**Q2: Descriptive (20 Marks)**")
        q2_i = st.number_input("Q2.i (Collaboration)", 0.0, 5.0, step=0.5)
        q2_ii = st.number_input("Q2.ii (Steps)", 0.0, 5.0, step=0.5)
        q2_iii = st.number_input("Q2.iii (Difference)", 0.0, 5.0, step=0.5)
        q2_iv = st.number_input("Q2.iv (Apple Case)", 0.0, 5.0, step=0.5)
        
        total = q1_score + q2_i + q2_ii + q2_iii + q2_iv
        st.metric("Total Marks", f"{total} / 30")
        
        if st.button("Finalize & Submit Score", type="primary"):
            st.success("Marks Saved to IDEMI Database!")

with col_script:
    st.subheader("📄 Answer Script Viewer")
    uploaded_file = st.file_uploader("Upload Scanned Student Script (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
    else:
        st.info("Waiting for scanned script upload...")

with col_ai:
    st.subheader("🤖 AI Copilot (Gemini)")
    if uploaded_file:
        if st.button("Run AI Evaluation"):
            with st.spinner("Analyzing handwriting and grading..."):
                # Define the IDEMI Specific Prompt
                prompt = """
                Evaluate this IDEMI Design Thinking script. 
                1. Check MCQs against Key: 1:B, 2:C, 3:B, 4:C, 5:C, 6:B, 7:A, 8:D, 9:B, 10:C.
                2. Critique the descriptive answers for Q2. 
                3. Transcribe a summary of what the student wrote.
                4. Flag any suspicious symbols or notes for 'Unfair Means'.
                Provide a score suggestion and feedback.
                """
                
                # Convert image to bytes for API
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                image_data = img_byte_arr.getvalue()
                
                response = model.generate_content([
                    prompt, 
                    {'mime_type': 'image/jpeg', 'data': image_data}
                ])
                
                st.markdown("---")
                st.markdown("#### AI Suggestion")
                st.write(response.text)
                st.warning("Evaluator must verify AI scores before final submission.")
    else:
        st.write("Upload a script to enable AI Copilot.")