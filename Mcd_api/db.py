import sqlite3
import json
from typing import List, Optional
from models import Outlet  # Ensure this path is correct in your project
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'mcd_outlets.db'))

def get_db_connection():
    """
    Create and return a new SQLite connection with row_factory set to sqlite3.Row.
    This allows fetching rows as dictionary-like objects (access by column name).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _row_to_outlet(row):
    """
    Convert a SQLite row to an Outlet object.
    Decodes the 'features' column from JSON string to dict.
    """
    row_dict = dict(row)
    # Decode features from JSON if exists
    features_str = row_dict.get("features")
    if features_str:
        try:
            row_dict["features"] = json.loads(features_str)
        except Exception:
            row_dict["features"] = {}
    else:
        row_dict["features"] = {}
    return Outlet(**row_dict)

def get_all_outlets() -> List[Outlet]:
    """
    Fetch all McDonald's outlets from the database and return as a list of Outlet objects.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM outlets")
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_outlet(row) for row in rows]

def get_outlet_by_id(outlet_id: int) -> Optional[Outlet]:
    """
    Fetch a single outlet by its ID.
    Returns the Outlet object if found, otherwise None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM outlets WHERE id = ?", (outlet_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return _row_to_outlet(row)
    return None
