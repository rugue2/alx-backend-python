#!/usr/bin/env python3
"""Unit tests for utils functions"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json


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
