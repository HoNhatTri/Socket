import json

file_name = "/home/vudeptrai/Documents/vu/config.json"
with open(file_name, 'r') as f:
    data = json.load(f)

print(data) 