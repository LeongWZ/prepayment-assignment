import subprocess

# Define the parameters
params = [
    "Prepayment assignment.xlsx",  # file_path
    "Schedule",                    # sheet_name
    "3",                           # header_row
    "A",                           # item_column
    "B",                           # invoice_column
    "EXP001",                      # expense_account
    "PRE001",                      # prepayment_account
    "2024-05",                     # target_month
    "--posting-date", "2024-05-31",
    "--description-prefix", "Prepayment amortisation for",
    "--item-name", "Insurance"
]

# Run shell.py with the parameters
subprocess.run(["python", "shell.py"] + params)
