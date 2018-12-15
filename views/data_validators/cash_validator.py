from . import base_validator


class CashValidator(base_validator.BaseValidator):
    def __init__(self):
        super().__init__()

    def Clone(self):
        return CashValidator()

    def Validate(self, parent):
        text_ctrl = self.GetWindow()
        value = text_ctrl.GetValue()

        if not value and not value.isnumeric():
            self._flag_ctrl_as_invalid()
            return False
        else:
            self._flag_ctrl_as_valid()
            return True
