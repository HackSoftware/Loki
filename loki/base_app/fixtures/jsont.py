import sys
import json
from rules import RULE


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
    print(rules['DELETE'])
    for item in data:
        for delete in rules['DELETE']:
            if delete in item:
                del item[delete]
        trans = rename(item, rules['RENAME'])
        trans = add(trans, rules['ADD'])
        trans = transform(trans, rules['TRANSFORM'])
        trans = restructure(trans, rules['RESTRUCTURE'])

        result.append(trans)

    return result


def main():
    if len(sys.argv) <= 1:
        print('Provide JSON file as argument')
        sys.exit()

    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    print(json.dumps(modify_json(data, RULE), indent=4, ensure_ascii=False))

if __name__ == '__main__':
    main()
