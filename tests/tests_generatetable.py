# pytest tests/test_generatetable.py
from utils.functions import generate_html_table

def test_generate_html_table():
    variables = [
        {"name": "TestVar1", "value": "123", "description": "This is a test variable"},
    ]
    expected_html = (
        "<table>"
        "<tr><th>Variable</th><th>Value</th><th>Description</th></tr>"
        "<tr><td>TestVar1</td><td>123</td><td>This is a test variable</td></tr>"
        "</table>"
    )
    assert generate_html_table(variables) == expected_html
def test_generate_html_table():
    variables = [
        {"name": "TestVar1", "value": "123", "description": "This is a test variable"},
    ]
    expected_html = (
        "<table>"
        "<tr><th>Variable</th><th>Value</th><th>Description</th></tr>"
        "<tr><td>TestVar1</td><td>123</td><td>This is a test variable</td></tr>"
        "</table>"
    )
    assert generate_html_table(variables) == expected_html
