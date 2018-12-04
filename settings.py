from pathlib import Path

"""
This file will continue information in regards to the following:
    The base project directory
    The path to the developer database
    The path to the test database
"""
BASE_DIR = Path(__file__).parent
BASE_PATH = str(BASE_DIR)
DB_PATH = str(BASE_DIR / "budget.db")
FIXTURE_PATH = str(BASE_DIR / "tests" / "fixtures")
