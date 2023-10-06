import json
fs = open("./rules.json","r")
data = json.loads(fs.read())
fs.close()

for v in data:
    print(f"{v['id']}:{v['name']}")