import sqlite3

from sqlite3 import Connection, Cursor

conn: Connection = sqlite3.connect("todos.db")
c: Cursor = conn.cursor()


class Database:
    """Handles database connection and initialization"""

    def __init__(self, db_name: str = "todos.db") -> None:
        self.db_name: str = db_name
        self.conn: sqlite3.Connection = sqlite3.connect(db_name)
        self.cursor: sqlite3.Cursor = self.conn.cursor()

    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __enter__(self) -> "Database":
        """Context manager entry"""
        return self

    def __exit__(self) -> None:
        """Context manager exit"""
        self.close()
