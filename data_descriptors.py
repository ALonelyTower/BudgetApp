

class DateDescriptor:
    def __init__(self, date):
        self.date = date

    def __get__(self):
        return self.date

    def __set__(self, date):
        self.date = date

    def __eq__(self, other):
        return self.date == other.date


class CashDescriptor:
    def __init__(self, cash):
        self.cash = cash

    def __get__(self):
        return self.cash

    def __set__(self, cash):
        self.cash = cash

    def __eq__(self, other):
        return self.cash == other.cash


class TextDescriptor:
    def __init__(self, text):
        self.text = text

    def __get__(self):
        return self.text

    def __set__(self, text):
        self.text = text

    def __eq__(self, other):
        return self.text
