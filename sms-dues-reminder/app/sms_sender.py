"""Thin wrapper around the Twilio SMS API."""

import logging

from twilio.rest import Client


logger = logging.getLogger("sms_dues_reminder")


class TwilioSmsSender:
    def __init__(
        self,
        account_sid: str,
        api_key: str,
        api_secret: str,
        from_number: str,
    ):
        self._client = Client(
            api_key,
            api_secret,
            account_sid,
        )
        self._from_number = from_number

    def send(self, to_number: str, body: str) -> str:
        message = self._client.messages.create(
            to=to_number,
            from_=self._from_number,
            body=body,
        )

        logger.info(
            "Sent SMS sid=%s to=%s status=%s",
            message.sid,
            to_number,
            message.status,
        )

        return message.sid
