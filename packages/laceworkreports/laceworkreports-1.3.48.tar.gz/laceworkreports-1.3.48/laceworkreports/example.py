"""Example of code."""
import typer

app: typer.Typer = typer.Typer()


def hello(name: str) -> str:
    """Just an greetings example.

    Args:
        name (str): Name to greet.

    Returns:
        str: greeting message

    Examples:
        .. code:: python

            >>> hello("Roman")
            'Hello Roman!'
    """
    return f"Hello {name}!"


if __name__ == "__main__":
    app()
