# Regular expressions demo
# pip install regex  # (optional; Python's built-in 're' is used below)
import re

text = "Order #A123 was placed by Alice on 2025-08-30. Email: alice@example.com"

# Match (from start)
m = re.match(r"Order #([A-Z]\d+)", text)
print("match:", m.group(1) if m else None)

# Search (anywhere)
s = re.search(r"\d{4}-\d{2}-\d{2}", text)
print("date found:", s.group(0) if s else None)

# Find all emails
emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
print("emails:", emails)

# Replace digits with X
masked = re.sub(r"\d", "X", text)
print("masked:", masked)
