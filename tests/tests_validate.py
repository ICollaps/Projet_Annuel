# pytest tests/test_validate.py
import pytest
from utils.functions import validate_input

def test_validate_input_positive_numbers():
    assert validate_input([1, 2, 3.5]) == True

def test_validate_input_zero():
    assert validate_input([0, 0, 0]) == True

def test_validate_input_negative_numbers():
    assert validate_input([-1, -2, -3]) == False

def test_validate_input_mix_positive_and_negative_numbers():
    assert validate_input([-1, 2, 3]) == False

def test_validate_input_non_numeric():
    assert validate_input(['a', 'b', 'c']) == False

def test_validate_input_mix_numeric_and_non_numeric():
    assert validate_input(['a', 2, 3]) == False
