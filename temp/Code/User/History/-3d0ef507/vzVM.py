from flask import Flask, request, render_template_string
import string

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

def emoji_translate(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    translated_words = [emoji_dict.get(word, word) for word in words]
    return ' '.join(translated_words)

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Emoji Translator</title>
</head>
<body>
    <h1>Emoji Translator</h1>
    <form method="POST">
        <label for="text">Enter your sentence:</label><br>
        <input type="text" id="text" name="text" size="50" value="{{ input_text|default('') }}"><br><br>
        <input type="submit" value="Translate">
    </form>
    {% if result is not none %}
    <h2>Output:</h2>
    <p>{{ result }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    input_text = None
    if request.method == 'POST':
        input_text = request.form.get('text', '')
        result = emoji_translate(input_text)
    return render_template_string(HTML_TEMPLATE, result=result, input_text=input_text)

if __name__ == '__main__':
    app.run(debug=True)
