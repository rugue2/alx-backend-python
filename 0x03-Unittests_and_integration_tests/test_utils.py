#!/usr/bin/env python3
"""Tests for utils module.            """Test memoization"""""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test case for access_nested_map function"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """Test that access_nested_map raises KeyError when expected"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{expected}'")


class TestGetJson(unittest.TestCase):
    """Tests for utils.get_json"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that utils.get_json returns expected result"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch('requests.get', return_value=mock_response) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test case for memoization decorator"""
    def test_memoize(self):
        """Test that when calling a_property twice, a_method is called once"""
        class TestClass:
            """Test class for memoization"""
            def a_method(self):
                """Method to be memoized"""
                return 42

            @memoize
            def a_property(self):
                """Property using memoized method"""
                return self.a_method()

        test_obj = TestClass()
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            first_call = test_obj.a_property
            second_call = test_obj.a_property
            mock_method.assert_called_once()
            self.assertEqual(first_call, 42)
            self.assertEqual(second_call, 42)
