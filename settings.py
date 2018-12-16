from pathlib import Path

"""
This file will continue information in regards to the following:
    The base project directory
    The path to the developer database
    The path to the test database
"""
BASE_DIR = Path(__file__).parent
BASE_PATH = str(BASE_DIR)
DB_PATH = str(BASE_DIR / "budget.sqlite")
DB_PATH_TEST = str(BASE_DIR / "tests" / "test_budget.sqlite")
TRANS_FIXTURE_PATH = str(BASE_DIR / "tests" / "fixtures" / "transaction_data.json")
CATEG_FIXTURE_PATH = str(BASE_DIR / "tests" / "fixtures" / "category_data.json")
