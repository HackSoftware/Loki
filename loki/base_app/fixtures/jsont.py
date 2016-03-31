import json

def rename(key, rename_rules):
    for old, new in rename_rules:
        if key == old:
            return new

    return key


def add(data, to_add):
    for key, value in to_add:
        data[key] = value

    return data


def restructure(data, restructure_rules):
    new = {}
    for rule in restructure_rules:
        new[rule['into']] = {key: data[key] for key in rule['fields']}
        new.update({key: data[key] for key in data if key not in rule['fields']})

    return new


def transform(data, transform_rules):
    for field, transform_obj in transform_rules:
        if isinstance(transform_obj, dict):
            data[field] = transform_obj[data[field]]

        if callable(transform_obj):
            data[field] = transform_obj(data[field])

    return data


def modify_json(data, rules):
    result = []
    for item in data:
        trans = {rename(k, rules['RENAME']): item[k] for k in item if k not in rules['DELETE']}
        trans = add(trans, rules['ADD'])
        trans = transform(trans, rules['TRANSFORM'])
        trans = restructure(trans, rules['RESTRUCTURE'])

        result.append(trans)

    return result

with open('./cities.json', 'r') as f:
    cities = json.load(f)


def get_id():
    current = 0

    def inner(*args, **kwargs):
        nonlocal current
        current += 1
        return current

    return inner


rules = {
    'DELETE': ['Брои', 'Основано', "Студенти[3]"],
    'RENAME': [('Висше училище', 'name'), ('Седалище', 'city')],
    'ADD': [('model', 'base_app.university'), ('pk', 0)],
    'RESTRUCTURE': [{'fields': ['city', 'name'], 'into': 'fields'}],
    'TRANSFORM': [('city', cities), ('pk', get_id())]
}

with open('./universities_in_bulgaria_raw.json', 'r') as f:
    data = json.load(f)

print(json.dumps(modify_json(data, rules), indent=4, ensure_ascii=False))
