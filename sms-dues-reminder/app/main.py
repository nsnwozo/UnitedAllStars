"""Entry point for the SMS dues reminder script.

Reads a CSV of members (name, phone, balance) from a local file, filters
members with an outstanding balance, and sends each one an SMS reminder via
Twilio. Run this manually whenever you want to send a batch of reminders:

    python -m app.main
"""
import logging
import sys

from app.config import Settings
from app.members import load_members
from app.sms_sender import TwilioSmsSender

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("sms_dues_reminder")


def main() -> int:
    settings = Settings.from_env()

    members = load_members(settings.members_csv_path)
    due_members = [m for m in members if m.balance > 0]

    logger.info("Loaded %d members, %d with outstanding balances", len(members), len(due_members))

    if not due_members:
        logger.info("No members with outstanding dues. Nothing to send.")
        return 0

    
    sender = TwilioSmsSender(
      account_sid=settings.twilio_account_sid,
      api_key=settings.twilio_api_key,
      api_secret=settings.twilio_api_secret,
      from_number=settings.twilio_from_number,
    )

    sent, failed = 0, 0
    for member in due_members:
        message_body = settings.message_template.format(
            name=member.name, balance=f"${member.balance:.2f}"
        ).replace("\\n", "\n")
        try:
            sender.send(to_number=member.phone, body=message_body)
            sent += 1
        except Exception:
            logger.exception("Failed to send SMS to %s", member.phone)
            failed += 1

    logger.info("Done. sent=%d failed=%d", sent, failed)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
