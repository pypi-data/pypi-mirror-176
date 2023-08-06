import typer
from . import queue

app = typer.Typer()
app.add_typer(queue.app, name="queue")
