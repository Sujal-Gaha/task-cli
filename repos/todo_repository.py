import sqlite3
from database import Database
import datetime
from typing import List, Optional
from models.todo import Todo


class TodoRepository:
    """Repository class for managing Todo operations"""

    def __init__(self, db_connection: Database):
        self.db = db_connection
        self.conn: sqlite3.Connection = db_connection.conn
        self.cursor: sqlite3.Cursor = db_connection.cursor
        self._create_table()

    def _create_table(self):
        """Create todos table if it doesn't exist"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                task TEXT,
                category TEXT,
                date_added TEXT,
                date_completed TEXT,
                status INTEGER,
                position INTEGER
            )
            """
        )
        self.conn.commit()

    def create(self, todo: Todo):
        """Create a new todo in the database"""
        self.cursor.execute("SELECT COUNT(*) FROM todos")
        count = self.cursor.fetchone()[0]
        todo.position = count if count else 0

        with self.conn:
            self.cursor.execute(
                """
                INSERT INTO todos (task, category, date_added, date_completed, status, position)
                VALUES (:task, :category, :date_added, :date_completed, :status, :position)
                """,
                {
                    "task": todo.task,
                    "category": todo.category,
                    "date_added": todo.date_added,
                    "date_completed": todo.date_completed,
                    "status": todo.status,
                    "position": todo.position,
                },
            )

    def get_all(self) -> List[Todo]:
        """Retrieve all todos from the database"""
        self.cursor.execute("SELECT * FROM todos")
        results = self.cursor.fetchall()
        todos = []
        for result in results:
            todos.append(Todo(*result))
        return todos

    def _change_position(
        self, old_position: int, new_position: int, commit: bool = True
    ):
        """Change the position of a todo"""
        self.cursor.execute(
            "UPDATE todos SET position = :position_new WHERE position = :position_old",
            {"position_old": old_position, "position_new": new_position},
        )

        if commit:
            self.conn.commit()

    def delete(self, position: int):
        """Delete a todo and reorder remaining todos"""
        self.cursor.execute("SELECT COUNT(*) FROM todos")
        count = self.cursor.fetchone()[0]

        with self.conn:
            self.cursor.execute(
                "DELETE FROM todos WHERE position = :position", {"position": position}
            )

            for pos in range(position + 1, count):
                self._change_position(pos, pos - 1, False)

    def update(
        self, position: int, task: Optional[str] = None, category: Optional[str] = None
    ):
        """Update a todo's task and/or category"""
        with self.conn:
            if task is not None and category is not None:
                self.cursor.execute(
                    "UPDATE todos SET task = :task, category = :category WHERE position = :position",
                    {"position": position, "task": task, "category": category},
                )
            elif task is not None:
                self.cursor.execute(
                    "UPDATE todos SET task = :task WHERE position = :position",
                    {"position": position, "task": task},
                )
            elif category is not None:
                self.cursor.execute(
                    "UPDATE todos SET category = :category WHERE position = :position",
                    {"position": position, "category": category},
                )

    def complete(self, position: int):
        """Mark a todo as completed"""
        with self.conn:
            self.cursor.execute(
                "UPDATE todos SET status = 2, date_completed = :date_completed WHERE position = :position",
                {
                    "position": position,
                    "date_completed": datetime.datetime.now().isoformat(),
                },
            )
