import json

def find_values(data, key="damageEvent"):
    values = []

    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                values.append(v)
            else:
                values.extend(find_values(v, key))
    elif isinstance(data, list):
        for item in data:
            values.extend(find_values(item, key))
    
    return values

def main(json_file_path):
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)
    print(len(json_data))

    print(find_values(json_data))


json_file_path = "../DATA/game-changers/games/2022/val:0a63934c-9907-4b7c-a553-ac945cc9eea4.json"  
main(json_file_path)
