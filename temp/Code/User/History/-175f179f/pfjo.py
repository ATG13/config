import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# A list with words
words = []

# Init the AI model with the prompt
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.0-flash')

instructions = os.getenv("INSTRUCTIONS")

def rephrase(para, words):
    out_para = ""
    return out_para