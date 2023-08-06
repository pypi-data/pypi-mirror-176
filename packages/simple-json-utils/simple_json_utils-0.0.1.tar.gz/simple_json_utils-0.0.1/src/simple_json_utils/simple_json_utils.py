import json

def get_json(fileName):
    with open(fileName, 'r') as f:
        return json.load(f)

def save_json(data: dict, fileName):
    with open(fileName, 'w') as f: 
        json.dump(data, f, indent=4)
    return True
