emoji_dict = {
    "happy": "😊",
    "love": "❤️",
    "fire": "🔥",
    "sad": "😢",
    "cat": "🐱",
    "dog": "🐶",
    "smile": "😄",
    "angry": "😡",
    "cool": "😎",
}

import string

def emoji_translate(text):
    # Lowercase and remove punctuation
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize
    words = text.split()
    
    # Replace words by emojis according to dictionary
    translated_words = [emoji_dict.get(word, word) for word in words]
    
    # Join back to string
    return ' '.join(translated_words)