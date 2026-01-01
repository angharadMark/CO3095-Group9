import os 
import re 

dataDir = os.path.join(os.path.dirname(__file__), "..", "data")
profanFile = os.path.join(dataDir, "en.txt")

def load_profan():
    if not os.path.exists(profanFile):
        return set()
    
    with open(profanFile, "r", encoding="utf-8") as f:
        return {
            line.strip().lower()
            for line in f
                if line.strip() and not line.startswith("#")
        }
    
def censor(text):
    profanity_words = load_profan()

    if not profanity_words:
        return text
    
    def replace(match):
        word = match.group()
        return "*" * len(word)
    
    pattern = r"\b(" + "|".join(map(re.escape, profanity_words)) + r")\b"
    return re.sub(pattern, replace, text, flags=re.IGNORECASE)