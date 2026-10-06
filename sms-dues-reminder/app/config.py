import os
from dataclasses import dataclass


DEFAULT_MESSAGE_TEMPLATE = (
    "Hi {name}, this is a gentle reminder that your outstanding UAS dues balance is ${balance}. "
    "Please Zelle your dues payment to unitedallstarsmd@gmail.com at your earliest convenience. "
    "Also, please reach out to the FinSec if you require payment arrangement options. Thank you."
)


@dataclass(frozen=True)
class Settings:
    members_csv_path: str
    twilio_account_sid: str
    twilio_api_key: str
    twilio_api_secret: str
    twilio_from_number: str
    message_template: str

    @staticmethod
    def from_env() -> "Settings":
        required = {
            "MEMBERS_CSV_PATH": os.environ.get("MEMBERS_CSV_PATH"),
            "TWILIO_ACCOUNT_SID": os.environ.get("TWILIO_ACCOUNT_SID"),
            "TWILIO_API_KEY": os.environ.get("TWILIO_API_KEY"),
            "TWILIO_API_SECRET": os.environ.get("TWILIO_API_SECRET"),
            "TWILIO_FROM_NUMBER": os.environ.get("TWILIO_FROM_NUMBER"),
        }

        missing = [key for key, value in required.items() if not value]

        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        return Settings(
            members_csv_path=required["MEMBERS_CSV_PATH"],
            twilio_account_sid=required["TWILIO_ACCOUNT_SID"],
            twilio_api_key=required["TWILIO_API_KEY"],
            twilio_api_secret=required["TWILIO_API_SECRET"],
            twilio_from_number=required["TWILIO_FROM_NUMBER"],
            message_template=os.environ.get(
                "MESSAGE_TEMPLATE",
                DEFAULT_MESSAGE_TEMPLATE,
            ),
        )
