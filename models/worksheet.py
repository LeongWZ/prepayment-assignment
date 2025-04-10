import datetime as dt
from typing import Any

from .entry import EntryDataModel

class WorksheetModel:
    def __init__(self, cells: list[list[Any]]):
        self.__cells = cells

    def get_cell_value(self, row: int, column: int) -> Any:
        """Get the amount from the specified column."""
        if not self.is_valid_row(row) or not self.is_valid_column(column):
            raise ValueError("Invalid row or column index")

        return self.__cells[row][column]

    def is_valid_row(self, row: int) -> bool:
        """Check if the row is valid based on the header row."""
        return row >= 0 and row < len(self.__cells)
    
    def is_valid_column(self, column: int) -> bool:
        return column >= 0 and column < len(self.__cells[0]) if self.__cells else False
    
    def get_row_count(self) -> int:
        """Get the number of rows in the worksheet."""
        return len(self.__cells)
    
    def get_column_count(self) -> int:
        """Get the number of columns in the worksheet."""
        return len(self.__cells[0]) if self.__cells else 0


class PrepaymentScheduleWorksheetModel(WorksheetModel):
    def __init__(self, cells: list[list[Any]], header_row: int, item_column: int, invoice_column: int):
        super().__init__(cells)
        self.header_row = header_row
        self.item_column = item_column
        self.invoice_column = invoice_column

    def get_date_column(self, date: dt.date) -> int | None:
        """Get the column for the given month and year."""
        # Iterate through the columns in the header row
        for column in range(self.get_column_count()):
            cell = self.get_cell_value(self.header_row, column)
            if not isinstance(cell, dt.datetime):
                continue

            if cell.month == date.month and cell.year == date.year:
                return column
        
        # Return None if no match is found
        return None
    
    def get_invoice_id(self, row: int) -> str:
        """Get the invoice number from the specified column."""
        value = self.get_cell_value(row, self.invoice_column)
        
        return str(value)

    def get_item(self, row: int) -> str:
        """Get the item from the specified column."""
        value = self.get_cell_value(row, self.item_column)
        
        if not isinstance(value, str):
            return ""
        
        return value
    
    def get_amount(self, row: int, column: int) -> float | None:
        """Get the amount from the specified column."""
        value = self.get_cell_value(row, column)

        if value is None or not isinstance(value, (int, float)):
            return None

        return float(value)
    
    def list_entry_data_for_month(self, month: dt.datetime) -> list[EntryDataModel]:
        """Get the entry data for the specified month."""
        entry_data_list = []
        date_column = self.get_date_column(month)

        if not date_column:
            return entry_data_list
        
        # Iterate through the rows to find entries
        for row in range(self.header_row + 1, self.get_row_count()):
            invoice_number = self.get_invoice_id(row)
            item = self.get_item(row)
            amount = self.get_amount(row, date_column)

            if amount is None:
                continue

            entry_data = EntryDataModel(
                date=month,
                item=item,
                invoice_id=invoice_number,
                amount = amount
            )

            entry_data_list.append(entry_data)
        
        return entry_data_list
