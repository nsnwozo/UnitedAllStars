from unittest.mock import MagicMock, patch

from app.sms_sender import TwilioSmsSender


@patch("app.sms_sender.Client")
def test_send_calls_twilio_with_expected_args(mock_client_cls):
    mock_client = MagicMock()
    mock_message = MagicMock(sid="SM123", status="queued")
    mock_client.messages.create.return_value = mock_message
    mock_client_cls.return_value = mock_client

    sender = TwilioSmsSender(account_sid="AC123", auth_token="token", from_number="+15555550123")
    sid = sender.send(to_number="+15551234567", body="Hello")

    mock_client.messages.create.assert_called_once_with(
        to="+15551234567", from_="+15555550123", body="Hello"
    )
    assert sid == "SM123"
