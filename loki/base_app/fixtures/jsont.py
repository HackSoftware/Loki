import json


def rename(data, rename_rules):
    for old, new in rename_rules:
        old_parts = old.split(".")

        for key in data:
            if key == old_parts[-1]:
                print(key)

        if key == old:
            return new

    return data


def add(data, to_add):
    for key, value in to_add:
        data[key] = value

    return data


def restructure(data, restructure_rules):
    if len(restructure_rules) == 0:
        return data

    new = {}
    for rule in restructure_rules:
        if rule['into'] not in data:
            new[rule['into']] = {}
        else:
            new[rule['into']] = {key: data[rule['into']][key] for key in data[rule['into']]}

        new[rule['into']].update({key: data[key] for key in rule['fields']})
        new.update({key: data[key] for key in data if key not in rule['fields'] if key != rule['into']})

    return new


def transform(data, transform_rules):
    for field, transform_obj in transform_rules:

        if isinstance(transform_obj, str):
            data[field] = transform_obj

        if isinstance(transform_obj, dict):
            data[field] = transform_obj[data[field]]

        if callable(transform_obj):
            data[field] = transform_obj(data[field])

    return data


def modify_json(data, rules):
    result = []
    for item in data:
        trans = rename(item, rules['RENAME'])
        # trans = {rename(k, rules['RENAME']): item[k] for k in item if k not in rules['DELETE']}
        trans = add(trans, rules['ADD'])
        trans = transform(trans, rules['TRANSFORM'])
        trans = restructure(trans, rules['RESTRUCTURE'])
        print(trans)

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


# rules = {
#     'DELETE': ['Брои', 'Основано', "Студенти[3]"],
#     'RENAME': [('Висше училище', 'name'), ('Седалище', 'city')],
#     'ADD': [('model', 'base_app.university'), ('pk', 0)],
#     'RESTRUCTURE': [{'fields': ['city', 'name'], 'into': 'fields'}],
#     'TRANSFORM': [('city', cities), ('pk', get_id())]
# }

rules = {
    'DELETE': [],
    'RENAME': [],
    'ADD': [('model', 'base_app.academy'), ('pk', 0)],
    'RESTRUCTURE': [{'fields': ['name', 'city'], 'into': 'fields'}],
    'TRANSFORM': [('pk', get_id())]
}

with open('./academies_in_bulgaria.json', 'r') as f:
    data = json.load(f)

print(json.dumps(modify_json(data, rules), indent=4, ensure_ascii=False))
