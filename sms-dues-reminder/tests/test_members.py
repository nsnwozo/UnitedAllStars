import pytest

from app.members import _parse_members


def test_parses_valid_members():
    csv_text = (
        "name,phone,balance\n"
        "Jane Doe,+15551234567,125.50\n"
        "John Smith,+15559876543,0\n"
    )
    members = _parse_members(csv_text)

    assert len(members) == 2
    assert members[0].name == "Jane Doe"
    assert members[0].phone == "+15551234567"
    assert members[0].balance == 125.50
    assert members[1].balance == 0


def test_rejects_missing_columns():
    csv_text = "name,phone\nJane Doe,+15551234567\n"
    with pytest.raises(ValueError, match="must contain columns"):
        _parse_members(csv_text)


def test_rejects_invalid_phone_format():
    csv_text = "name,phone,balance\nJane Doe,5551234567,125.50\n"
    with pytest.raises(ValueError, match="E.164 format"):
        _parse_members(csv_text)


def test_rejects_missing_name():
    csv_text = "name,phone,balance\n,+15551234567,125.50\n"
    with pytest.raises(ValueError, match="are required"):
        _parse_members(csv_text)


def test_rejects_invalid_balance():
    csv_text = "name,phone,balance\nJane Doe,+15551234567,not-a-number\n"
    with pytest.raises(ValueError, match="invalid balance"):
        _parse_members(csv_text)
