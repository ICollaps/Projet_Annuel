# pytest tests/test_sendemail.py
from unittest.mock import patch, ANY
from utils.functions import send_email

@patch('smtplib.SMTP')
def test_send_email(mock_smtp):
    send_email('Subject', 'Message', 'from@example.com', 'to@example.com', 'password', [])
    mock_smtp.assert_called_with('smtp.gmail.com', 587)
    instance = mock_smtp.return_value
    instance.sendmail.assert_called_with('from@example.com', 'to@example.com', ANY)
