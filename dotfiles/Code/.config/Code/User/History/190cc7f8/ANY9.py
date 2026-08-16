# Test run of vocab-graph

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

#Model generated
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 12000,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="You are a program that would rewrite the content provided to you in a paragraph variable with the words mentioned in the word_list variable. You are supposed to maintain the flow, style and content of the paragraph in the same way it has been written. Only use the words from the word_list variable if it makes sense to do so. \nIt is important to maintain the natural flow, so do not force use the words from the list and not add any information not mentioned already.\nThe input prompt would be as follows.\nword_list: \nparagraph: \nThe output of the content should only be the rewritten paragraph with the new words in bold. If there is no input provided, give an output as INVALID INPUT",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "list = [\"unprepossessing\", \"suave\", \"veneer\", \"angst\", \"emulate\"]\nparagraph = “Across the crowded cafe, Ethan, with his perfectly tailored suit and a confident smile, captivated every conversation. At a corner table sat Daniel, his shoulders slumped, eyes downcast, a stark contrast to the vibrant energy swirling around him. Their outward appearances couldn't be more different, but beneath the surface, their stories likely held unexpected depths.”",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Across the crowded cafe, Ethan, with his perfectly tailored suit and a **suave** **veneer**, captivated every conversation. At a corner table sat Daniel, his shoulders slumped, eyes downcast, a stark contrast to the vibrant energy swirling around him. Their outward appearances couldn't be more different, but beneath the surface, their stories likely held unexpected depths. \n",
      ],
    },
  ]
)

word_list = 'word_list: ' + input("> words: \n")
para = 'paragraph: ' + input("> Paragraph: \n")

prompt = str(f'{word_list} \n {para}')

response = chat_session.send_message(prompt)

print(response.text)