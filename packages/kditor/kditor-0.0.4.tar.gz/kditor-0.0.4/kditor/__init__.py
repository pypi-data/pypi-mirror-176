import re
from typing import Dict, Tuple


def search_path(
    obj: Dict,
    path: str,
    key_not_found=lambda _, o: (False, o),
    need_append=lambda _, o: (False, o),
    index_invalid=lambda _, o: (False, o),
) -> Tuple[bool, Dict, str]:
    """search_path is a method that will search a python object by the given path.
    When it reach the target, it will return target's value.
    Otherwise, it will call different method based on different situation.

    Args:
        obj (Dict): Python dictionary that is goting to be searched
        path (str): Path to the target
        key_not_found (str, Any): Triggered when the given key is not found
        need_append (str, Any): Triggered when the given index is the next index of the list
        index_invalid (str, Any): Triggered when the given index is an invalid index of the list

    Raises:
        TypeError: Raised if user trying to get item by index from a non-list obj

    Returns:
        Tuple[bool, Dict, str]: is success, last object, last searched path
    """
    partial_obj = obj
    path_list = path.split(".")
    searched_path = []
    for prop in path_list:
        # Check if prop is trying to find an item from a list
        brackets = re.search(r"(.*)\[(\d+)\]", prop)
        if brackets:
            prop = str(brackets.group(1))
            list_index = int(brackets.group(2))
            if prop not in partial_obj:
                if list_index == 0:
                    # User is trying to create a new list with a single item
                    keep_search, partial_obj = key_not_found(
                        f"{prop}[{list_index}]", partial_obj
                    )
                else:
                    # User is trying to create a new list but provides an invalid index
                    keep_search, partial_obj = index_invalid(
                        f"{prop}[{list_index}]", partial_obj
                    )
                if not keep_search:
                    return False, partial_obj, ".".join(searched_path)
            else:
                if type(partial_obj[prop]) is not list:
                    # Wrong data type, raise an error
                    raise TypeError(
                        f"{'.'.join(searched_path)}.{prop} should be a list"
                    )
                elif len(partial_obj[prop]) == list_index:
                    # Required index is not in the list, but can be append to the end of list
                    keep_search, partial_obj = need_append(
                        f"{prop}[{list_index}]", partial_obj
                    )
                    if not keep_search:
                        return False, partial_obj, ".".join(searched_path)
                elif len(partial_obj[prop]) < list_index:
                    # Required index is not in the list, and cannot append to the end of list
                    keep_search, partial_obj = index_invalid(
                        f"{prop}[{list_index}]", partial_obj
                    )
                    if not keep_search:
                        return False, partial_obj, ".".join(searched_path)
                else:
                    partial_obj = partial_obj[prop][list_index]
        else:
            if prop not in partial_obj:
                keep_search, partial_obj = key_not_found(prop, partial_obj)
                if not keep_search:
                    return False, partial_obj, ".".join(searched_path)
            else:
                partial_obj = partial_obj[prop]
        searched_path.append(prop)
    return True, partial_obj, ".".join(path_list)


def edit(yaml_obj: Dict, path: str, value):
    invalid_index_err = lambda x: IndexError(
        f"{x} is an invalid index! The list will have empty entry after insertion"
    )

    def key_not_found(prop, obj):
        brackets = re.search(r"(.*)\[(\d+)\]", prop)
        new_obj = {}
        if brackets:
            prop = str(brackets.group(1))
            obj[prop] = [new_obj]
        else:
            obj[prop] = new_obj
        return True, new_obj

    def need_append(prop, obj):
        new_obj = {}
        brackets = re.search(r"(.*)\[(\d+)\]", prop)
        prop = str(brackets.group(1))
        obj[prop].append(new_obj)
        return True, new_obj

    def index_invalid(prop, _):
        raise invalid_index_err(prop)

    path = path.split(".")
    if len(path) == 1:
        success, obj = True, yaml_obj
    else:
        before_the_last = ".".join(path[:-1])
        success, obj, _ = search_path(
            yaml_obj, before_the_last, key_not_found, need_append, index_invalid
        )

    if success:
        prop = path[-1]
        brackets = re.search(r"(.*)\[(\d+)\]", prop)
        if brackets:
            prop = str(brackets.group(1))
            list_index = str(brackets.group(2))
            if prop in obj:
                if list_index < len(obj[prop]):
                    obj[prop][list_index] = value
                elif list_index == len(obj[prop]):
                    obj[prop].append(value)
                else:
                    raise invalid_index_err(f"{prop}[{list_index}]")
            elif int(list_index) == 0:
                obj[prop] = [value]
            else:
                raise invalid_index_err(f"{prop}[{list_index}]")
        else:
            obj[path[-1]] = value
    return yaml_obj


def conditional_edit(yaml_obj: Dict, path: str, value, decide_path: str, condition):
    success, result, _ = search_path(yaml_obj, decide_path)
    if (success and result == condition) or (not success and condition is None):
        yaml_obj = edit(yaml_obj, path, value)
    return yaml_obj


def mapping_edit(yaml_obj: Dict, path: str, value: Dict, key_path: str):
    success, key, _ = search_path(yaml_obj, key_path)
    if success and key in value:
        yaml_obj = edit(yaml_obj, path, value[key])
    return yaml_obj
