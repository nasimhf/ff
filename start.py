#!/usr/bin/env python3
import sys
import os

sys.path.append("/data/data/com.termux/files/home/ff")

try:
    import tempmail
    tempmail.main()
except Exception as e:
    print(f"Error: {e}")
