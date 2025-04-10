import openpyxl
import datetime as dt
from typing import Any

from models.worksheet import PrepaymentScheduleWorksheetModel
from models.entry import AccountingEntryModel, EntryDataModel

def sheet_to_2d_list(file_path: str, sheet_name: str, data_only=True) -> list[list[Any]]:
    try:
        workbook = openpyxl.load_workbook(file_path, data_only=data_only)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
    
    sheet = workbook[sheet_name]

    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(list(row))

    return data

def get_accounting_entry(date: dt.date,
    description: str,
    reference: str,
    expense_account: str,
    prepayment_account: str,
    amount: float
) -> tuple[AccountingEntryModel, AccountingEntryModel]:

    debit_entry = AccountingEntryModel(
        date=date,
        description=description,
        reference=reference,
        account=expense_account,
        amount=-amount
    )

    credit_entry = AccountingEntryModel(
        date=date,
        description=description,
        reference=reference,
        account=prepayment_account,
        amount=amount
    )

    return debit_entry, credit_entry

def filter_entries_by_item(entry_data_list: list[EntryDataModel], item_name: str) -> list[EntryDataModel]:
    """Filter entries by item name."""
    return [
        entry for entry in entry_data_list
        if entry.item.strip().lower() == item_name.strip().lower()
    ]

def get_accounting_entries(
    entry_data_list: list[EntryDataModel],
    posting_date: dt.date,
    description_prefix: str,
    expense_account: str,
    prepayment_account: str
) -> list[AccountingEntryModel]:
    """Generate accounting entries from entry data."""
    accounting_entries = []
    for entry in entry_data_list:
        description = f"{description_prefix} {entry.item}"

        debit_entry, credit_entry = get_accounting_entry(
            date=posting_date,
            description=description,
            reference=entry.invoice_id,
            expense_account=expense_account,
            prepayment_account=prepayment_account,
            amount=entry.amount
        )

        accounting_entries.append(debit_entry)
        accounting_entries.append(credit_entry)

    return accounting_entries

def generate_accounting_entries_for_month(
    file_path: str,
    sheet_name: str,
    header_row: int,
    item_column: str,
    invoice_column: str,
    expense_account: str,
    prepayment_account: str,
    target_month: dt.datetime,
    posting_date: dt.date,
    description_prefix: str,
    item_name: str | None = None  # New filter parameter
) -> list[AccountingEntryModel]:

    cells = sheet_to_2d_list(file_path, sheet_name)

    worksheet_model = PrepaymentScheduleWorksheetModel(
        cells=cells,
        header_row=header_row - 1,
        item_column=openpyxl.utils.column_index_from_string(item_column) - 1,
        invoice_column=openpyxl.utils.column_index_from_string(invoice_column) - 1
    )

    entry_data_list = worksheet_model.list_entry_data_for_month(target_month)

    if item_name:
        entry_data_list = filter_entries_by_item(entry_data_list, item_name)

    return get_accounting_entries(
        entry_data_list=entry_data_list,
        posting_date=posting_date,
        description_prefix=description_prefix,
        expense_account=expense_account,
        prepayment_account=prepayment_account
    )
