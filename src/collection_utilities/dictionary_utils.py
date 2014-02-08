
def invert_dictionary(dictionary):
    """
    Creates a new dictionary containing the keys of the given dictionary
    as values and the values as keys.
    Will not work if the given dictionary has repeated values.
    """
    inverted_dic = {}
    for key, value in dictionary.items():
        try:
            inverted_dic[value] = key
        except TypeError, e:
            inverted_dic[str(value)] = key
    return inverted_dic
