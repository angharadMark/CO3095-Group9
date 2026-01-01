import json
import os

def export_data(user):
    user_data = user.to_dict()
    export_path = f"{user.username}_data.json"

    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=2, ensure_ascii=False)
    
    print(f"Your user data has been exported! You can find it here: {os.path.abspath(export_path)}")
