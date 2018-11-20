import wx
import view_menu
import collections


class BudgetView(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr):
        # Unnecessary, but prefer to be explicit as it was driving me crazy keeping track.
        super().__init__(parent, id, title, pos, size, style, name)

        self._window_size = wx.Size(1050, 240)
        self.SetMinSize(wx.Size(self._window_size))

        self._init_gui_control_widgets()

        self.Bind(wx.EVT_LIST_INSERT_ITEM, self._increment_window_size, self._transaction_list_view)
        self._transaction_list_view.Bind(wx.EVT_RIGHT_DOWN, self._on_right_click)

        self.Show()

    def _increment_window_size(self, event):
        self._window_size.IncBy(0, 15)
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

    def _on_right_click(self, event):
        off_flag = 0
        num_of_entries = self._transaction_list_view.GetItemCount()
        for index in range(num_of_entries):
            self._transaction_list_view.Select(index, on=off_flag)
        point = event.GetPosition()
        index, hit_flag = self._transaction_list_view.HitTest(point)

        if hit_flag is wx.LIST_HITTEST_ABOVE | wx.LIST_HITTEST_ONITEMLABEL:
            self._transaction_list_view.Select(index)
            self._transaction_list_view.Focus(index)
            menu_position = wx.Point(point.x + 95, point.y + 11)
            self.PopupMenu(view_menu.ContextMenu(self._transaction_list_view), menu_position)

    def set_transaction_list(self, transaction_list):
        for index, trans in enumerate(transaction_list):
            # trans_tup = trans.get_tuple()
            list_item = wx.ListItem()
            list_item.SetId(index)
            list_item.SetText(trans[0])
            index = self._transaction_list_view.InsertItem(list_item)
            self._transaction_list_view.SetItem(index, 1, trans[1])
            self._transaction_list_view.SetItem(index, 2, trans[2])
            self._transaction_list_view.SetItem(index, 3, str(trans[3]))
            self._transaction_list_view.SetItem(index, 4, trans[4])

    def bind_add_transaction_action(self, button_action):
        self._add_transaction_button.Bind(wx.EVT_BUTTON, button_action)


if __name__ == '__main__':
    app = wx.App()
    budget = BudgetView()
    budget.set_transaction_list([
        ("2018-01-11", "Grocery", "Cash", 43.11, "Ran out of whole milk, and beef stew ingredients."),
        ("2018-02-23", "Utility", "Chase Visa", 1000.32, "Charter Xfinity Time Warner Cable Internet."),
        ("2018-01-11", "Maintenance", "Cash", 200.00, "Leaky ceiling repairs."),
        ("2018-01-11", "Entertainment", "US Bank Visa", 12.41, "Movie Ticket: Infinity War"),
        ("2018-01-11", "Education", "Cash", 2341.11, "College Tuition Payment"),
        ("2018-01-11", "Dine-out", "American Bank Mastercard", 41.13, "Jiro's Sushi"),
        ("2018-01-11", "Grocery", "ApplePay", 21.91, "Ingredients for Beef Curry"),
        ("2018-01-11", "Grocery", "Cash", 43.11, "Ran out of whole milk, and beef stew ingredients."),
        ("2018-02-23", "Utility", "Chase Visa", 1000.32, "Charter Xfinity Time Warner Cable Internet."),
        ("2018-01-11", "Maintenance", "Cash", 200.00, "Leaky ceiling repairs."),
        ("2018-01-11", "Entertainment", "US Bank Visa", 12.41, "Movie Ticket: Infinity War"),
        ("2018-01-11", "Education", "Cash", 2341.11, "College Tuition Payment"),
        ("2018-01-11", "Dine-out", "American Bank Mastercard", 41.13, "Jiro's Sushi"),
        ("2018-01-11", "Grocery", "ApplePay", 21.91, "Ingredients for Beef Curry"),
        ("2018-01-11", "Grocery", "Cash", 43.11, "Ran out of whole milk, and beef stew ingredients."),
        ("2018-02-23", "Utility", "Chase Visa", 1000.32, "Charter Xfinity Time Warner Cable Internet."),
        ("2018-01-11", "Maintenance", "Cash", 200.00, "Leaky ceiling repairs."),
        ("2018-01-11", "Entertainment", "US Bank Visa", 12.41, "Movie Ticket: Infinity War"),
        ("2018-01-11", "Education", "Cash", 2341.11, "College Tuition Payment"),
        ("2018-01-11", "Dine-out", "American Bank Mastercard", 41.13, "Jiro's Sushi"),
        ("2018-01-11", "Grocery", "ApplePay", 21.91, "Ingredients for Beef Curry"),
        ("2018-01-11", "Grocery", "Cash", 43.11, "Ran out of whole milk, and beef stew ingredients."),
        ("2018-02-23", "Utility", "Chase Visa", 1000.32, "Charter Xfinity Time Warner Cable Internet."),
        ("2018-01-11", "Maintenance", "Cash", 200.00, "Leaky ceiling repairs."),
        ("2018-01-11", "Entertainment", "US Bank Visa", 12.41, "Movie Ticket: Infinity War"),
        ("2018-01-11", "Education", "Cash", 2341.11, "College Tuition Payment"),
        ("2018-01-11", "Dine-out", "American Bank Mastercard", 41.13, "Jiro's Sushi"),
        ("2018-01-11", "Grocery", "ApplePay", 21.91, "Ingredients for Beef Curry"),
    ])
    app.MainLoop()