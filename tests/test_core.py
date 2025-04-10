import datetime as dt
import pytest
from core import (
    get_accounting_entry,
    filter_entries_by_item,
    get_accounting_entries,
)
from models.entry import EntryDataModel

@pytest.fixture
def sample_entry_data():
    """Fixture to provide sample entry data."""
    return [
        EntryDataModel(date=dt.datetime(2024, 5, 1), item="Webhosting", invoice_id="INV001", amount=833.33),
        EntryDataModel(date=dt.datetime(2024, 5, 1), item="Domain", invoice_id="INV002", amount=500.00),
        EntryDataModel(date=dt.datetime(2024, 5, 1), item="SSL", invoice_id="INV003", amount=300.00),
    ]

def test_get_accounting_entry():
    """Test generating debit and credit accounting entries."""
    date = dt.date(2024, 5, 31)
    description = "Prepayment amortisation for Webhosting"
    reference = "INV001"
    expense_account = "EXP001"
    prepayment_account = "PRE001"
    amount = 833.33

    debit_entry, credit_entry = get_accounting_entry(
        date=date,
        description=description,
        reference=reference,
        expense_account=expense_account,
        prepayment_account=prepayment_account,
        amount=amount
    )

    # Validate debit entry
    assert debit_entry.date == date
    assert debit_entry.description == description
    assert debit_entry.reference == reference
    assert debit_entry.account == expense_account
    assert debit_entry.amount == -amount

    # Validate credit entry
    assert credit_entry.date == date
    assert credit_entry.description == description
    assert credit_entry.reference == reference
    assert credit_entry.account == prepayment_account
    assert credit_entry.amount == amount

def test_filter_entries_by_item(sample_entry_data):
    """Test filtering entries by item name."""
    filtered_entries = filter_entries_by_item(sample_entry_data, "Webhosting")
    assert len(filtered_entries) == 1
    assert filtered_entries[0].item == "Webhosting"

    filtered_entries = filter_entries_by_item(sample_entry_data, "Domain")
    assert len(filtered_entries) == 1
    assert filtered_entries[0].item == "Domain"

    filtered_entries = filter_entries_by_item(sample_entry_data, "Nonexistent")
    assert len(filtered_entries) == 0

def test_get_accounting_entries(sample_entry_data):
    """Test generating accounting entries from entry data."""
    posting_date = dt.date(2024, 5, 31)
    description_prefix = "Prepayment amortisation for"
    expense_account = "EXP001"
    prepayment_account = "PRE001"

    accounting_entries = get_accounting_entries(
        entry_data_list=sample_entry_data,
        posting_date=posting_date,
        description_prefix=description_prefix,
        expense_account=expense_account,
        prepayment_account=prepayment_account
    )

    assert len(accounting_entries) == 6  # 3 entries * 2 (debit + credit)

    # Validate the first debit and credit entries
    debit_entry = accounting_entries[0]
    credit_entry = accounting_entries[1]

    assert debit_entry.date == posting_date
    assert debit_entry.description == f"{description_prefix} Webhosting"
    assert debit_entry.account == expense_account
    assert debit_entry.amount == -833.33

    assert credit_entry.date == posting_date
    assert credit_entry.description == f"{description_prefix} Webhosting"
    assert credit_entry.account == prepayment_account
    assert credit_entry.amount == 833.33
