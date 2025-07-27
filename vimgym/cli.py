"""
VimGym CLI module
"""

import click
from rich.console import Console
from rich.text import Text

from . import __version__

console = Console()


@click.group()
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """VimGym - Interactive tutorial for vim"""
    ctx.ensure_object(dict)


@cli.command()
def hello() -> None:
    """Test command to verify CLI is working"""
    text = Text("Hello from VimGym!", style="bold green")
    console.print(text)
    console.print("🎯 Welcome to the interactive vim tutorial!")
    console.print("Use 'vimgym --help' to see available commands.")


@cli.command()
def status() -> None:
    """Show VimGym status and configuration"""
    console.print(f"[bold]VimGym v{__version__}[/bold]")
    console.print("Status: Ready for development")
    console.print("📚 Data directory: ./data")
    console.print("🧪 Tests directory: ./tests")


if __name__ == "__main__":
    cli()
