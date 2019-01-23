import wx


from settings import DB_PATH
from data_storage.reset_database import reset_database
from data_storage.populate_database import populate_database
from presenters.presenter_budget import BudgetPresenter
from presenters.presenter_transaction import TransactionPresenter
from presenters.presenter_category import CategoryPresenter
from views.view_budget import BudgetView


"""
Simple script to run the program in its current state.


--WARNING--
Everything is reset each time this script is run.  If that behavior isn't desirable, set the fresh_start variable to
False.
"""


if __name__ == '__main__':
    fresh_start = False

    if fresh_start:
        reset_database(DB_PATH)
        populate_database(DB_PATH)

    app = wx.App(False)
    budget_v = BudgetView()
    categ_p = CategoryPresenter()
    budget_v.bind_edit_categories_menu_item(categ_p.display_categories_menu)
    trans_p = TransactionPresenter(categ_p)
    budget_presenter = BudgetPresenter(budget_v, trans_p)
    budget_v.start()
    app.MainLoop()
