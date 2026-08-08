import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def ask_llm(context, question):

    prompt = f"""
You are a Resume Chatbot.

Rules:
- Answer ONLY using the resume context.
- Do not make up information.
- If the answer isn't in the resume, say:
  "I couldn't find that information in the uploaded resume."

Resume Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text