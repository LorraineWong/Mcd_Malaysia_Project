# db.py
import sqlite3
from typing import List, Optional
from models import Outlet  # Ensure this path is correct in your project

# Path to your SQLite database file
DB_PATH = "../Mcd_Scraper/mcd_outlets.db"

def get_db_connection():
    """
    Create and return a new SQLite connection with row_factory set to sqlite3.Row.
    This allows fetching rows as dictionary-like objects (access by column name).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_outlets() -> List[Outlet]:
    """
    Fetch all McDonald's outlets from the database and return as a list of Outlet objects.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM outlets")
    rows = cursor.fetchall()
    conn.close()
    # Use dictionary unpacking to directly map database fields to the Outlet model
    return [Outlet(**dict(row)) for row in rows]

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
        return Outlet(**dict(row))
    return None
