import wx


class CategoryWindow(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=(300, 400),
                 style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr):
        super().__init__(parent, id, title, pos, size, style, name)
        self._panel = wx.Panel(self)
        self._panel_sizer = wx.BoxSizer(orient=wx.VERTICAL)

        self._category_list_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self._category_button_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self._category_confirm_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._category_list_window = wx.ListView(self._panel)
        self._category_list_sizer.Add(self._category_list_window, flag=wx.EXPAND)

        self._add_category_button = wx.Button(self._panel, label="Add", name="add_category")
        self._category_button_sizer.Add(self._add_category_button)

        self._edit_category_button = wx.Button(self._panel, label="Edit", name="edit_category")
        self._category_button_sizer.Add(self._edit_category_button, flag=wx.LEFT, border=5)

        self._delete_category_button = wx.Button(self._panel, label="Delete", name="delete_category")
        self._category_button_sizer.Add(self._delete_category_button, flag=wx.LEFT, border=5)

        self._ok_button = wx.Button(self._panel, id=wx.ID_OK, label="&Ok", name="ok_button")
        self._category_confirm_sizer.Add(self._ok_button)

        self._cancel_button = wx.Button(self._panel, id=wx.ID_CANCEL, label="&Cancel", name="cancel_button")
        self._category_confirm_sizer.Add(self._cancel_button, flag=wx.LEFT, border=5)

        self._panel_sizer.Add(self._category_list_sizer, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self._panel_sizer.Add(self._category_button_sizer, proportion=0, flag=wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=5)
        self._panel_sizer.Add(self._category_confirm_sizer, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=5)

        self._panel.SetSizer(self._panel_sizer)


if __name__ == '__main__':
    app = wx.App()
    cat = CategoryWindow()
    cat.Show()
    app.MainLoop()
