# Python Standard Library
import os

# ZION Shared Library Imports
from zion.utils.resolvers import (
    resolve_method,
    split_module_name_parts,
)


class TestSplitModuleNameParts:
    def test_single_attribute_name(self):
        """
        Tests that the function correctly splits a module string with a single attribute name
        """
        module_str = "module.attribute"
        expected_module_name = "module"
        expected_attr_name = "attribute"
        module_name, attr_name = split_module_name_parts(module_str)
        assert module_name == expected_module_name
        assert attr_name == expected_attr_name

    def test_multiple_attribute_names(self):
        """
        Tests that the function correctly splits a module string with multiple attribute names
        """
        module_str = "module.submodule.attribute"
        expected_module_name = "module.submodule"
        expected_attr_name = "attribute"
        module_name, attr_name = split_module_name_parts(module_str)
        assert module_name == expected_module_name
        assert attr_name == expected_attr_name

    def test_empty_module_string(self):
        """
        Tests that the function returns None for an empty module string
        """
        module_str = ""
        expected_module_name = None
        expected_attr_name = None
        module_name, attr_name = split_module_name_parts(module_str)
        assert module_name == expected_module_name
        assert attr_name == expected_attr_name

    def test_no_attribute_name(self):
        """
        Tests that the function correctly splits a module string with no attribute name
        """
        module_str = "module."
        expected_module_name = "module"
        expected_attr_name = ""
        module_name, attr_name = split_module_name_parts(module_str)
        assert module_name == expected_module_name
        assert attr_name == expected_attr_name

    def test_no_module_name(self):
        """
        Tests that the function correctly splits a module string with no module name
        """
        module_str = ".attribute"
        expected_module_name = ""
        expected_attr_name = "attribute"
        module_name, attr_name = split_module_name_parts(module_str)
        assert module_name == expected_module_name
        assert attr_name == expected_attr_name

    def test_special_characters(self):
        """
        Tests that the function correctly splits a module string with special characters
        """
        module_str = "module.sub-module.attribute"
        expected_module_name = "module.sub-module"
        expected_attr_name = "attribute"
        module_name, attr_name = split_module_name_parts(module_str)
        assert module_name == expected_module_name
        assert attr_name == expected_attr_name

    def test_behaviour(self):
        """
        Tests that the function 'split_module_name_parts' correctly splits a
        module string with non-alphanumeric characters into module and attribute
        name parts
        """
        module_str = "my_module.my_class-1"
        expected_module_name = "my_module"
        expected_attr_name = "my_class-1"
        actual_module_name, actual_attr_name = split_module_name_parts(module_str)
        assert actual_module_name == expected_module_name
        assert actual_attr_name == expected_attr_name

    def test_behaviour_long_module_name(self):
        """
        Tests that the function 'split_module_name_parts' correctly splits a
        module string with a very long module name into its module part and
        attribute name
        """
        module_str = "very.long.module.name.with.many.parts"
        expected_module_name = "very.long.module.name.with.many"
        expected_attr_name = "parts"
        module_name, attr_name = split_module_name_parts(module_str)
        assert module_name == expected_module_name
        assert attr_name == expected_attr_name


class TestResolveMethod:
    def test_valid_module_string_returns_method(self):
        """
        Tests that a valid module string returns a method
        """
        method = resolve_method("os.path")
        assert method == os.path

    def test_valid_module_string_with_function_returns_function(self):
        """
        Tests that a valid module string with a function returns the function
        """
        method = resolve_method("os.getcwd")
        assert method == os.getcwd

    def test_empty_string_returns_none(self):
        """
        Tests that an empty string returns None
        """
        method = resolve_method("")
        assert method is None

    # Tests that resolve_method returns None when given a module string with an invalid module name
    def test_invalid_module_name_returns_none(self):
        assert resolve_method("invalid_module_name.invalid_attr_name") is None

    # Tests that a module string with an invalid attribute name returns None
    def test_invalid_attribute_name_returns_none(self):
        assert resolve_method("module.invalid") is None

    # Tests that the function returns None if the module is not found
    def test_behaviour_non_existent(self):
        assert resolve_method("nonexistent_module.nonexistent_function") is None

    # Tests that resolve_method returns None if the attribute is not callable
    def test_behaviour(self):
        assert resolve_method("os.path.join") is None

    # Tests that resolve_method returns None if the attribute is a private method or attribute
    def test_private_method(self):
        assert resolve_method("os._exit") == os._exit

    # Tests that resolve_method returns None if the attribute is not a class or function
    def test_resolve_method_returns_none_if_attribute_not_class_or_function(self):
        assert resolve_method("os.path.join") is None
        assert resolve_method("os") is None
