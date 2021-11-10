from typing import Any, Dict, Optional, Set, Union

mydata = {"id": 22, "user": {"id": 33, "age": 33}, "address": "foo"}


def get(data, include):
    if include == ...:
        return data

    if isinstance(include, set):
        return {key: data[key] for key in include}

    assert isinstance(include, dict)

    return {key: get(data[key], include[key]) for key in include}


def copy_from_dict(data: Dict[str, Any], *, include: Optional[Union[Set, Dict]] = None):
    #
    # Analogous to advanced includes from pydantic exports
    #   https://pydantic-docs.helpmanual.io/usage/exporting_models/#advanced-include-and-exclude
    #
    return get(data, include)


print(get(mydata, include={"user": {"id"}}))
