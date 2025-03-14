# test_json_util.py

import pytest
from app.utils.JsonUtil import JsonUtil


def test_convert_to_dict_valid_dict():
    input_str = '{"key": "value", "num": 123}'
    result = JsonUtil.convert_to_dict(input_str)
    # Expecting a valid dictionary.
    assert isinstance(result, dict)
    assert result == {"key": "value", "num": 123}


def test_convert_to_dict_invalid_json():
    input_str = '{"key": "value", "num": 123'  # Missing closing brace.
    result = JsonUtil.convert_to_dict(input_str)
    # Should return an empty dictionary.
    assert result == {}


def test_convert_to_dict_with_list_input():
    # Although the docstring says it converts to a dict, the function just does json.loads.
    # In this case, json.loads returns a list.
    input_str = '["a", "b", "c"]'
    result = JsonUtil.convert_to_dict(input_str)
    # We expect a list here because no type-checking is done.
    assert isinstance(result, list)
    assert result == ["a", "b", "c"]


def test_convert_to_list_of_dicts_valid_array():
    input_str = '[{"key": "value"}, {"foo": "bar"}]'
    result = JsonUtil.convert_to_list_of_dicts(input_str)
    assert isinstance(result, list)
    assert result == [{"key": "value"}, {"foo": "bar"}]


def test_convert_to_list_of_dicts_valid_dict():
    input_str = '{"key": "value", "foo": "bar"}'
    result = JsonUtil.convert_to_list_of_dicts(input_str)
    # When a single dict is provided, it should be wrapped in a list.
    assert isinstance(result, list)
    assert result == [{"key": "value", "foo": "bar"}]


def test_convert_to_list_of_dicts_invalid_json():
    input_str = '[{"key": "value"}, {"foo": "bar"'  # Missing closing bracket/brace.
    result = JsonUtil.convert_to_list_of_dicts(input_str)
    # Should return an empty list.
    assert result == []


def test_convert_to_list_of_dicts_unexpected_type():
    # For a JSON that represents a number (unexpected type), it should return an empty list.
    input_str = "123"
    result = JsonUtil.convert_to_list_of_dicts(input_str)
    assert result == []
