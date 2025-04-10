# Prepayment Accounting Entry Automation

This project automates the generation of accounting entries for prepaid items based on a prepayment schedule stored in an Excel file. The script processes the schedule and generates the necessary accounting entries for a specified month.

## Features
- Automatically generates debit and credit accounting entries for prepaid items.
- Supports filtering by item name.
- Allows customization of posting dates and description prefixes.
- Accepts arguments via the command line for flexibility and ease of use.

## Requirements
- Python 3.10 or higher
- `openpyxl` library (install using `pip install openpyxl`)
- `pytest` library (for unit testing)

## Installation
1. Clone this repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
The main script to run is `shell.py`. It accepts the following arguments:

### Required Arguments
- `file_path`: Path to the Excel file containing the prepayment schedule.
- `sheet_name`: Name of the sheet in the Excel file.
- `header_row`: Row number of the header in the Excel sheet.
- `item_column`: Column letter where item descriptions are stored.
- `invoice_column`: Column letter where invoice numbers are stored.
- `expense_account`: Expense account code for the entries.
- `prepayment_account`: Prepayment account code for the entries.
- `target_month`: Target month in the format `YYYY-MM`.

### Optional Arguments
- `--posting-date`: Date for the accounting entries in the format `YYYY-MM-DD`. Defaults to the last day of the target month.
- `--description-prefix`: Prefix for the description of the accounting entries. Defaults to `"Prepayment amortisation for"`.
- `--item-name`: Filter entries by a specific item name.

### Example Command
```bash
python shell.py "Prepayment assignment.xlsx" "Schedule" 3 "A" "B" "EXP001" "PRE001" "2024-05" --posting-date "2024-05-31" --description-prefix "Prepayment amortisation for" --item-name "Webhosting"
```

### Example Output
```
Date       | Description                          | Reference | Account | Amount
2024-05-31 | Prepayment amortisation for Webhosting | 46248    | EXP001  | 833.33
2024-05-31 | Prepayment amortisation for Webhosting | 46248    | PRE001  | -833.33
```

## Example Script
You can also use the `example_script.py` file to run the script programmatically. It defines the parameters and runs the `shell.py` script using `subprocess`.

### Example Code
```python
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
    "--item-name", "Webhosting"
]

# Run shell.py with the parameters
subprocess.run(["python", "shell.py"] + params)
```

### Running the Example Script
Run the example script using:
```bash
python example_script.py
```

## Testing
This project includes unit tests to ensure the correctness of its functionality. The tests are written using the `pytest` framework.

### Running Tests
To run all tests, execute the following command in the root directory of the project:
```bash
pytest
```

### Running Specific Tests
To run a specific test file, use:
```bash
pytest tests/test_core.py
```

To run a specific test function, use:
```bash
pytest tests/test_core.py::test_get_accounting_entry
```

## File Structure
- `shell.py`: Main script to run the automation.
- `core.py`: Contains core logic for generating accounting entries.
- `models/entry.py`: Defines data models for entries.
- `models/worksheet.py`: Handles worksheet-related operations.
- `tests/`: Contains unit tests for the project.
- `Prepayment assignment.xlsx`: Example Excel file containing the prepayment schedule.

## License
This project is licensed under the MIT License.