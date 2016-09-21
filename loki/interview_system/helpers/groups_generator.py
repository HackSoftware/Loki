from itertools import groupby, chain


def cycle_groups_generator(ns):
   groups = []

   for _, group in groupby(ns):
       groups.append(list(group))

   while sum(len(g) for g in groups) != 0:
       current_result = []

       for group in groups:
           if group:
               x = group.pop(0)
               current_result.append(x)

       yield current_result


def cycle_groups(ns):
   return list(chain.from_iterable(cycle_groups_generator(ns)))
