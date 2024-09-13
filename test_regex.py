import re

# Regex pattern for host matching
pattern = r"^(api\.tip-lite|tip-lite)"

# Example test
urls = [
    "tip-lite.example.com",
    "api.tip-lite.example.com",
    "somethingelse.example.com",
    "tip-litesomething.example.com",
]

for url in urls:
    if re.search(pattern, url):
        print(f"Match found: {url}")
    else:
        print(f"No match: {url}")
