from views.view_transaction import TransactionView


class MockTransactionView(TransactionView):
    def __init__(self, title):
        super().__init__(title=title)

    @property
    def date_year_textctrl(self):
        return self._date_year_textctrl.GetValue()

    @date_year_textctrl.setter
    def date_year_textctrl(self, value):
        self._date_year_textctrl.SetValue(value)

    @property
    def date_month_textctrl(self):
        return self._date_month_textctrl.GetValue()

    @date_month_textctrl.setter
    def date_month_textctrl(self, value):
        self._date_month_textctrl.SetValue(value)

    @property
    def date_day_textctrl(self):
        return self._date_day_textctrl.GetValue()

    @date_day_textctrl.setter
    def date_day_textctrl(self, value):
        self._date_day_textctrl.SetValue(value)

    @property
    def category_textctrl(self):
        return self._category_textctrl

    @property
    def payment_method_textctrl(self):
        return self._payment_method_textctrl.GetValue()

    @payment_method_textctrl.setter
    def payment_method_textctrl(self, value):
        self._payment_method_textctrl.SetValue(value)

    @property
    def total_expense_textctrl(self):
        return self._total_expense_textctrl.GetValue()

    @total_expense_textctrl.setter
    def total_expense_textctrl(self, value):
        self._total_expense_textctrl.SetValue(value)

    @property
    def description_textctrl(self):
        return self._description_textctrl.GetValue()

    @description_textctrl.setter
    def description_textctrl(self, value):
        self._description_textctrl.SetValue(value)

    def ok_button(self):
        return self._ok_button
