
def is_there_any_duplicate(all_results):
    seen = set()
    for element in all_results:
        if element in seen:
            return True
        seen.add(element)
    return False