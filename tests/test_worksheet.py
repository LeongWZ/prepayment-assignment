import datetime as dt
import pytest
from models.worksheet import PrepaymentScheduleWorksheetModel
from models.entry import EntryDataModel

@pytest.fixture
def sample_cells():
    """Fixture to provide sample worksheet data with proper headers."""
    return [
        ["Invoice ID", "Item", dt.datetime(2024, 5, 1), dt.datetime(2024, 6, 1)],  # Header row with datetime objects
        ["INV001", "Webhosting", 833.33, None],                                   # Row 1
        ["INV002", "Domain", 500.00, None],                                       # Row 2
        ["INV003", "SSL", None, None],                                            # Row 3 (no amount for May or June)
    ]

@pytest.fixture
def worksheet_model(sample_cells):
    """Fixture to initialize PrepaymentScheduleWorksheetModel."""
    return PrepaymentScheduleWorksheetModel(
        cells=sample_cells,
        header_row=0,  # The first row (index 0) is the header row
        item_column=1,  # Column 1 contains item names
        invoice_column=0  # Column 0 contains invoice IDs
    )

def test_get_date_column(worksheet_model: PrepaymentScheduleWorksheetModel):
    """Test getting the correct column for a given date."""
    date_column = worksheet_model.get_date_column(dt.datetime(2024, 5, 1))
    assert date_column == 2  # May 2024 is in column 2 (zero-indexed)

    date_column = worksheet_model.get_date_column(dt.datetime(2024, 6, 1))
    assert date_column == 3  # June 2024 is in column 3 (zero-indexed)

    date_column = worksheet_model.get_date_column(dt.datetime(2023, 5, 1))
    assert date_column is None  # No matching column for this date

def test_get_invoice_id(worksheet_model: PrepaymentScheduleWorksheetModel):
    """Test retrieving the invoice ID."""
    assert worksheet_model.get_invoice_id(1) == "INV001"  # Row 1 (zero-indexed)
    assert worksheet_model.get_invoice_id(2) == "INV002"  # Row 2 (zero-indexed)
    assert worksheet_model.get_invoice_id(3) == "INV003"  # Row 3 (zero-indexed)

def test_get_item(worksheet_model: PrepaymentScheduleWorksheetModel):
    """Test retrieving the item name."""
    assert worksheet_model.get_item(1) == "Webhosting"  # Row 1 (zero-indexed)
    assert worksheet_model.get_item(2) == "Domain"     # Row 2 (zero-indexed)
    assert worksheet_model.get_item(3) == "SSL"        # Row 3 (zero-indexed)

def test_get_amount(worksheet_model: PrepaymentScheduleWorksheetModel):
    """Test retrieving the amount for a specific row and column."""
    assert worksheet_model.get_amount(1, 2) == 833.33  # May 2024, Row 1 (zero-indexed)
    assert worksheet_model.get_amount(2, 2) == 500.00  # May 2024, Row 2 (zero-indexed)
    assert worksheet_model.get_amount(3, 2) is None    # May 2024, Row 3 (zero-indexed, no amount)

def test_list_entry_data_for_month(worksheet_model: PrepaymentScheduleWorksheetModel):
    """Test listing entry data for a specific month."""
    entry_data_list = worksheet_model.list_entry_data_for_month(dt.datetime(2024, 5, 1))
    assert len(entry_data_list) == 2  # Only two rows have amounts for May 2024

    # Validate the first entry
    entry1 = entry_data_list[0]
    assert isinstance(entry1, EntryDataModel)
    assert entry1.date == dt.datetime(2024, 5, 1)
    assert entry1.item == "Webhosting"
    assert entry1.invoice_id == "INV001"
    assert entry1.amount == 833.33

    # Validate the second entry
    entry2 = entry_data_list[1]
    assert isinstance(entry2, EntryDataModel)
    assert entry2.date == dt.datetime(2024, 5, 1)
    assert entry2.item == "Domain"
    assert entry2.invoice_id == "INV002"
    assert entry2.amount == 500.00

    # Test for a month with no entries
    entry_data_list = worksheet_model.list_entry_data_for_month(dt.datetime(2023, 5, 1))
    assert len(entry_data_list) == 0
