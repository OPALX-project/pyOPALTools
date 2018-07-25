import re

# 2. Mai 2018
# https://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


# 2. Mai 2018
# https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return None


def sort_list(names, dimension, key):
    natsort_names = natural_sort(names)
    natsort_dimension = []
    for name in natsort_names:
        idx = find(dimension, 'label', name)
        natsort_dimension.append(dimension[idx])
    return natsort_dimension
