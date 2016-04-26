import json

file = open('universities_in_bulgaria.json', 'r')
json_text = file.read()
json_data = json.loads(json_text)

print(len(json_data))

lenght = len(json_data)
a, b = 0, 1
while a != lenght:
    while b != lenght:
        if json_data[a] == json_data[b]:
            print('Match found')
        b += 1
    a += 1
    b = a + 1

file.close()
