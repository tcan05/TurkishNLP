import re, json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, "wikipedia_shortened2.txt")

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zçğıöşü\s]', ' ', text)
    text = re.sub(r'\s+', '_', text).strip()
    return text


# Regex-based syllabifier
def syllabify(word):
    pattern = r'[^aeıioöuü]*[aeıioöuü]+(?:[^aeıioöuü]*$|[^aeıioöuü](?=[^aeıioöuü]))?'
    return re.findall(pattern, word)

def syllabify_sentence(sentence):

    words = sentence.split()
    syllables = []

    for w in words:
        syllables.extend(syllabify(w))

    return syllables


# Syllabify
syllable_list = []

for line in lines:

    clean_line = clean_text(line)

    if not clean_line:
        continue

    syllables = syllabify_sentence(clean_line)
    syllable_list.extend(syllables)


print("Total syllables:", len(syllable_list))


with open("syllables.json", "w", encoding="utf-8") as f:
    json.dump(syllable_list, f, ensure_ascii = False, indent = 2)