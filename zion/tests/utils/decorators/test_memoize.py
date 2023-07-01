# Third Party (PyPI) Imports
import pytest

# ZION Shared Library Imports
from zion.decorators import memoize


class TestGroup:
    """
    Tests for @memoize decorator
    """

    def test_valid_input(self):
        """
        Tests that the function returns the correct output for valid input
        """

        @memoize
        def add(a, b):
            return a + b

        assert add(1, 2) == 3
        assert add(3, 4) == 7

    def test_cached_output(self):
        """
        Tests that the function caches the output for repeated input
        """

        @memoize
        def add(a, b):
            return a + b

        assert add(1, 2) == 3
        assert add(1, 2) == 3

    def test_different_input_types(self):
        """
        Tests that the function works correctly for different input types
        """

        @memoize
        def add(a, b):
            return a + b

        assert add(1, 2) == 3
        assert add("a", "b") == "ab"

    def test_empty_input(self):
        """
        Tests that the function works correctly for empty input
        """

        @memoize
        def add():
            return 0

        assert add() == 0
        assert add() == 0

    def test_large_input(self):
        """
        Tests that the function works correctly for large input
        """

        @memoize
        def add(a, b):
            return a + b

        assert (
            add(
                1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,  # noqa: E501
                1,
            )
            == 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001  # noqa: E501
        )
        assert add(100, 200) == 300

    def test_invalid_input_types(self):
        """
        Tests that the function works correctly for invalid input types
        """

        @memoize
        def add(a, b):
            return a + b

        with pytest.raises(TypeError):
            add([], [])
        with pytest.raises(TypeError):
            add({}, {})

    def test_uncacheable_input_types(self):
        """
        Tests that the function raises an error for uncacheable input types
        """

        @memoize
        def func(lst):
            return sum(lst)

        with pytest.raises(TypeError):
            func([1, 2, [3, 4]])

    def test_default_arguments(self):
        """
        Tests that the function works correctly for functions with default arguments
        """

        @memoize
        def add(a, b=1):
            return a + b

        assert add(1) == 2
        assert add(1) == 2
        assert add(2) == 3
        assert add(2) == 3
        assert add(1, 2) == 3
        assert add(1, 2) == 3
        assert add(2, 3) == 5
        assert add(2, 3) == 5

    def test_variable_arguments(self):
        """
        Tests that the function works correctly for functions with variable arguments
        """

        @memoize
        def add(*args):
            return sum(args)

        assert add(1, 2, 3) == 6
        assert add(1, 2, 3) == 6
        assert add(4, 5, 6) == 15
        assert add(4, 5, 6) == 15

    def test_keyword_arguments(self):
        """
        Tests that the function works correctly for functions with keyword arguments
        """

        @memoize
        def add(a, b):
            return a + b

        assert add(a=1, b=2) == 3
        assert add(a=1, b=2) == 3
        assert add(b=2, a=1) == 3
        assert add(b=2, a=1) == 3
