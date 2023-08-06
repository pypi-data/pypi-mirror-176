import json

def get_json(filePath: str) -> dict:
    with open(filePath, 'r') as f:
        return json.load(f)

def save_json(data: dict, filePath: str) -> bool:
    with open(filePath, 'w') as f: 
        json.dump(data, f, indent=4)
    return True
