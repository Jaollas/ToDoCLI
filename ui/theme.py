from rich.console import Console
from rich.theme import Theme

APP_TITLE = "📝  To-Do List"

_tema = Theme(
    {
        "title": "bold cyan",
        "done": "bold green",
        "pending": "bold yellow",
        "danger": "bold red",
        "muted": "dim white",
        "key": "bold magenta",
        "pri.alta": "bold red",
        "pri.media": "bold yellow",
        "pri.baixa": "bold green",
        "cat": "bold cyan",
        "overdue": "bold red",
        "due.today": "bold red",
        "due.soon": "bold yellow",
        "due.ok": "green",
    }
)

console = Console(theme=_tema)
