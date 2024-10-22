import typer

from .gitco import gen_commit_msg


app = typer.Typer()
app.command()(gen_commit_msg)


if __name__ == "__main__":
    app()
