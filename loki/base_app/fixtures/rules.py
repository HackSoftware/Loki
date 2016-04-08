def get_id():
    current = 0

    def inner(*args, **kwargs):
        nonlocal current
        current += 1
        return current

    return inner

# RULE = {
#     'DELETE': ['field_name'],
#     'RENAME': [('field_name1', 'field_name2')],
#     'ADD': [('model', 'base_app.academy'), ('pk', 0)],
#     'RESTRUCTURE': [{'fields': ['name', 'city'], 'into': 'fields'}],
#     'TRANSFORM': [('pk', get_id())]
# }

RULE = {
    'DELETE': ['pk'],
    'RENAME': [],
    'ADD': [],
    'RESTRUCTURE': [],
    'TRANSFORM': []
}
