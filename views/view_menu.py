import wx


class MenuBar(wx.MenuBar):
    def __init__(self, parent, style=0):
        super().__init__(style=style)
        self.parent = parent

        file_menu = wx.Menu(title="", style=0)
        quit_menu_item = wx.MenuItem(parentMenu=file_menu, id=wx.ID_EXIT, text="Q&uit\tCtrl+Q", helpString="Quit Application")
        file_menu.Append(menuItem=quit_menu_item)
        file_menu.Bind(wx.EVT_MENU, self.on_quit, quit_menu_item)

        category_menu = wx.Menu(title="", style=0)
        self._category_menu_item = wx.MenuItem(parentMenu=category_menu, id=wx.ID_ANY, text="Edit Categories...")
        category_menu.Append(menuItem=self._category_menu_item)

        self.Append(file_menu, "&File")
        self.Append(category_menu, "&Category")

    def on_quit(self, event):
        self.parent.Close()

    def bind_categories_context_button(self, button_action, ):
        self.Bind(wx.EVT_MENU, button_action, self._category_menu_item)


class ContextMenu(wx.Menu):
    def __init__(self, parent=None, title="", style=0):
        super().__init__(title=title, style=style)
        self._parent = parent

        self._view_menu_item = wx.MenuItem(parentMenu=self, id=wx.NewId(), text='View Transaction')
        self._edit_menu_item = wx.MenuItem(parentMenu=self, id=wx.NewId(), text='Edit Transaction')
        self._delete_menu_item = wx.MenuItem(parentMenu=self, id=wx.NewId(), text='Delete Transaction')

        self.Append(self._view_menu_item)
        self.Append(self._edit_menu_item)
        self.Append(self._delete_menu_item)

    def bind_edit_menu_item(self, button_action):
        self._bind_action(button_action, self._edit_menu_item)

    def bind_view_menu_item(self, button_action):
        self._bind_action(button_action, self._view_menu_item)

    def bind_delete_menu_item(self, button_action):
        self._bind_action(button_action, self._delete_menu_item)

    def _bind_action(self, button_action, menu_item):
        self.Bind(wx.EVT_MENU, button_action, menu_item)


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, title="Simple App")
    frame.SetMenuBar(MenuBar(parent=frame))
    frame.Show()
    app.MainLoop()
