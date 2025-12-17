import re

# Small curated drug list (can be expanded later)
KNOWN_DRUGS = [
    "atorvastatin",
    "paracetamol",
    "ibuprofen",
    "aspirin",
    "metformin",
    "amoxicillin",
    "ciprofloxacin",
    "diclofenac",
    "statin"
]

def extract_drugs(text: str):
    if not text:
        return []

    text = text.lower()
    found = []

    for drug in KNOWN_DRUGS:
        pattern = r"\b" + re.escape(drug) + r"\b"
        if re.search(pattern, text):
            found.append(drug)

    return list(set(found))