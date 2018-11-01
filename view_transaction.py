import wx


class TransactionView(wx.Dialog):
    def __init__(self):
        super().__init__(None, size=(400, 600))
        wx.Panel().__init__(self)
        self.form_sizer = wx.BoxSizer(wx.VERTICAL)
        self.form_item_border = 5

        self._add_form_title()
        self._add_date_controls()
        self._add_category_controls()
        self._add_payment_method_controls()
        self._add_expense_controls()
        self._add_description_controls()
        self._add_ok_cancel_button_controls()

        self.SetSizer(self.form_sizer)

    def _add_form_title(self):
        transaction_label = wx.StaticText(self, label="Transaction")
        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        transaction_label.SetFont(font)
        self.form_sizer.Add(transaction_label, flag=wx.TOP | wx.CENTER, border=self.form_item_border)

        static_line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        self.form_sizer.Add(static_line, flag=wx.ALL | wx.EXPAND, border=self.form_item_border)

    def _add_date_controls(self):
        date_label = wx.StaticText(self, label="YYYY/MM/DD")
        self.form_sizer.Add(date_label, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=self.form_item_border)

        date_textcontrol = wx.TextCtrl(self)
        self.form_sizer.Add(date_textcontrol, flag=wx.BOTTOM | wx.LEFT | wx.RIGHT, border=self.form_item_border)

    def _add_category_controls(self):
        category_label = wx.StaticText(self, label="Category")
        self.form_sizer.Add(category_label, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=self.form_item_border)

        category_textcontrol = wx.TextCtrl(self)
        self.form_sizer.Add(category_textcontrol, flag=wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=self.form_item_border)

    def _add_payment_method_controls(self):
        payment_method_label = wx.StaticText(self, label="Payment Method")
        self.form_sizer.Add(payment_method_label, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=self.form_item_border)

        payment_textcontrol = wx.TextCtrl(self)
        self.form_sizer.Add(payment_textcontrol, flag=wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=self.form_item_border)

    def _add_expense_controls(self):
        total_expense_label = wx.StaticText(self, label="Total Expense")
        self.form_sizer.Add(total_expense_label, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=self.form_item_border)

        total_expense_textcontrol = wx.TextCtrl(self)
        self.form_sizer.Add(total_expense_textcontrol, flag=wx.BOTTOM | wx.LEFT | wx.RIGHT, border=self.form_item_border)

    def _add_description_controls(self):
        description_label = wx.StaticText(self, label="Description")
        self.form_sizer.Add(description_label, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=self.form_item_border)

        description_textcontrol = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)
        self.form_sizer.Add(description_textcontrol, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=self.form_item_border)

    def _add_ok_cancel_button_controls(self):
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        ok_button = wx.Button(self, label="Ok")
        button_sizer.Add(ok_button, proportion=0, flag=wx.EXPAND | wx.ALL)

        cancel_button = wx.Button(self, label="Cancel")
        button_sizer.Add(cancel_button, proportion=0, flag=wx.EXPAND | wx.ALL)

        self.form_sizer.Add(button_sizer, flag=wx.ALL | wx.CENTER, border=self.form_item_border)


if __name__ == '__main__':
    app = wx.App()
    transView = TransactionView()
    transView.ShowModal()
    app.MainLoop()
