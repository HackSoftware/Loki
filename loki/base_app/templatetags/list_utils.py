from django import template

register = template.Library()

@register.filter
def split_in_groups(items, n):
    try:
        n = int(n)
    except  (ValueError, TypeError):
        return [items]

    groups = []
    
    while len(items) != 0:
        print(items)
        next_group = items[:n]
        groups.append(next_group)

        items = items[n:]

    return groups
