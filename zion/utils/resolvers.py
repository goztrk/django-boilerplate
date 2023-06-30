"""
Module resolvers
"""
# Python Standard Library
import typing as t

# Django Imports
from django.apps import (
    apps,
)

# ZION Shared Library Imports
from zion.decorators import (
    memoize,
)


def split_module_name_parts(
    module_str: str,
) -> t.Tuple[t.Optional[str], t.Optional[str]]:
    """split_module_name_parts

    Gets the name parts of a module string

    Args:
        module_str (str): module path with dot notation

    Returns:
        Tuple[Optional[str], Optional[str]]: Module part and attribute name
    """
    module_name = None
    attr_name = None
    module_str = module_str.strip()
    if module_str and "." in module_str:
        module_name, attr_name = module_str.rsplit(".", 1)

    return module_name, attr_name


@memoize
def resolve_method(module_str: str) -> t.Optional[object]:
    """resolve_method

    Returns the method for a module

    Args:
        module_str (str): module path with dot notation

    Returns:
        object: function or class or `None` if not found
    """
    (
        module_name,
        attr_name,
    ) = split_module_name_parts(module_str)
    if not module_name or not attr_name:
        return None

    try:
        module = __import__(module_name)
    except ModuleNotFoundError:
        return None

    try:
        method = getattr(module, attr_name)
    except AttributeError:
        return None
    else:
        return method


@memoize
def resolve_model(module_str: str):
    """resolve_model

    Resolve and returns model dynamically

    Args:
        module_str (str): Model path with dot notation

    Returns:
        Model: Resolved model or `None`
    """
    (
        module_name,
        attr_name,
    ) = split_module_name_parts(module_str)
    if module_name and attr_name:
        model = apps.get_model(module_name, attr_name)
        return model
    return None
