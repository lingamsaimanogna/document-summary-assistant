import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key)


def generate_summary(text, summary_length):

    length_instructions = {
        "short": "Give a concise summary in about 5 to 7 sentences.",
        "medium": "Give a balanced summary in about 2 to 3 paragraphs.",
        "long": "Give a detailed summary covering the important information and context."
    }

    instruction = length_instructions.get(
        summary_length,
        length_instructions["medium"]
    )

    prompt = f"""
You are a document summarization assistant.

Analyze the document below.

{instruction}

Then provide:

SUMMARY:
A clear summary of the document.

KEY POINTS:
- Important point 1
- Important point 2
- Important point 3
- Add more points if necessary.

Do not invent information that is not present in the document.

DOCUMENT:
{text}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text
