import wx


class CategoryWindow(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=(300, 400),
                 style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr):
        super().__init__(parent, id, title, pos, size, style, name)
        self._panel = wx.Panel(self)

        self._create_frame_sizers()

        self._create_category_list_ctrl()
        self._create_category_buttons()
        self._create_form_buttons()

        self._add_sizers_to_parent_sizer()

        self._panel.SetSizer(self._panel_sizer)

    def _create_frame_sizers(self):
        self._panel_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self._category_list_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self._category_button_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self._form_button_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)

    def _create_category_list_ctrl(self):
        self._category_textctrl = wx.ListView(self._panel, style=wx.LC_REPORT)
        self._category_textctrl.InsertColumn(col=0, heading="#", format=wx.LIST_FORMAT_CENTER, width=50)
        self._category_textctrl.InsertColumn(col=1, heading="Category", format=wx.LIST_FORMAT_CENTER, width=200)
        self._category_list_sizer.Add(self._category_textctrl, flag=wx.EXPAND)

    def _create_category_buttons(self):
        self._add_category_button = wx.Button(self._panel, label="Add", name="add_category")
        self._category_button_sizer.Add(self._add_category_button)

        self._edit_category_button = wx.Button(self._panel, label="Edit", name="edit_category")
        self._category_button_sizer.Add(self._edit_category_button, flag=wx.LEFT, border=5)

        self._delete_category_button = wx.Button(self._panel, label="Delete", name="delete_category")
        self._category_button_sizer.Add(self._delete_category_button, flag=wx.LEFT, border=5)

    def _create_form_buttons(self):
        self._ok_button = wx.Button(self._panel, id=wx.ID_OK, label="&Ok", name="ok_button")
        self._form_button_sizer.Add(self._ok_button)

        self._cancel_button = wx.Button(self._panel, id=wx.ID_CANCEL, label="&Cancel", name="cancel_button")
        self._form_button_sizer.Add(self._cancel_button, flag=wx.LEFT, border=5)

    def _add_sizers_to_parent_sizer(self):
        self._panel_sizer.Add(self._category_list_sizer, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=5)
        self._panel_sizer.Add(self._category_button_sizer, proportion=0, flag=wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=5)
        self._panel_sizer.Add(self._form_button_sizer, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=5)

    def set_categories(self, categories):
        categories = [category for category in categories if category.name != 'No Category']
        for (index, category) in enumerate(categories):
            list_item = wx.ListItem()
            list_item.SetId(index)
            list_item.SetData(category.id)
            list_item.SetText(f"{index + 1}")
            list_item_index = self._category_textctrl.InsertItem(list_item)
            self._category_textctrl.SetItem(list_item_index, 1, category.name)


if __name__ == '__main__':
    app = wx.App()
    cat = CategoryWindow()
    cat.Show()
    app.MainLoop()
