import wx
import datetime


class DateFormValidator(wx.Validator):
    def __init__(self):
        wx.Validator.__init__(self)
        self._upper_year_limit = datetime.datetime.now().year
        self._lower_year_limit = 1900
        self._upper_month_limit = 12
        self._lower_month_limit = 1
        self._upper_day_limit = 31
        self._lower_day_limit = 1

    def Clone(self):
        return DateFormValidator()

    def Validate(self, window):
        text_ctrl = self.GetWindow()
        value = text_ctrl.GetValue()
        date_typename = text_ctrl.GetName()

        if not value or not value.isnumeric():
            self._flag_ctrl_as_invalid()
            return False
        else:
            num_value = int(value)
            if date_typename == 'date_year':
                self._validate(num_value, self._upper_year_limit, self._lower_year_limit)
            elif date_typename == 'date_month':
                self._validate(num_value, self._upper_month_limit, self._lower_month_limit)
            elif date_typename == 'date_day':
                self._validate(num_value, self._upper_day_limit, self._lower_day_limit)
            else:
                raise ValueError("Attempted to Validate unknown Date Type.")

        self._flag_ctrl_as_valid()
        return True

    def _validate(self, value, upper_limit, lower_limit):
        if value < lower_limit or value > upper_limit:
            self._flag_ctrl_as_invalid()
            return False

    def _flag_ctrl_as_invalid(self):
        text_ctrl = self.GetWindow()
        text_ctrl.SetBackgroundColour(wx.Colour(250, 128, 114))
        text_ctrl.SetFocus()
        text_ctrl.Refresh()

    def _flag_ctrl_as_valid(self):
        text_ctrl = self.GetWindow()
        text_ctrl.SetBackgroundColour(wx.Colour(wx.WHITE))
        text_ctrl.Refresh()

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True
