#!/usr/bin/env python3
"""Unit tests for utils functions"""
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
        # Create Mock object with json method that returns test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        
        # Patch 'requests.get' to return our mock response
        with patch('requests.get', return_value=mock_response) as mock_get:
            # Call the function under test
            result = get_json(test_url)
            
            # Assert requests.get was called exactly once with test_url
            mock_get.assert_called_once_with(test_url)
            
            # Assert the output of get_json equals test_payload
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test case for memoization decorator"""
    
    def test_memoize(self):
        """Test that when calling a_property twice, a_method is only called once"""
        
        class TestClass:
            """Test class for memoization"""
            
            def a_method(self):
                """Method to be memoized"""
                return 42

            @memoize
            def a_property(self):
                """Property that uses memoization decorator"""
                return self.a_method()
        
        test_obj = TestClass()
        
        # Mock a_method
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            # Call a_property twice
            first_call = test_obj.a_property
            second_call = test_obj.a_property
            
            # Assert a_method was only called once
            mock_method.assert_called_once()
            
            # Assert both calls return the expected result
            self.assertEqual(first_call, 42)
            self.assertEqual(second_call, 42)
