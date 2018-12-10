import wx
from contextlib import contextmanager


class TransactionView(wx.Dialog):
    # TODO: Experiment with GridBagSizer - it might give better positioning control
    # TODO: Should eventually use pertinent data types like DateTime and Decimal
    # TODO: Should eventually use Data Transfer Object to codify expected Data Structure
    def __init__(self, parent=None, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_DIALOG_STYLE, name=wx.DialogNameStr):
        super().__init__(parent, id, title, pos, size=(400, 600), style=style, name=name)

        self._set_flags_and_sizers()
        self._declare_widget_ctrls()
        self._add_ctrls_to_sizer()
        self.SetSizer(self._form_sizer)

    def _set_flags_and_sizers(self):
        self._formitem_border = 5
        self._label_flags = wx.TOP | wx.LEFT | wx.RIGHT
        self._textctrl_flags = wx.BOTTOM | wx.LEFT | wx.RIGHT
        self._ctrls_enabled = True

    def _declare_widget_ctrls(self):
        self._date_textctrl = wx.TextCtrl(self)
        self._category_textctrl = wx.TextCtrl(self)
        self._payment_method_textctrl = wx.TextCtrl(self)
        self._total_expense_textctrl = wx.TextCtrl(self)
        self._description_textctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)

        self._ctrl_list = [self._date_textctrl, self._category_textctrl, self._payment_method_textctrl,
                           self._total_expense_textctrl, self._description_textctrl]
        self._ok_button = wx.Button(self, id=wx.ID_OK, label="&Ok")
        self._cancel_button = wx.Button(self, id=wx.ID_CANCEL, label="&Cancel")

    def _add_ctrls_to_sizer(self):
        self._form_sizer = wx.BoxSizer(wx.VERTICAL)
        self._add_form_title()
        self._add_date_controls()
        self._add_category_controls()
        self._add_payment_method_controls()
        self._add_expense_controls()
        self._add_description_controls()
        self._add_ok_cancel_button_controls()

    def bind_ok_button(self, button_action):
        self._ok_button.Bind(wx.EVT_BUTTON, button_action)

    def get_form_values(self):
        return {
            'primary_key': None,
            'date': self._date_textctrl.GetValue(),
            'category': self._category_textctrl.GetValue(),
            'payment_method': self._payment_method_textctrl.GetValue(),
            'total_expense': self._total_expense_textctrl.GetValue(),
            'description': self._description_textctrl.GetValue()
        }

    def set_form_values(self, transaction_data):
        self._date_textctrl.SetValue(transaction_data['date'])
        self._category_textctrl.SetValue(transaction_data['category'])
        self._payment_method_textctrl.SetValue(transaction_data['payment_method'])
        self._total_expense_textctrl.SetValue(str(transaction_data['total_expense']))
        self._description_textctrl.SetValue(transaction_data['description'])

    def display_view_form(self):
        with self._temporarily_disable_form():
            self.ShowModal()
        self._clear_form_values()

    def _clear_form_values(self):
        for ctrl in self._ctrl_list:
            ctrl.Clear()

    def did_user_approve_transaction(self):
        return self.ShowModal() == wx.ID_OK

    def did_user_confirm_deletion(self):
        result = False

        with self._temporarily_disable_form():
            if self.did_user_approve_transaction():
                result = self._ask_user_for_final_delete_confirmation()

        return result

    @contextmanager
    def _temporarily_disable_form(self):
        try:
            for ctrl in self._ctrl_list:
                ctrl.Disable()
            yield None
        finally:
            for ctrl in self._ctrl_list:
                ctrl.Enable()

    def _ask_user_for_final_delete_confirmation(self):
        with self._delete_warning_popup() as dialog_popup:
            user_confirmation = dialog_popup.ShowModal()

        return True if user_confirmation == wx.ID_OK else False

    def _delete_warning_popup(self):
        return wx.MessageDialog(parent=self, message="Are you sure you want to delete this Transaction?",
                                caption="Confirm Deletion", style=wx.OK | wx.CANCEL)

    def _add_form_title(self):
        transaction_label = wx.StaticText(self, label="Transaction")
        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        transaction_label.SetFont(font)
        self._form_sizer.Add(transaction_label, flag=wx.TOP | wx.CENTER, border=self._formitem_border)

        static_line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        self._form_sizer.Add(static_line, flag=wx.ALL | wx.EXPAND, border=self._formitem_border)

    def _add_date_controls(self):
        date_label = wx.StaticText(self, label="YYYY/MM/DD")
        self._form_sizer.Add(date_label, flag=self._label_flags, border=self._formitem_border)
        self._form_sizer.Add(self._date_textctrl, flag=self._textctrl_flags, border=self._formitem_border)

    def _add_category_controls(self):
        category_label = wx.StaticText(self, label="Category")
        self._form_sizer.Add(category_label, flag=self._label_flags, border=self._formitem_border)
        self._form_sizer.Add(self._category_textctrl, flag=wx.EXPAND | self._textctrl_flags, border=self._formitem_border)

    def _add_payment_method_controls(self):
        payment_method_label = wx.StaticText(self, label="Payment Method")
        self._form_sizer.Add(payment_method_label, flag=self._label_flags, border=self._formitem_border)
        self._form_sizer.Add(self._payment_method_textctrl, flag=wx.EXPAND | self._textctrl_flags, border=self._formitem_border)

    def _add_expense_controls(self):
        total_expense_label = wx.StaticText(self, label="Total Expense")
        self._form_sizer.Add(total_expense_label, flag=self._label_flags, border=self._formitem_border)
        self._form_sizer.Add(self._total_expense_textctrl, flag=self._textctrl_flags, border=self._formitem_border)

    def _add_description_controls(self):
        description_label = wx.StaticText(self, label="Description")
        self._form_sizer.Add(description_label, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=self._formitem_border)
        self._form_sizer.Add(self._description_textctrl, proportion=1, flag=wx.EXPAND | self._textctrl_flags, border=self._formitem_border)

    def _add_ok_cancel_button_controls(self):
        """
        Still can't figure out how to properly align the buttons.  The difficulty is the opaque behavior of
        manipulating two sizers within one another.
        """
        button_sizer = wx.StdDialogButtonSizer()
        button_sizer.AddButton(self._ok_button)
        button_sizer.AddButton(self._cancel_button)
        button_sizer.Realize()
        self._form_sizer.Add(button_sizer, flag=wx.ALL | wx.CENTER, border=self._formitem_border)


if __name__ == '__main__':
    app = wx.App()
    view = TransactionView()
    view.display_view_form()
    app.MainLoop()

