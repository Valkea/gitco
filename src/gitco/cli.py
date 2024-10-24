import typer
import importlib.metadata
from .gitco import gen_commit_msg
from .utils import get_version


app = typer.Typer()
app.command()(gen_commit_msg)

@app.callback()
def version(
    version: bool = typer.Option(None,
                                 "--version", "-v",
                                 callback=get_version,
                                 is_eager=True,
                                 help="Print the version and exit")
):
    pass

if __name__ == "__main__":
    app()
