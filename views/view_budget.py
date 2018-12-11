import wx
import os

from views import view_menu


class BudgetView(wx.Frame):
    # TODO: Add Asset class
    def __init__(self, parent=None, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr):
        # Unnecessary, but prefer to be explicit as it was driving me crazy keeping track.
        super().__init__(parent, id, title, pos, size, style, name)

        self._set_default_window_size()
        self._init_gui_control_widgets()
        self._bind_commands_to_gui_controls()

    def _set_default_window_size(self):
        self._window_size = wx.Size(1050, 720)
        self.SetMinSize(wx.Size(self._window_size))

    def _init_gui_control_widgets(self):
        # Methods are positionally dependent.  Reordering them may break things.
        self._panel = wx.Panel(parent=self)

        self._create_transaction_button()
        self._create_transaction_table()
        self._create_panel_sizer()

        self._menu_bar = view_menu.MenuBar(self)
        self._context_menu = view_menu.ContextMenu(self._transaction_list_view)
        self.SetMenuBar(self._menu_bar)

    def _bind_commands_to_gui_controls(self):
        self._transaction_list_view.Bind(wx.EVT_RIGHT_DOWN, self._on_right_click)

    def start(self):
        self.Show()

    def _create_transaction_button(self):
        bitmap_image_path = "W:\\BudgetApp\\appbar_add.png"
        if self._bitmap_image_exists(bitmap_image_path):
            add_bitmap_icon = wx.Bitmap("W:\\BudgetApp\\appbar_add.png")
            self._add_transaction_button = wx.BitmapButton(parent=self._panel, id=wx.ID_ANY,
                                                           bitmap=add_bitmap_icon, pos=wx.DefaultPosition,
                                                           size=(75, 75), style=wx.BU_AUTODRAW,
                                                           validator=wx.DefaultValidator, name="Add Transaction")
        else:
            self._add_transaction_button = wx.Button(parent=self._panel, id=wx.ID_ANY, label="Add Transaction",
                                                     pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
                                                     validator=wx.DefaultValidator, name="Add Transaction")

    @staticmethod
    def _bitmap_image_exists(path):
        return os.path.isfile(path)

    def _create_transaction_table(self):
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

        if hit_flag is wx.LIST_HITTEST_ABOVE | wx.LIST_HITTEST_ONITEMLABEL or hit_flag is wx.LIST_HITTEST_ONITEMLABEL:
            self._transaction_list_view.Select(index)
            self._transaction_list_view.Focus(index)
            self.PopupMenu(self._context_menu)

    def set_transaction_list_ctrl(self, transaction_list):
        # TODO: Refactor for readability
        self._transaction_list_view.DeleteAllItems()
        for index, trans in enumerate(transaction_list):
            list_item = self._create_list_item(index, trans[0], str(trans[1]))
            index = self._transaction_list_view.InsertItem(list_item)
            self._transaction_list_view.SetItem(index, 1, trans[2])
            self._transaction_list_view.SetItem(index, 2, trans[3])
            self._transaction_list_view.SetItem(index, 3, '$' + str(trans[4]))
            self._transaction_list_view.SetItem(index, 4, trans[5])

    @staticmethod
    def _create_list_item(index, primary_key, date):
        list_item = wx.ListItem()
        list_item.SetId(index)
        list_item.SetData(primary_key)
        list_item.SetText(date)
        return list_item

    def get_selected_transaction_id(self):
        list_id = self._transaction_list_view.GetFirstSelected()
        return self._transaction_list_view.GetItemData(list_id)

    def bind_add_transaction_action(self, button_action):
        command = self._create_command(button_action)
        self._add_transaction_button.Bind(wx.EVT_BUTTON, command)

    def bind_view_transaction_action(self, button_action):
        command = self._create_command(button_action)
        self._context_menu.bind_view_menu_item(command)

    def bind_edit_transaction_action(self, button_action):
        command = self._create_command(button_action)
        self._context_menu.bind_edit_menu_item(command)

    def bind_delete_transaction_action(self, button_action):
        command = self._create_command(button_action)
        self._context_menu.bind_delete_menu_item(command)

    @staticmethod
    def _create_command(button_action):
        # TODO: When things get out of hand, move to a command class
        def command(event):
            return button_action()
        return command


if __name__ == '__main__':
    app = wx.App(False)
    budget = BudgetView()
    budget.set_transaction_list_ctrl([
        (1, "2018-01-11", "Grocery", "Cash", 43.11, "Ran out of whole milk, and beef stew ingredients."),
        (2, "2018-02-23", "Utility", "Chase Visa", 1000.32, "Charter Xfinity Time Warner Cable Internet."),
        (3, "2018-01-11", "Maintenance", "Cash", 200.00, "Leaky ceiling repairs."),
        (4, "2018-01-11", "Entertainment", "US Bank Visa", 12.41, "Movie Ticket: Infinity War"),
        (5, "2018-01-11", "Education", "Cash", 2341.11, "College Tuition Payment"),
        (6, "2018-01-11", "Dine-out", "American Bank Mastercard", 41.13, "Jiro's Sushi"),
        (7, "2018-01-11", "Grocery", "ApplePay", 21.91, "Ingredients for Beef Curry"),
    ])
    budget.start()
    app.MainLoop()
