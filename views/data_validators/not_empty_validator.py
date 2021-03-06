from . import base_validator


class NotEmptyValidator(base_validator.BaseValidator):
    def __init__(self):
        super().__init__()

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
