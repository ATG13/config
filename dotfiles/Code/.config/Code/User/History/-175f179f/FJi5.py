import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# A list with words
words = []

# Init the AI model with the prompt
api_key = os.getenv("GOOGLE_API_KEY")
instructions = os.getenv("INSTRUCTIONS")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=instructions)

prompt = (
    f"Rewrite the following paragraph, making it more engaging and sophisticated. "
    f"Try to incorporate or reflect the following concepts/words: {', '.join(keywords)}. "
    f"Original Paragraph:\n\n'{paragraph_text}'\n\nRewritten Paragraph:"
)

print(prompt)

def rephrase(para, words):
    out_para = ""
    return out_para