#!/usr/bin/python3

import sys

current_page = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    page, count = line.split('\t', 1)

    try:
        count = int(count)
    except ValueError:
        continue # Skip lines that cannot be converted to integer

    if current_page == page:
        current_count += count
    else:
        if current_page:
            print(f"{current_page}\t{current_count}")
        current_count = count
        current_page = page

if current_page:
    print(f"{current_page}\t{current_count}")