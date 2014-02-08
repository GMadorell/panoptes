import re

match_number_in_brackets = re.compile(r"\{\d+\}")

match_word_in_brackets = re.compile(r"\{[A-Za-z_]+\}")

match_alphanumerical_in_brackets = re.compile(r"\{[A-Za-z0-9_]+\}")

match_any_text = re.compile(r"[a-zA-Z, ]+")
