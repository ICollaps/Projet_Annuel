# pytest tests/test_createemail.py
from unittest.mock import patch, ANY
from utils.functions import create_email

def test_create_email():
    # Define input parameters
    subject = "Test Subject"
    message = "Test Message"
    from_addr = "from@example.com"
    to_addr = "to@example.com"
    variables = [{'name': 'Var1', 'value': 'Value1', 'description': 'Desc1'}]

    # Call the function with the test inputs
    result = create_email(subject, message, from_addr, to_addr, variables)

    # Assert the resulting email body is correctly formatted
    assert result['Subject'] == subject
    assert result['From'] == from_addr
    assert result['To'] == to_addr

    # Assert that the plain text part is equal to the 'message'
    assert result.get_payload(0).get_payload() == message

    # Assert the HTML part of the email contains certain expected strings
    html_payload = result.get_payload(1).get_payload()
    assert message in html_payload
    assert "<table>" in html_payload
    assert "</table>" in html_payload
    assert 'Var1' in html_payload
    assert 'Value1' in html_payload
    assert 'Desc1' in html_payload
