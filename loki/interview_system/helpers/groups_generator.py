from itertools import groupby, chain


def cycle_groups_generator(ns, key=None):

    groups = []

    for _, group in groupby(ns, key=key):
        groups.append(list(group))

    while sum(len(g) for g in groups) != 0:
        current_result = []

        for group in groups:
            if group:
                x = group.pop(0)
                current_result.append(x)

        yield current_result


def cycle_groups(ns, key=None):
    return list(chain.from_iterable(cycle_groups_generator(ns, key=key)))
