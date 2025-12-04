import sqlite3

conn = sqlite3.connect("todos.db")
c = conn.cursor()


class Database:
    """Handles database connection and initialization"""

    def __init__(self, db_name: str = "todos.db"):
        self.db_name = db_name
        self.conn: sqlite3.Connection = sqlite3.connect(db_name)
        self.cursor: sqlite3.Cursor = self.conn.cursor()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __enter__(self) -> "Database":
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
