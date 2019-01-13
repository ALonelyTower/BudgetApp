import wx
from contextlib import contextmanager


from views.data_validators import date_form_validator as dfv
from views.data_validators import not_empty_validator as nev
from models.data_transfer_object import TransactionDTO, CategoryDTO


class TransactionView(wx.Dialog):
    # TODO: Should eventually use pertinent data types like DateTime and Decimal
    def __init__(self, transaction_id=-1, parent=None, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE, name=wx.DialogNameStr):
        super().__init__(parent, id, title, pos, size=(400, 600), style=style, name=name)

        self._transaction_id = transaction_id

        self._form_sizer = wx.BoxSizer(wx.VERTICAL)
        self._set_flags_and_values()
        self._declare_form_ctrls()
        self._add_form_sections()
        self._install_form_data_validator()
        self._bind_internal_events()
        self.SetSizer(self._form_sizer)

    def _set_flags_and_values(self):
        self._formitem_border = 5
        self._label_flags = wx.TOP | wx.LEFT | wx.RIGHT
        self._textctrl_flags = wx.BOTTOM | wx.LEFT | wx.RIGHT
        self._date_delimiter = '-'
        self._default_categories = ["", "[New Category]"]
        self._new_categories = []

    def _declare_form_ctrls(self):
        self._date_year_textctrl = wx.TextCtrl(self, name="date_year")
        self._date_month_textctrl = wx.TextCtrl(self, name="date_month")
        self._date_day_textctrl = wx.TextCtrl(self, name="date_day")
        self._category_textctrl = wx.ComboBox(parent=self, name="category", style=wx.CB_READONLY,
                                              choices=self._default_categories)
        self._payment_method_textctrl = wx.TextCtrl(self, name="payment_method")
        self._total_expense_textctrl = wx.TextCtrl(self, name="total_expense")
        self._description_textctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL, name="description")

        self._ctrl_list = [self._date_year_textctrl, self._date_month_textctrl, self._date_day_textctrl,
                           self._category_textctrl, self._payment_method_textctrl, self._total_expense_textctrl,
                           self._description_textctrl]
        self._ok_button = wx.Button(self, id=wx.ID_OK, label="&Ok", name="ok_button")
        self._cancel_button = wx.Button(self, id=wx.ID_CANCEL, label="&Cancel", name="cancel_button")

    def _add_form_sections(self):
        self._add_title_section()
        self._add_date_section()
        self._add_category_section()
        self._add_payment_method_sections()
        self._add_expense_section()
        self._add_description_section()
        self._add_ok_cancel_button_section()

    def _install_form_data_validator(self):
        self._date_year_textctrl.SetValidator(dfv.DateFormValidator())
        self._date_month_textctrl.SetValidator(dfv.DateFormValidator())
        self._date_day_textctrl.SetValidator(dfv.DateFormValidator())
        self._category_textctrl.SetValidator(nev.NotEmptyValidator())
        self._payment_method_textctrl.SetValidator(nev.NotEmptyValidator())
        self._total_expense_textctrl.SetValidator(nev.NotEmptyValidator())
        self._description_textctrl.SetValidator(nev.NotEmptyValidator())

    def _add_title_section(self):
        transaction_label = wx.StaticText(self, label="Transaction")
        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        transaction_label.SetFont(font)
        self._form_sizer.Add(transaction_label, flag=wx.TOP | wx.CENTER, border=self._formitem_border)

        static_line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        self._form_sizer.Add(static_line, flag=wx.ALL | wx.EXPAND, border=self._formitem_border)

    def _add_date_section(self):
        date_sizer = wx.FlexGridSizer(rows=2, cols=3, vgap=0, hgap=3)

        date_year_label = wx.StaticText(self, label="Year (YYYY)")
        date_month_label = wx.StaticText(self, label="Month (MM)")
        date_day_label = wx.StaticText(self, label="Day (DD)")

        # Items are added to the widget from left to right, top to bottom.  Order matters.
        date_sizer.AddMany(
            [
                (date_year_label, 0, wx.EXPAND), (date_month_label, 0, wx.EXPAND), (date_day_label, 0, wx.EXPAND),
                (self._date_year_textctrl, 0.50), (self._date_month_textctrl, 0.25), (self._date_day_textctrl, 0.25),
            ]
        )

        self._form_sizer.Add(date_sizer, flag=self._textctrl_flags, border=self._formitem_border)

    def _add_category_section(self):
        category_label = wx.StaticText(self, label="Category")
        self._form_sizer.Add(category_label, flag=self._label_flags, border=self._formitem_border)
        self._form_sizer.Add(self._category_textctrl, flag=wx.EXPAND | self._textctrl_flags, border=self._formitem_border)

    def _add_payment_method_sections(self):
        payment_method_label = wx.StaticText(self, label="Payment Method")
        self._form_sizer.Add(payment_method_label, flag=self._label_flags, border=self._formitem_border)
        self._form_sizer.Add(self._payment_method_textctrl, flag=wx.EXPAND | self._textctrl_flags, border=self._formitem_border)

    def _add_expense_section(self):
        total_expense_label = wx.StaticText(self, label="Total Expense")
        self._form_sizer.Add(total_expense_label, flag=self._label_flags, border=self._formitem_border)
        self._form_sizer.Add(self._total_expense_textctrl, flag=self._textctrl_flags, border=self._formitem_border)

    def _add_description_section(self):
        description_label = wx.StaticText(self, label="Description")
        self._form_sizer.Add(description_label, flag=wx.TOP | wx.LEFT | wx.RIGHT, border=self._formitem_border)
        self._form_sizer.Add(self._description_textctrl, proportion=1, flag=wx.EXPAND | self._textctrl_flags, border=self._formitem_border)

    def _add_ok_cancel_button_section(self):
        """
        Still can't figure out how to properly align the buttons.  The difficulty is the opaque behavior of
        manipulating two sizers within one another.
        """
        button_sizer = wx.StdDialogButtonSizer()
        button_sizer.AddButton(self._ok_button)
        button_sizer.AddButton(self._cancel_button)
        button_sizer.Realize()
        self._form_sizer.Add(button_sizer, flag=wx.ALL | wx.CENTER, border=self._formitem_border)

    def _bind_internal_events(self):
        self._category_textctrl.Bind(wx.EVT_COMBOBOX, self._add_new_category)

    def get_form_values(self):
        category_index = self._category_textctrl.GetSelection()
        return TransactionDTO(
            self._transaction_id,
            self._get_date_value(),
            self._category_textctrl.GetClientData(category_index),
            self._payment_method_textctrl.GetValue(),
            self._total_expense_textctrl.GetValue(),
            self._description_textctrl.GetValue()
        )

    def _get_date_value(self):
        year = self._date_year_textctrl.GetValue()
        month = self._date_month_textctrl.GetValue()
        day = self._date_day_textctrl.GetValue()
        delimiter = self._date_delimiter
        return f"{year}{delimiter}{month}{delimiter}{day}"

    def set_form_values(self, transaction_record):
        self._transaction_id = transaction_record.id
        year, month, day = self._split_date(transaction_record.date)
        self._date_year_textctrl.SetValue(year)
        self._date_month_textctrl.SetValue(month)
        self._date_day_textctrl.SetValue(day)
        self._category_textctrl.SetValue(transaction_record.category.name)
        self._payment_method_textctrl.SetValue(transaction_record.payment_method)
        self._total_expense_textctrl.SetValue(f"{transaction_record.total_expense}")
        self._description_textctrl.SetValue(transaction_record.description)

    def _split_date(self, date_string):
        return date_string.split(self._date_delimiter)

    def get_new_categories(self):
        return self._new_categories

    def set_categories(self, categories):
        for category in categories:
            self._category_textctrl.Append(category.name, category)

    def _add_new_category(self, event):
        selected_value = self._category_textctrl.GetValue()
        if selected_value == "[New Category]":
            dlg = wx.TextEntryDialog(parent=self, message="Enter new category name:")
            if dlg.ShowModal() == wx.ID_OK:
                category_name = dlg.GetValue()
                new_category = CategoryDTO.new(category_name)
                self._category_textctrl.Append(new_category.name, new_category)
                self._category_textctrl.SetValue(new_category.name)
                self._new_categories.append(new_category)

    def display_readonly_form(self):
        with self._temporarily_disable_form():
            self.ShowModal()
            self.Destroy()
        self._clear_form_values()

    def _clear_form_values(self):
        for ctrl in self._ctrl_list:
            ctrl.Clear()

    def did_user_confirm_deletion(self):
        result = False

        with self._temporarily_disable_form():
            if self.display_editable_form():
                result = self._ask_user_for_final_delete_confirmation()

        return result

    def display_editable_form(self):
        return self.ShowModal() == wx.ID_OK

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


if __name__ == '__main__':
    app = wx.App()
    trans_view = TransactionView()
    trans_view.display_readonly_form()
    app.MainLoop()
