"""Main CLI application for VimGym."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from . import __version__


class VimGym:
    """Main VimGym application controller."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize VimGym application.
        
        Args:
            config_path: Optional path to configuration directory
        """
        self.console = Console()
        self.config_path = config_path or self._get_default_config_path()
        self.running = False
        
    def _get_default_config_path(self) -> Path:
        """Get default configuration directory."""
        if sys.platform == "win32":
            import os
            appdata = os.environ.get('APPDATA')
            if appdata:
                return Path(appdata) / 'VimGym'
            else:
                return Path.home() / 'AppData' / 'Roaming' / 'VimGym'
        else:
            # Linux/macOS
            xdg_config = Path.home() / '.config'
            return xdg_config / 'vimgym'
    
    def run(self) -> None:
        """Start the main application loop."""
        self.running = True
        self.console.print("🏋️ [bold blue]VimGym - Interactive Vim Training[/bold blue]")
        self.console.print(f"Version: {__version__}")
        self.console.print()
        
        try:
            self._show_main_menu()
        except KeyboardInterrupt:
            self.console.print("\n👋 Goodbye! Happy Vim learning!")
        except Exception as e:
            self.console.print(f"❌ [red]Error: {e}[/red]")
            sys.exit(1)
    
    def _show_main_menu(self) -> None:
        """Display the main menu."""
        while self.running:
            self.console.print("\n📚 [bold]Main Menu[/bold]")
            self.console.print("1. Start Training")
            self.console.print("2. Continue Session")
            self.console.print("3. View Progress")
            self.console.print("4. Settings")
            self.console.print("5. Help")
            self.console.print("0. Exit")
            
            choice = click.prompt("\nSelect an option", type=click.Choice(['0', '1', '2', '3', '4', '5']))
            
            if choice == '0':
                self.running = False
                self.console.print("👋 Goodbye! Happy Vim learning!")
            elif choice == '1':
                self.console.print("🚧 Training modules coming soon!")
            elif choice == '2':
                self.console.print("🚧 Session management coming soon!")
            elif choice == '3':
                self.console.print("🚧 Progress tracking coming soon!")
            elif choice == '4':
                self.console.print("🚧 Settings coming soon!")
            elif choice == '5':
                self._show_help()
    
    def _show_help(self) -> None:
        """Show help information."""
        self.console.print("\n📖 [bold]VimGym Help[/bold]")
        self.console.print()
        self.console.print("VimGym is an interactive Vim tutor that helps you learn Vim")
        self.console.print("through hands-on practice in a safe simulated environment.")
        self.console.print()
        self.console.print("[bold]Features:[/bold]")
        self.console.print("• 7 learning modules from basics to advanced")
        self.console.print("• Interactive Vim simulator")
        self.console.print("• Progress tracking and achievements")
        self.console.print("• Challenge system")
        self.console.print("• Interactive cheat sheet")
        self.console.print()
        self.console.print("Navigate menus with number keys and press Enter to select.")
        self.console.print("Press Ctrl+C at any time to exit.")


@click.command()
@click.version_option(version=__version__)
@click.option('--config', type=click.Path(exists=True), help='Configuration directory path')
def main(config: Optional[str] = None) -> None:
    """VimGym - Interactive Vim Training in your terminal."""
    config_path = Path(config) if config else None
    app = VimGym(config_path)
    app.run()


if __name__ == "__main__":
    main()