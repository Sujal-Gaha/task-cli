import typer
from rich.console import Console
from rich.table import Table
from models.todo import Todo
from database import Database
from repos.todo_repository import TodoRepository
from typing import Optional

console = Console()

app = typer.Typer()

# Global repository instance - initialized once
_db: Optional[Database] = None
_todo_repo: Optional[TodoRepository] = None


def get_todo_repo() -> TodoRepository:
    """
    Dependency injection function to get or create the TodoRepository instance.
    This ensures we reuse the same connection throughout the app lifecycle.
    """
    global _db, _todo_repo

    if _todo_repo is None:
        _db = Database("todos.db")
        _todo_repo = TodoRepository(_db)

    return _todo_repo


def cleanup():
    """Clean up database connection on app exit"""
    global _db

    if _db:
        _db.close()


@app.command(short_help="adds an item")
def add(task: str, category: str):
    """Add a new todo item"""
    repo = get_todo_repo()
    typer.echo(f"adding {task}, {category}")
    todo = Todo(task, category)
    repo.create(todo)
    show()


@app.command()
def delete(position: int):
    """Delete a todo item by position"""
    repo = get_todo_repo()
    typer.echo(f"deleting {position}")
    repo.delete(position - 1)
    show()


@app.command()
def update(position: int, task: Optional[str] = None, category: Optional[str] = None):
    """Update a todo item's task and/or category"""
    repo = get_todo_repo()
    typer.echo(f"updating {position}")
    repo.update(position - 1, task, category)
    show()


@app.command()
def complete(position: int):
    """Mark a todo item as completed"""
    repo = get_todo_repo()
    typer.echo(f"complete {position}")
    repo.complete(position - 1)
    show()


@app.command()
def show():
    """Display all todo items in a table"""
    repo = get_todo_repo()
    tasks = repo.get_all()

    console.print("[bold magenta]Todos[/bold magenta]!", "🖥️")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category: str) -> str:
        """Map category to color"""
        COLORS = {"Learn": "cyan", "Youtube": "red", "Sports": "cyan", "Study": "green"}
        if category in COLORS:
            return COLORS[category]
        return "white"

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = "✅" if task.status == 2 else "❌"
        table.add_row(str(idx), task.task, f"[{c}]{task.category}[/{c}]", is_done_str)

    console.print(table)


if __name__ == "__main__":
    app()
