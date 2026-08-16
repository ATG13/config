#!/usr/bin/python3

import sys

for line in sys.stdin:
    line = line.strip()  # Remove leading/trailing whitespace
    words = line.split(',')  # Split the line by commas

    for word in words:
        word = word.strip()  # Remove whitespace around each word
        if word: #make sure word is not empty
          print(f"{word}\t1") #output word and count of 1   