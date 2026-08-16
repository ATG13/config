s = [[1, 2], [3, 4], [5, 6], 7, 8 ]

def flatten(l):
    flatten_list = []
    for item in l:
        if isinstance(item, list):
            flatten_list.extend(flatten(item))
        else:
            flatten_list.append(item)
    return flatten_list

print(flatten(s))