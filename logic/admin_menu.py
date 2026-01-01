import os
dataDir = os.path.join(os.path.dirname(__file__), "..", "data")
profanFile = os.path.join(dataDir, "en.txt")

def add_profan(word):
    with open(profanFile, "a") as f:
        f.write(word + "\n")

def delete_profan(target):
    with open(profanFile, "r") as f:
        lines = f.readlines()
    
    lines_temp = []
    for line in lines:
        if line.strip() != target.strip():
            lines_temp.append(line)
    
    if len(lines_temp) == len(lines):
        return False 
    
    with open(profanFile, "w") as f:
        for line in lines_temp:
            f.writelines(line)

