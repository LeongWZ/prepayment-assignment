import datetime as dt

class EntryDataModel:
    def __init__(self, date: dt.date, item: str, invoice_id: str, amount: float):
        self.date = date
        self.item = item
        self.invoice_id = invoice_id
        self.amount = amount


class AccountingEntryModel:
    def __init__(self, date: dt.date, description: str, reference: str, account: str, amount: float):
        self.date = date
        self.description = description
        self.reference = reference
        self.account = account
        self.amount = amount
