import re

# Define the regex pattern
pattern = r"^(testing\.)?tip\."
pattern = r"^(testing\.)?s4l[\.-]"

# pattern = r"^(testing\.)?tip-lite[\.-]"

# Test the pattern
test_strings = [
    "testing.osparc.somevalue",
    "testing.tip.io",
    "tip.com",
    "osparc.somevalue",
    "testing-somethingelse",
    "osparc-testing",
]

# Filter strings that match the pattern
matches = [s for s in test_strings if re.match(pattern, s)]

print(matches)
