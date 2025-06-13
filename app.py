# import streamlit as st
# from utils import extract_text_from_file, generate_flashcards, export_flashcards
# import pandas as pd

# st.set_page_config(page_title="LLM Flashcard Generator", layout="wide")
# st.title("📚 LLM-Powered Flashcard Generator")

# uploaded_file = st.file_uploader("Upload a .pdf or .txt file", type=["pdf", "txt"])
# user_input = st.text_area("Or paste your educational content here")

# subject = st.selectbox("Select Subject (optional)", ["General", "Biology", "History", "Computer Science", "Physics", "Chemistry"])

# if st.button("Generate Flashcards"):
#     with st.spinner("Extracting content and generating flashcards..."):
#         text = ""
#         if uploaded_file:
#             text = extract_text_from_file(uploaded_file)
#         elif user_input.strip():
#             text = user_input.strip()

#         if not text:
#             st.error("Please upload a file or paste content to continue.")
#         else:
#             flashcards = generate_flashcards(text, subject)
#             if flashcards:
#                 st.success(f"{len(flashcards)} flashcards generated successfully!")
#                 df = pd.DataFrame(flashcards)
#                 st.dataframe(df)

#                 export_format = st.selectbox("Export format", ["CSV", "JSON"])
#                 if st.button("Download Flashcards"):
#                     export_flashcards(df, export_format)
#             else:
#                 st.warning("No flashcards generated. Try with more content.")


import streamlit as st
import pandas as pd
from utils import extract_text_from_file, generate_flashcards, export_flashcards

st.set_page_config(page_title="📚 Flashcard Generator", page_icon="📖", layout="wide")

st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            color: #4B8BBE;
            font-weight: bold;
            text-align: center;
        }
        .sub-title {
            text-align: center;
            font-size: 18px;
            color: #777;
        }
        .section-title {
            font-size: 20px;
            font-weight: 600;
            color: #333;
            margin-top: 30px;
        }
        .flashcard {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            border-left: 5px solid #4B8BBE;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .footer {
            margin-top: 60px;
            text-align: center;
            font-size: 14px;
            color: #aaa;
        }
    </style>
    <div class="main-title">📚 LLM-Powered Flashcard Generator</div>
    <p class="sub-title">Create and translate smart flashcards with structure, difficulty levels, and export options</p>
    <hr>
""", unsafe_allow_html=True)

# Sidebar Inputs
with st.sidebar:
    st.header("📥 Input")
    uploaded_file = st.file_uploader("Upload a `.pdf` or `.txt` file", type=["pdf", "txt"])
    user_input = st.text_area("Paste content", height=200)
    subject = st.selectbox("📘 Subject", ["General", "Biology", "History", "Computer Science", "Physics", "Chemistry"])
    language = st.selectbox("🌐 Translate to", ["English", "Hindi", "Spanish", "None"])
    export_format = st.selectbox("💾 Export format", ["CSV", "JSON"])
    generate = st.button("🚀 Generate Flashcards")

# Main Flashcard Logic
if generate:
    with st.spinner("Generating flashcards using GPT-3.5..."):
        text = ""
        if uploaded_file:
            text = extract_text_from_file(uploaded_file)
        elif user_input.strip():
            text = user_input.strip()

        if not text:
            st.error("⚠️ Please upload or paste some educational content.")
        else:
            flashcards = generate_flashcards(text, subject, language)

            if flashcards:
                st.success(f"✅ {len(flashcards)} flashcards generated!")

                st.markdown("<div class='section-title'>🧾 Review & Edit Flashcards</div>", unsafe_allow_html=True)
                df = pd.DataFrame(flashcards)
                edited_df = st.data_editor(df, num_rows="dynamic")

                st.markdown("<div class='section-title'>⬇️ Export Flashcards</div>", unsafe_allow_html=True)
                if st.button("📥 Download Now"):
                    export_flashcards(edited_df, export_format)
            else:
                st.warning("⚠️ No flashcards generated. Try more detailed content.")

# Footer
st.markdown("""
<div class="footer">
    Built by <strong>Sahil Kunwar Singh Naagar</strong> | Internship Project 2025
</div>
""", unsafe_allow_html=True)
