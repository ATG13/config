#!/usr/bin/python3

import sys

for line in sys.stdin:
    line = line.strip()
    try:
        timestamp, user_id, page_url = line.split(',')
        print(f"{page_url}\t1")
    except ValueError:
        # Handle cases where the line doesn't have the expected format
        pass