# SMS Dues Reminder

Sends SMS reminders to organization members with outstanding dues balances.
Reads a CSV roster, filters members with a balance > 0, and sends each one a
text via Twilio. A plain local Python script — run it yourself whenever you
want to send a batch of reminders. No servers, containers, or cloud
infrastructure required.

## Project structure

```
sms-dues-reminder/
├── app/
│   ├── main.py          # script entrypoint
│   ├── config.py        # env var based settings
│   ├── members.py       # CSV loading/parsing + validation
│   └── sms_sender.py    # Twilio wrapper
├── tests/                # pytest unit tests
├── sample_data/
│   └── members_sample.csv
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

## CSV format

```csv
name,phone,balance
Jane Doe,+15551234567,125.50
John Smith,+15559876543,0
```

- `phone` must be E.164 format (`+<countrycode><number>`).
- Members with `balance <= 0` are skipped automatically.

## Setup

```powershell
cd sms-dues-reminder
python -m venv .venv
.venv\Scripts\Activate.ps1          # Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt -r requirements-dev.txt

# run tests (no Twilio account needed — the Twilio client is mocked)
pytest -q
```

## Send reminders

1. Edit `sample_data/members_sample.csv` (or point `MEMBERS_CSV_PATH` at your own file) with your real member roster.
2. Set your Twilio credentials and run:

```powershell
$env:MEMBERS_CSV_PATH = "sample_data/members_sample.csv"
$env:TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
$env:TWILIO_AUTH_TOKEN = "your_auth_token"
$env:TWILIO_FROM_NUMBER = "+15555550123"
python -m app.main
```

Run this manually whenever you want to send a new round of reminders (e.g. weekly). There's no scheduler — it only sends when you run it.

> **Twilio free trial**: You get ~$15 of credit, but trial accounts can only
> send to phone numbers you've manually verified in the Twilio console, and
> each message is prefixed with "Sent from your Twilio trial account".
> Upgrade to a paid account before using this for real members.

## Security notes

- Twilio credentials are read from environment variables — never commit real values (see `.env.example` for the placeholder format; `.gitignore` already excludes `.env`).
- Phone numbers and balances are validated before any network call (E.164 format check, numeric balance check) to avoid sending malformed requests.
- Rotate your Twilio auth token periodically from the Twilio Console if it's ever exposed.

