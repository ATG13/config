import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def rewrite_paragraph_with_ai(paragraph_text, keywords):
    """
    Rewrites a given paragraph using an AI model, incorporating specific keywords.

    Args:
        paragraph_text (str): The original paragraph to be rewritten.
        keywords (list): A list of words to be incorporated or emphasized in the rewritten paragraph.

    Returns:
        str: The rewritten paragraph.
    """
    try:
        # Configure the Google Generative AI with an API key.
        # This API key will be automatically provided by the Canvas environment.
        # If running outside Canvas, you would need to set an environment variable 'GOOGLE_API_KEY'
        # or provide it directly.
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            # Fallback for local testing if API_KEY is not set as an environment variable
            # In a real application, you'd prompt the user or load from a config file.
            print("Warning: GOOGLE_API_KEY environment variable not set. Please set it for Gemini API access.")
            return "AI model not configured. Please provide an API key."
        
        genai.configure(api_key=api_key)

        # Initialize the Gemini-2.0-flash model
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Construct the prompt for the AI model
        prompt = (
            f"Rewrite the following paragraph, making it more engaging and sophisticated. "
            f"Try to incorporate or reflect the following concepts/words: {', '.join(keywords)}. "
            f"Original Paragraph:\n\n'{paragraph_text}'\n\nRewritten Paragraph:"
        )

        print("Generating rewritten paragraph with AI (this might take a moment)...")
        # Make the API call to generate content
        response = model.generate_content(prompt)

        # Return the generated text
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            return "Could not generate rewritten paragraph. The AI model response was empty or malformed."

    except Exception as e:
        return f"An error occurred while communicating with the AI model: {e}"

if __name__ == "__main__":
    # Inbuilt list of words
    inbuilt_words = ["innovation", "synergy", "paradigm shift", "dynamic", "transformative"]

    # Inbuilt paragraph
    original_paragraph = """
    The company launched a new product. It is expected to improve efficiency.
    The team worked hard to bring this to market. We are hopeful it will succeed.
    """

    print("--- Original Paragraph ---")
    print(original_paragraph.strip())
    print("\n--- Inbuilt Keywords ---")
    print(inbuilt_words)

    # Rewrite the paragraph using the AI model
    rewritten_paragraph = rewrite_paragraph_with_ai(original_paragraph, inbuilt_words)

    print("\n--- Rewritten Paragraph (by AI) ---")
    print(rewritten_paragraph)
