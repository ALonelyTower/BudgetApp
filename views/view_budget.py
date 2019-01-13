import wx
import os

from views import view_menu


class BudgetView(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.Size(1140, 720),
                 style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr):

        super().__init__(parent, id, title, pos, size, style, name)

        self._create_column_id_variables()
        self._init_gui_control_widgets()
        self._bind_commands_to_gui_controls()

    def _create_column_id_variables(self):
        self._INDEX_COL = 0
        self._DATET_COL = 1
        self._CATEG_COL = 2
        self._PAYME_COL = 3
        self._TOTAL_COL = 4
        self._DESCR_COL = 5

    def _init_gui_control_widgets(self):
        # Methods are positionally dependent.  Reordering them may break things.
        self._panel = wx.Panel(parent=self)

        self._create_transaction_button()
        self._create_transaction_table()
        self._create_panel_sizer()

        self._menu_bar = view_menu.MenuBar(self)
        self._context_menu = view_menu.ContextMenu(self._trans_listview_ctrl)
        self.SetMenuBar(self._menu_bar)

    def _bind_commands_to_gui_controls(self):
        self._trans_listview_ctrl.Bind(wx.EVT_RIGHT_DOWN, self._on_right_click)

    def start(self):
        self.Show()

    def _create_transaction_button(self):
        # TODO: Move this explicit dependency somewhere else!
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
        self._trans_listview_ctrl = wx.ListView(self._panel, style=wx.LC_REPORT)

        self._trans_listview_ctrl.InsertColumn(col=self._INDEX_COL, heading="#",
                                               format=wx.LIST_FORMAT_CENTER, width=50)
        self._trans_listview_ctrl.InsertColumn(col=self._DATET_COL, heading="Date",
                                               format=wx.LIST_FORMAT_CENTER, width=100)
        self._trans_listview_ctrl.InsertColumn(col=self._CATEG_COL, heading="Category",
                                               format=wx.LIST_FORMAT_CENTER, width=200)
        self._trans_listview_ctrl.InsertColumn(col=self._PAYME_COL, heading="Payment Method",
                                               format=wx.LIST_FORMAT_CENTER, width=175)
        self._trans_listview_ctrl.InsertColumn(col=self._TOTAL_COL, heading="Total Expense",
                                               format=wx.LIST_FORMAT_LEFT, width=100)
        self._trans_listview_ctrl.InsertColumn(col=self._DESCR_COL, heading="Description",
                                               format=wx.LIST_FORMAT_CENTER, width=375)

    def _create_panel_sizer(self):
        self._grid_bag_sizer = wx.GridBagSizer(vgap=0, hgap=0)

        self._grid_bag_sizer.Add(window=self._add_transaction_button, pos=(0, 0),
                                 flag=wx.TOP | wx.LEFT | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=10)
        self._grid_bag_sizer.Add(window=self._trans_listview_ctrl, pos=(0, 1), flag=wx.EXPAND | wx.ALL, border=10)

        # Must only be set after adding widgets to Sizer.
        self._grid_bag_sizer.AddGrowableRow(0, 0)
        self._grid_bag_sizer.AddGrowableCol(0, 0)
        self._grid_bag_sizer.AddGrowableCol(1, 0)

        self._panel.SetSizer(self._grid_bag_sizer)

    def _on_right_click(self, event):
        off_flag = 0
        num_of_entries = self._trans_listview_ctrl.GetItemCount()
        for index in range(num_of_entries):
            self._trans_listview_ctrl.Select(index, on=off_flag)
        point = event.GetPosition()
        index, hit_flag = self._trans_listview_ctrl.HitTest(point)

        if hit_flag is wx.LIST_HITTEST_ONITEMLABEL:
            self._trans_listview_ctrl.Select(index)
            self._trans_listview_ctrl.Focus(index)
            self.PopupMenu(self._context_menu)

    def set_transaction_list_ctrl(self, transaction_list):
        self._trans_listview_ctrl.DeleteAllItems()
        for index, trans_dto in enumerate(transaction_list):
            list_item = self._create_list_item(index, trans_dto.id)
            list_item_index = self._trans_listview_ctrl.InsertItem(list_item)
            self._trans_listview_ctrl.SetItem(list_item_index, self._DATET_COL, trans_dto.date)
            self._trans_listview_ctrl.SetItem(list_item_index, self._CATEG_COL, f"{trans_dto.category}")
            self._trans_listview_ctrl.SetItem(list_item_index, self._PAYME_COL, trans_dto.payment_method)
            self._trans_listview_ctrl.SetItem(list_item_index, self._TOTAL_COL, f"${trans_dto.total_expense}")
            self._trans_listview_ctrl.SetItem(list_item_index, self._DESCR_COL, trans_dto.description)

    @staticmethod
    def _create_list_item(index, primary_key):
        """A ListView must be populated with a ListItem."""
        list_item = wx.ListItem()
        list_item.SetId(index)
        list_item.SetData(primary_key)
        list_item.SetText(f"{index + 1}")
        return list_item

    def get_selected_transaction_id(self):
        list_id = self._trans_listview_ctrl.GetFirstSelected()
        return self._trans_listview_ctrl.GetItemData(list_id)

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

    def bind_edit_categories_menu_item(self, button_action):
        command = self._create_command(button_action)
        self._menu_bar.bind_categories_context_button(command)

    @staticmethod
    def _create_command(button_action):
        def command(event):
            return button_action()
        return command


if __name__ == '__main__':
    app = wx.App()
    budget_view = BudgetView()
    budget_view.Show()
    app.MainLoop()
