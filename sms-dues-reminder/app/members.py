"""Loading and parsing the member roster (CSV) from a local file."""
import csv
import io
import re
from dataclasses import dataclass

_E164_PATTERN = re.compile(r"^\+[1-9]\d{6,14}$")
_REQUIRED_COLUMNS = {"name", "phone", "balance"}


@dataclass(frozen=True)
class Member:
    name: str
    phone: str
    balance: float


def load_members(csv_path: str) -> list[Member]:
    """Load and validate members from a local CSV file path."""
    with open(csv_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    return _parse_members(raw_text)


def _parse_members(raw_text: str) -> list[Member]:
    members: list[Member] = []
    reader = csv.DictReader(io.StringIO(raw_text))

    found_columns = {c.strip().lower() for c in (reader.fieldnames or [])}
    if not _REQUIRED_COLUMNS.issubset(found_columns):
        raise ValueError(
            f"CSV must contain columns: {', '.join(sorted(_REQUIRED_COLUMNS))}. "
            f"Found: {reader.fieldnames}"
        )

    for row_num, row in enumerate(reader, start=2):
        normalized = {k.strip().lower(): (v or "").strip() for k, v in row.items()}
        name = normalized.get("name", "")
        phone = normalized.get("phone", "")
        balance_raw = normalized.get("balance", "0") or "0"

        if not name or not phone:
            raise ValueError(f"Row {row_num}: 'name' and 'phone' are required")

        if not _E164_PATTERN.match(phone):
            raise ValueError(
                f"Row {row_num}: phone '{phone}' must be in E.164 format, e.g. +15551234567"
            )

        try:
            balance = float(balance_raw)
        except ValueError as exc:
            raise ValueError(f"Row {row_num}: invalid balance '{balance_raw}'") from exc

        members.append(Member(name=name, phone=phone, balance=balance))

    return members
