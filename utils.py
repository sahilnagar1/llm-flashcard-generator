# from openai import OpenAI
# import PyPDF2
# import streamlit as st
# import pandas as pd
# from openai import OpenAI
# import streamlit as st

# client = OpenAI(api_key=st.secrets["openai_api_key"])
# def extract_text_from_file(file):
#     if file.type == "application/pdf":
#         reader = PyPDF2.PdfReader(file)
#         return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
#     elif file.type == "text/plain":
#         return file.read().decode("utf-8")
#     return ""

# def generate_flashcards(text, subject):
#     prompt = f"""
# Convert the following educational content into 10–15 Q&A flashcards. Each flashcard should include:
# - A clear, concise question
# - A self-contained answer

# Subject: {subject}
# Content:
# \"\"\"{text}\"\"\"

# Format like:
# Q1: ...
# A1: ...
# Q2: ...
# A2: ...
# """

#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7
#         )
#         content = response.choices[0].message.content
#         lines = content.strip().split("\n")
#         flashcards = []
#         for i in range(0, len(lines), 2):
#             if i + 1 < len(lines):
#                 q = lines[i].strip().replace("Q", "").replace(":", "").strip()
#                 a = lines[i+1].strip().replace("A", "").replace(":", "").strip()
#                 flashcards.append({"Question": q, "Answer": a})
#         return flashcards
#     except Exception as e:
#         st.error(f"Error generating flashcards: {e}")
#         return []

# def export_flashcards(df, format):
#     if format == "CSV":
#         csv = df.to_csv(index=False).encode("utf-8")
#         st.download_button("Download CSV", csv, "flashcards.csv", "text/csv")
#     elif format == "JSON":
#         json_data = df.to_json(orient="records", indent=2)
#         st.download_button("Download JSON", json_data, "flashcards.json", "application/json")

import PyPDF2
import pandas as pd
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai_api_key"])

def extract_text_from_file(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    return ""

def generate_flashcards(text, subject, language):
    prompt = f"""
You are a flashcard generator assistant.

Task:
1. Read the following educational content.
2. Extract 10–15 well-structured flashcards grouped under subheadings (e.g., chapters/sections).
3. Each flashcard must contain:
    - Question
    - Answer
    - Difficulty level (Easy, Medium, Hard)
4. Preserve any topic structure if present.
5. Translate the flashcards into {language} if it's not English.

Content:
\"\"\"{text}\"\"\"

Format Example:
Section: Chapter 1 - Introduction
Q1: ...
A1: ...
Difficulty: ...

Section: Chapter 2 - Advanced Concepts
Q2: ...
A2: ...
Difficulty: ...
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content
        lines = content.strip().split("\n")

        flashcards = []
        section = ""
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line.lower().startswith("section:"):
                section = line.split(":", 1)[1].strip()
                i += 1
                continue

            if line.lower().startswith("q"):
                question = line.split(":", 1)[-1].strip()
                answer = lines[i+1].split(":", 1)[-1].strip() if i+1 < len(lines) else ""
                difficulty = lines[i+2].split(":", 1)[-1].strip() if i+2 < len(lines) else "Medium"
                flashcards.append({
                    "Section": section or "General",
                    "Question": question,
                    "Answer": answer,
                    "Difficulty": difficulty
                })
                i += 3
            else:
                i += 1

        return flashcards

    except Exception as e:
        st.error(f"Error generating flashcards: {e}")
        return []

def export_flashcards(df, format):
    if format == "CSV":
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "flashcards.csv", "text/csv")
    elif format == "JSON":
        json_data = df.to_json(orient="records", indent=2)
        st.download_button("Download JSON", json_data, "flashcards.json", "application/json")
