#Basic Caeser Cipher

text = 'I am gay'
shift = 3
alphabet = 'abcdefghijklmnopqrstuvwxyz'
cipher = ''

for char in text.lower():
    index = alphabet.find(char)
    new_index = (index + shift)% len(alphabet)
    new_char = alphabet[new_index]
    print(new_char)
    cipher += new_char

print(cipher)

