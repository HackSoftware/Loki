import json
f = open('universities_in_bulgaria.json', 'r')
fin = open('final_cities.json', 'w')

str1 = f.read()
uni = json.loads(str1)
# print(cities)
sofia_uni = []
for i in range(len(uni)):
    lst = uni[i]['fields']['name'].split(' ')
    if "академия" in lst or "Aкадемия" in lst:
        sofia_uni.append(uni[i])
        # print(uni[i])

for i in sofia_uni:
    print(i['fields']['name'])
asd = json.dumps(sofia_uni, fin, ensure_ascii=False, indent=4)
    
fin.write(asd)


fin.close()
f.close()
