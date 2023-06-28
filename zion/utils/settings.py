# Python Standard Library
import contextlib
import types
import typing as t
from importlib.resources import (
    as_file,
    files,
)


# If resources are located in archives, importlib will create temporary
# files to access them contained within contexts, we track the contexts
# here as opposed to the _Resource.__del__ method because invocation of
# that method is non-deterministic
__resource_file_contexts__: t.List[contextlib.ExitStack] = []

Package: t.TypeAlias = t.Union[str, types.ModuleType]


def resource(package: Package, filename: str) -> str:
    """
    Include a packaged resource as a settings file.

    Args:
        package: the package as either an imported module, or a string
        filename: the filename of the resource to include.

    Returns:
        New instance of :class:`_Resource`.
    """
    return _Resource(package, filename)


class _Resource(str):
    """
    Wrap an included package resource as a str.

    Resource includes may also be wrapped as Optional an record if the
    package was found or not.
    """

    module_not_found = False
    package: str
    filename: str

    def __new__(cls, package: Package, filename: str) -> "_Resource":
        try:
            ref = files(package) / filename
        except ModuleNotFoundError:
            _resource = super().__new__(cls, "")
            _resource.module_not_found = True
            return _resource

        file_manager = contextlib.ExitStack()
        __resource_file_contexts__.append(file_manager)
        return super().__new__(cls, file_manager.enter_context(as_file(ref)))

    def __init__(self, package: Package, filename: str) -> None:
        super().__init__()
        if isinstance(package, types.ModuleType):
            self.package = package.__name__
        else:
            self.package = package
        self.filename = filename

    def __repr__(self):
        return f"_Resource(package={self.package}, filename='{self.filename}')"

    def __str__(self):
        return f"Resource: {self.filename}"
