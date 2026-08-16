#!/usr/bin/python3
import sys

current_word = {}

for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t', 1)

    try:
        count = int(count)
    except ValueError:
        continue

    try:
        current_word[word] = current_word[word] + count
    except KeyError:
        current_word[word] = count

for word, count in current_word.items():
    print(f"{word}\t{count}")