import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyBQIhGZUYJf4PoMsO4WeWaDK5Ebqc44sHk")

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content('Teach me about how an LLM works')

print(response.text)
