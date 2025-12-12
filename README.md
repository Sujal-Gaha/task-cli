# Todo CLI App

A simple command-line task manager built with Typer, Rich, and SQLite.
It lets you add, update, complete, delete, and list todos directly from the terminal.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run the CLI:

```bash
python main.py --help
```

### Add a task

```bash
python main.py add "Buy milk" "Groceries"
```

### Update a task

```bash
python main.py update 1 --task "Buy oat milk"
```

### Mark as completed

```bash
python main.py complete 1
```

### Delete a task

```bash
python main.py delete 1
```

### Show all tasks

```bash
python main.py show
```

## Features

- SQLite-backed persistent storage
- Colorful terminal UI using Rich
- Categories with automatic color mapping
- Reusable database connection via simple dependency injection
