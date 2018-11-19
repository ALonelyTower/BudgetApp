import wx
import view_menu


class BudgetView(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr):
        # Unnecessary, but prefer to be explicit as it was driving me crazy keeping track.
        super().__init__(parent, id, title, pos, size, style, name)

        self._window_size = wx.Size(1050, 240)
        self.SetMinSize(wx.Size(self._window_size))

        self._init_gui_control_widgets()

        self.Bind(wx.EVT_LIST_INSERT_ITEM, self._increment_window_size, self._transaction_list_view)

        self.Show()

    def _increment_window_size(self, event):
        self._window_size.IncBy(0, 10)
        self.SetSize(self._window_size)

    def _init_gui_control_widgets(self):
        # Methods are positionally dependent.  Reordering them may break things.
        self._panel = wx.Panel(parent=self)

        self._create_transaction_button()
        self._create_transaction_list()
        self._create_panel_sizer()

        self._menu_bar = view_menu.MenuBar(self)
        self.SetMenuBar(self._menu_bar)

    def _create_transaction_button(self):
        add_bitmap_icon = wx.Bitmap("W:\\BudgetApp\\appbar_add.png")
        self._add_transaction_button = wx.BitmapButton(parent=self._panel, id=wx.ID_ANY,
                                                       bitmap=add_bitmap_icon, pos=wx.DefaultPosition,
                                                       size=(75, 75), style=wx.BU_AUTODRAW,
                                                       validator=wx.DefaultValidator, name="Add Transaction")

    def _create_transaction_list(self):
        self._transaction_list_view = wx.ListView(self._panel, style=wx.LC_REPORT)
        self._transaction_list_view.InsertColumn(col=1, heading="Date", format=wx.LIST_FORMAT_CENTER, width=100)
        self._transaction_list_view.InsertColumn(col=2, heading="Category", format=wx.LIST_FORMAT_CENTER, width=200)
        self._transaction_list_view.InsertColumn(col=3, heading="Payment Method", format=wx.LIST_FORMAT_CENTER, width=150)
        self._transaction_list_view.InsertColumn(col=4, heading="Total Expense", format=wx.LIST_FORMAT_CENTER, width=100)
        self._transaction_list_view.InsertColumn(col=5, heading="Description", format=wx.LIST_FORMAT_CENTER, width=375)

    def _create_panel_sizer(self):
        self._grid_bag_sizer = wx.GridBagSizer(vgap=0, hgap=0)

        self._grid_bag_sizer.Add(window=self._add_transaction_button, pos=(0, 0),
                                 flag=wx.TOP | wx.LEFT | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=10)
        self._grid_bag_sizer.Add(window=self._transaction_list_view, pos=(0, 1), flag=wx.EXPAND | wx.ALL, border=10)

        # Must only be set after adding widgets to Sizer.
        self._grid_bag_sizer.AddGrowableRow(0, 0)
        self._grid_bag_sizer.AddGrowableCol(0, 0)
        self._grid_bag_sizer.AddGrowableCol(1, 0)

        self._panel.SetSizer(self._grid_bag_sizer)

    def bind_add_transaction_action(self, button_action):
        self._add_transaction_button.Bind(wx.EVT_BUTTON, button_action)


if __name__ == '__main__':
    app = wx.App()
    budget = BudgetView()
    app.MainLoop()
