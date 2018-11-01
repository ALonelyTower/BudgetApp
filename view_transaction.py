import wx
import view_menu


class TransactionView(wx.Dialog):
    def __init__(self):
        super().__init__(None, size=(400, 600))
        panel = wx.Panel(self)
        transaction_sizer = wx.BoxSizer(wx.VERTICAL)
        transaction_border = 10

        transaction_label = wx.StaticText(self, label="Transaction")
        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        transaction_label.SetFont(font)
        transaction_sizer.Add(transaction_label, flag=wx.TOP | wx.CENTER, border=transaction_border)

        static_line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        transaction_sizer.Add(static_line, flag=wx.ALL | wx.EXPAND, border=transaction_border)

        date_label = wx.StaticText(self, label="YYYY/MM/DD")
        date_textcontrol = wx.TextCtrl(self)
        transaction_sizer.Add(date_label, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=transaction_border)
        transaction_sizer.Add(date_textcontrol, flag=wx.BOTTOM | wx.LEFT | wx.RIGHT, border=transaction_border)

        category_label = wx.StaticText(self, label="Category")
        category_textcontrol = wx.TextCtrl(self)
        transaction_sizer.Add(category_label, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=transaction_border)
        transaction_sizer.Add(category_textcontrol, flag=wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=transaction_border)

        payment_method_label = wx.StaticText(self, label="Payment Method")
        payment_textcontrol = wx.TextCtrl(self)
        transaction_sizer.Add(payment_method_label, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=transaction_border)
        transaction_sizer.Add(payment_textcontrol, flag=wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=transaction_border)

        total_expense_label = wx.StaticText(self, label="Total Expense")
        total_expense_textcontrol = wx.TextCtrl(self)
        transaction_sizer.Add(total_expense_label, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=transaction_border)
        transaction_sizer.Add(total_expense_textcontrol, flag=wx.BOTTOM | wx.LEFT | wx.RIGHT, border=transaction_border)

        description_label = wx.StaticText(self, label="Description")
        description_textcontrol = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)
        transaction_sizer.Add(description_label, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=transaction_border)
        transaction_sizer.Add(description_textcontrol, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=transaction_border)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, label="Ok")
        cancel_button = wx.Button(self, label="Cancel")
        button_sizer.Add(ok_button, proportion=0, flag=wx.EXPAND | wx.ALL)
        button_sizer.Add(cancel_button, proportion=0, flag=wx.EXPAND | wx.ALL)
        transaction_sizer.Add(button_sizer, flag=wx.ALL | wx.CENTER, border=transaction_border)

        self.SetSizer(transaction_sizer)


if __name__ == '__main__':
    app = wx.App()
    transView = TransactionView()
    transView.ShowModal()
    app.MainLoop()
