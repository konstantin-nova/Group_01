"""
This module contains unit tests for the MovieDataAnalyzer class using the
pytest framework.

The tests cover various aspects of the MovieDataAnalyzer class, including
error handling and functionality. Each test function is designed to check
the behavior of specific methods within the MovieDataAnalyzer class under
different conditions and input values.

Tested Methods:
- movie_type: Tests for handling invalid types, negative values, zero values,
and large values.
- actor_distributions: Tests for handling invalid gender types, invalid height
types, and invalid height ranges.

The tests ensure that the methods in the MovieDataAnalyzer class raise
appropriate exceptions (TypeError, ValueError) when provided with invalid
input and return expected results for valid input.

Usage:
- To run these tests, use the pytest framework by executing `pytest` in the
terminal.
"""
import pytest
from movie_data_analysis import (
    MovieDataAnalyzer,
    MovieTypeRequest,
    ActorFilter
    )

# Create an instance of the MovieDataAnalyzer class
analyzer = MovieDataAnalyzer()

# Test Error Handling


def test_movie_type_invalid_n():
    """
    Test that the movie_type function raises a TypeError when the parameter n
    is given an invalid type (string instead of integer).

    This test uses pytest to check that the function correctly handles invalid
    input by raising the appropriate exception.

    Raises:
        TypeError: If the parameter n is not of the expected type.
    """
    with pytest.raises(TypeError):
        analyzer.movie_type(MovieTypeRequest(n="ten"))


def test_movie_type_negative_value():
    """
    Test that the movie_type method raises a ValueError when passed a negative
    value.

    This test ensures that the movie_type method in the analyzer object
    correctly handles invalid input by raising a ValueError when the parameter
    n is negative.
    """
    with pytest.raises(ValueError):
        analyzer.movie_type(MovieTypeRequest(n=-1))


def test_movie_type_zero_value():
    """
    Test that the movie_type method raises a ValueError when called with n=0.

    This test ensures that the movie_type method in the analyzer object
    correctly handles the case where the input value n is zero, which is
    expected to raise a ValueError.

    Raises:
        ValueError: If the input value n is zero.
    """
    with pytest.raises(ValueError):
        analyzer.movie_type(MovieTypeRequest(n=0))


def test_movie_type_large_value():
    """
    Test the movie_type function with a large value for n.

    This test checks if the 'movie_type' key is present in the result when the
    movie_type function is called with n=1000.

    Raises:
        AssertionError: If 'movie_type' is not found in the result.
    """
    result = analyzer.movie_type(MovieTypeRequest(n=1000))
    assert 'movie_type' in result


def test_actor_distributions_invalid_gender():
    """
    Test the actor_distributions function with an invalid gender type.

    This test ensures that the actor_distributions function raises a TypeError
    when the gender parameter is provided with an invalid type (e.g., an
    integer).

    Raises:
        TypeError: If the gender parameter is not of the expected type.
    """
    with pytest.raises(TypeError):
        actor_filter = ActorFilter(gender=123, max_height=2.0, min_height=1.5)
        analyzer.actor_distributions(actor_filter)


def test_actor_distributions_invalid_height_type():
    """
    Test that the actor_distributions function raises a TypeError when an
    invalid type is provided for the max_height parameter.

    This test ensures that the function correctly handles the case where the
    max_height parameter is given a string value instead of a numeric value.

    Raises:
        TypeError: If the max_height parameter is not of a numeric type.
    """
    with pytest.raises(TypeError):
        actor_filter = ActorFilter(gender="M",
                                   max_height="tall",
                                   min_height=1.5)
        analyzer.actor_distributions(actor_filter)


def test_actor_distributions_invalid_height_range():
    """
    Test that the `actor_distributions` method raises a ValueError when the
    minimum height is greater than the maximum height.

    This test ensures that the `actor_distributions` method correctly handles
    invalid height ranges by raising a ValueError when `min_height` is greater
    than `max_height`.

    Raises:
        ValueError: If the `actor_distributions` method does not raise a
        ValueError when `min_height` is greater than `max_height`.
    """
    with pytest.raises(ValueError):
        actor_filter = ActorFilter(gender="M", max_height=1.0, min_height=1.5)
        analyzer.actor_distributions(actor_filter)


def test_actor_distributions_invalid_height_values():
    """
    Test the actor_distributions function for invalid height values.

    This test checks that the actor_distributions function raises a ValueError
    when provided with invalid height ranges. Specifically, it tests the
    following cases:
    1. max_height is less than min_height.
    2. Both max_height and min_height are outside the valid range.

    The function is expected to raise a ValueError in both cases.
    """
    with pytest.raises(ValueError):
        actor_filter = ActorFilter(gender="M", max_height=0, min_height=1.5)
        analyzer.actor_distributions(actor_filter)

    with pytest.raises(ValueError):
        actor_filter = ActorFilter(gender="M", max_height=2.5, min_height=3.5)
        analyzer.actor_distributions(actor_filter)

# Test Functionality


def test_movie_type():
    """
    Test the movie_type function from the analyzer module.

    This test checks if the movie_type function returns the correct movie type
    for a given input. Specifically, it verifies that when n=1, the function
    returns a dictionary where the 'movie_type' key corresponds to the value
    '"/m/07s9rl0": "Drama"'.

    Raises:
        AssertionError: If the returned movie type does not match the expected
        value.
    """
    result = analyzer.movie_type(MovieTypeRequest(n=10))
    assert any("Drama" in movie for movie in result['movie_type'])


def test_actor_distributions():
    """
    Test the actor_distributions function from the analyzer module.

    This test checks if the actor_distributions function returns the correct
    distribution of"
    """
    actor_filter = ActorFilter(gender="M", max_height=2.0, min_height=1.5)
    result = analyzer.actor_distributions(actor_filter)
    assert 'height' in result
