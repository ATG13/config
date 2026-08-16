#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.strip()
    if line:
        try:
            timestamp, user_id, page_url = line.split(',')
            print(f"{page_url}\t1")
        except ValueError:
            pass 