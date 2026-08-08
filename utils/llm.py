from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

MODEL_NAME = "gemini-3.6-flash"


def ask_llm(context, question):

    prompt = f"""
You are a Resume AI Assistant.

Answer the user's question using ONLY the information
contained in the resume context below.

If the answer is not present in the resume, say:
"I couldn't find that information in the resume."

Resume Context:
{context}

User Question:
{question}

Give a clear and concise answer.
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:

        error_message = str(e)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

            return (
                "⚠️ **Gemini API quota reached.**\n\n"
                "The Gemini API free-tier request limit for this "
                "project/model has been reached.\n\n"
                "Please wait for the quota to reset or check your "
                "Gemini API usage and billing settings."
            )

        return (
            "⚠️ **Unable to generate an answer right now.**\n\n"
            f"Error: `{error_message}`"
        )