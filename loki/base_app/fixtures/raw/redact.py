import json
f = open('cities.json', 'r')

str = f.read()
cities = json.loads(str)
for el in cities:
    print(el['name'])

f.close()
