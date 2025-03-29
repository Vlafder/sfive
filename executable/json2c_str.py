import json

with open('../firmware/plot_templates.json', 'r') as file:
    data = json.load(file)
data = '"' + str(data).replace("'", "\\\"") + '"'

print(data)