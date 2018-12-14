import wx


class NotEmptyValidator(wx.Validator):
    def __init__(self):
        wx.Validator.__init__(self)

    def Clone(self):
        return NotEmptyValidator()

    def Validate(self, parent):
        text_ctrl = self.GetWindow()
        value = text_ctrl.GetValue()

        if not value:
            self._flag_ctrl_as_invalid()
            return False
        else:
            self._flag_ctrl_as_valid()
            return True

    def _flag_ctrl_as_invalid(self):
        text_ctrl = self.GetWindow()
        text_ctrl.SetBackgroundColour(wx.Colour(250, 128, 114))
        text_ctrl.SetFocus()
        text_ctrl.Refresh()

    def _flag_ctrl_as_valid(self):
        text_ctrl = self.GetWindow()
        text_ctrl.SetBackgroundColour(wx.Colour(wx.WHITE))
        text_ctrl.Refresh()

    def TransferFromWindow(self):
        return True

    def TransferToWindow(self):
        return True
