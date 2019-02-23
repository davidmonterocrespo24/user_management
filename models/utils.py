# -*- coding: utf-8 -*-

import unidecode

def del_new(self, values, key, flag):
    A = []
    B = []
    for _key in self[key]:
        A.append(_key.id)
    if values[key]:
        for _key1 in values[key][0][2]:
            B.append(_key1)
    delete_keys = list(set(A)-set(B))
    new_keys = list(set(B)-set(A))
    if flag:
        rest_keys = list(set(A)-set(delete_keys))
        return delete_keys, new_keys, rest_keys
    else:
        return delete_keys, new_keys

def find_bigger(grupos):
    bigger = 0
    if grupos:
        for grupo in grupos:
            if grupo.cuota > bigger:
                bigger = grupo.cuota
    return bigger

def del_accent_nn(accented_string):
    return unidecode.unidecode(accented_string)