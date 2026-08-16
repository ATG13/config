import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# A list with words
words_list = ["innovation", "synergy", "paradigm shift", "dynamic", "transformative"]

paragraph = """
Perplexity has announced that its AI-powered Comet browser is now available to Windows users. The company’s CEO, Aravind Srinivas, confirmed via a post on X that the Windows version of Comet is complete and invites have already been sent out to early testers. Srinivas also mentioned that an Android release is underway and is moving faster than expected.
Earlier this year, Perplexity introduced Comet in a beta form, initially available only to Mac users with Apple Silicon chips. The browser integrates AI tools that let users ask questions, find discounts in shopping carts, and manage emails more efficiently. One notable feature is that it allows users to upload a photo and see how selected clothing items would look on them, which shows the browser’s interactive AI capabilities.
"""

# Init the AI model with the prompt
api_key = os.getenv("GOOGLE_API_KEY")
instructions = os.getenv("INSTRUCTIONS")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=instructions)


def rephrase(para, words):
    prompt = (
        f"para = {para}"
        f"\n"
        f"words = {words}"
    )
    response = model.generate_content(prompt)

    out_para = response.candidates[0].content.parts[0].text
    print(out_para)

rephrase(paragraph, words_list)