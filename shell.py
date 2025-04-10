import argparse
import datetime as dt

from core import generate_accounting_entries_for_month


def main():
    parser = argparse.ArgumentParser(description="Generate accounting entries for a given month.")
    parser.add_argument("file_path", type=str, help="Path to the Excel file.")
    parser.add_argument("sheet_name", type=str, help="Name of the sheet.")
    parser.add_argument("header_row", type=int, help="Header row number.")
    parser.add_argument("item_column", type=str, help="Column letter for item descriptions.")
    parser.add_argument("invoice_column", type=str, help="Column letter for invoice numbers.")
    parser.add_argument("expense_account", type=str, help="Expense account code.")
    parser.add_argument("prepayment_account", type=str, help="Prepayment account code.")
    parser.add_argument("target_month", type=str, help="Target month (YYYY-MM).")
    parser.add_argument("--posting-date", type=str, default=None, help="Date for the accounting entries (YYYY-MM-DD).")
    parser.add_argument("--description-prefix", type=str, default="Prepayment amortisation for", help="Prefix for the description.")
    parser.add_argument("--item-name", type=str, help="Only include entries matching this item name.")

    args = parser.parse_args()

    try:
        target_month = dt.datetime.strptime(args.target_month, "%Y-%m")
    except ValueError:
        print("Invalid target month format. Use YYYY-MM.")
        return

    if args.posting_date:
        try:
            posting_date = dt.datetime.strptime(args.posting_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid posting date format. Use YYYY-MM-DD.")
            return
    else:
        # Default: use the last day of the target month
        next_month = target_month.replace(day=28) + dt.timedelta(days=4)
        posting_date = (next_month - dt.timedelta(days=next_month.day)).date()

    entries = generate_accounting_entries_for_month(
        file_path=args.file_path,
        sheet_name=args.sheet_name,
        header_row=args.header_row,
        item_column=args.item_column,
        invoice_column=args.invoice_column,
        expense_account=args.expense_account,
        prepayment_account=args.prepayment_account,
        target_month=target_month,
        posting_date=posting_date,
        description_prefix=args.description_prefix,
        item_name=args.item_name
    )

    for entry in entries:
        print(f"{entry.date.strftime('%Y-%m-%d')} | {entry.description} | {entry.reference} | {entry.account} | {entry.amount:.2f}")


if __name__ == "__main__":
    main()
