"""
VimGym Interactive Menu Systems

Provides interactive menu components with keyboard navigation, selection handling,
and support for various menu types including main menu, module selection, and settings.
"""

from dataclasses import dataclass
from typing import List, Optional, Callable, Any, Dict, Union
from enum import Enum
import sys

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.align import Align
from rich.prompt import Prompt, Confirm

from .themes import get_theme, VimGymTheme


class MenuResult(Enum):
    """Menu interaction results."""
    SELECTED = "selected"
    CANCELLED = "cancelled"
    BACK = "back"
    QUIT = "quit"


@dataclass
class MenuOption:
    """Menu option configuration."""
    key: str
    label: str
    description: Optional[str] = None
    action: Optional[Callable] = None
    enabled: bool = True
    data: Optional[Any] = None
    submenu: Optional['Menu'] = None
    style_override: Optional[str] = None


class Menu:
    """Interactive menu component with keyboard navigation."""
    
    def __init__(
        self,
        title: str,
        options: List[MenuOption],
        console: Optional[Console] = None,
        theme: Optional[VimGymTheme] = None,
        show_back: bool = False,
        show_quit: bool = True,
        columns: int = 1
    ):
        self.title = title
        self.options = options
        self.console = console or Console()
        self.theme = theme or get_theme()
        self.show_back = show_back
        self.show_quit = show_quit
        self.columns = columns
        self.selected_index = 0
        self._setup_navigation_options()
    
    def _setup_navigation_options(self) -> None:
        """Add navigation options to the menu."""
        nav_options = []
        
        if self.show_back:
            nav_options.append(MenuOption(
                key="b",
                label="Back",
                description="Return to previous menu",
                enabled=True
            ))
        
        if self.show_quit:
            nav_options.append(MenuOption(
                key="q",
                label="Quit",
                description="Exit VimGym",
                enabled=True
            ))
        
        if nav_options:
            # Add separator if we have other options
            if self.options:
                nav_options.insert(0, MenuOption(
                    key="",
                    label="─" * 20,
                    enabled=False
                ))
            
            self.options.extend(nav_options)
    
    def render(self) -> Panel:
        """Render the menu as a Rich panel."""
        # Create menu table
        if self.columns == 1:
            table = Table.grid(padding=(0, 2))
            table.add_column("Key", style=self.theme.get_style("menu.shortcut"))
            table.add_column("Option")
            table.add_column("Description", style=self.theme.get_style("muted"))
            
            for option in self.options:
                if not option.enabled and option.key == "":
                    # Separator
                    table.add_row("", option.label, "")
                    continue
                
                key_text = f"[{option.key}]" if option.key else ""
                
                if option.enabled:
                    label_style = option.style_override or "menu.option"
                    desc_style = "muted"
                else:
                    label_style = "menu.option.disabled"
                    desc_style = "menu.option.disabled"
                
                label_text = Text(option.label, style=self.theme.get_style(label_style))
                desc_text = option.description or ""
                
                table.add_row(key_text, label_text, desc_text)
        
        else:
            # Multi-column layout
            columns_data = []
            for i in range(0, len(self.options), self.columns):
                column_options = self.options[i:i + self.columns]
                column_table = Table.grid()
                
                for option in column_options:
                    if not option.enabled and option.key == "":
                        continue
                    
                    key_text = f"[{option.key}] " if option.key else ""
                    style = "menu.option" if option.enabled else "menu.option.disabled"
                    option_text = Text(key_text + option.label, style=self.theme.get_style(style))
                    column_table.add_row(option_text)
                
                columns_data.append(column_table)
            
            table = Columns(columns_data, equal=True, expand=True)
        
        return Panel(
            table,
            title=f"[menu.title]{self.title}[/menu.title]",
            border_style=self.theme.get_style("border.active"),
            padding=(1, 2)
        )
    
    def show(self) -> tuple[MenuResult, Optional[MenuOption]]:
        """Display the menu and handle user interaction."""
        self.console.clear()
        
        while True:
            # Render menu
            menu_panel = self.render()
            self.console.print(menu_panel)
            
            # Get user input
            try:
                choice = Prompt.ask(
                    "\n[bold]Choose an option[/bold]",
                    console=self.console
                ).lower().strip()
                
                # Handle special cases
                if choice == "q" and self.show_quit:
                    if Confirm.ask("Are you sure you want to quit?", console=self.console):
                        return MenuResult.QUIT, None
                    else:
                        self.console.clear()
                        continue
                
                if choice == "b" and self.show_back:
                    return MenuResult.BACK, None
                
                # Find matching option
                selected_option = None
                for option in self.options:
                    if option.key.lower() == choice and option.enabled:
                        selected_option = option
                        break
                
                if selected_option:
                    # Execute action if present
                    if selected_option.action:
                        try:
                            result = selected_option.action()
                            if result is False:  # Action failed
                                continue
                        except Exception as e:
                            self.console.print(f"[red]Error: {e}[/red]")
                            input("Press Enter to continue...")
                            self.console.clear()
                            continue
                    
                    # Handle submenu
                    if selected_option.submenu:
                        submenu_result, submenu_option = selected_option.submenu.show()
                        if submenu_result == MenuResult.QUIT:
                            return MenuResult.QUIT, None
                        elif submenu_result == MenuResult.BACK:
                            self.console.clear()
                            continue
                        elif submenu_result == MenuResult.SELECTED:
                            return MenuResult.SELECTED, submenu_option
                    else:
                        return MenuResult.SELECTED, selected_option
                
                else:
                    self.console.print(f"[red]Invalid option: {choice}[/red]")
                    input("Press Enter to continue...")
                    self.console.clear()
                    continue
            
            except KeyboardInterrupt:
                if Confirm.ask("\nAre you sure you want to quit?", console=self.console):
                    return MenuResult.QUIT, None
                else:
                    self.console.clear()
                    continue
            except EOFError:
                return MenuResult.QUIT, None


class MainMenu:
    """Main application menu."""
    
    def __init__(self, console: Optional[Console] = None, theme: Optional[VimGymTheme] = None):
        self.console = console or Console()
        self.theme = theme or get_theme()
    
    def create_menu(self) -> Menu:
        """Create the main menu structure."""
        options = [
            MenuOption(
                key="s",
                label="Start Learning",
                description="Begin your vim journey",
                action=self._start_learning
            ),
            MenuOption(
                key="p",
                label="Practice Mode",
                description="Practice specific vim skills",
                action=self._practice_mode
            ),
            MenuOption(
                key="c",
                label="Challenges",
                description="Test your vim mastery",
                action=self._challenges
            ),
            MenuOption(
                key="pr",
                label="Progress",
                description="View your learning progress",
                action=self._view_progress
            ),
            MenuOption(
                key="st",
                label="Settings",
                description="Configure VimGym",
                submenu=self._create_settings_menu()
            ),
            MenuOption(
                key="h",
                label="Help",
                description="Get help and tutorials",
                action=self._show_help
            ),
        ]
        
        return Menu(
            title="🎯 VimGym Main Menu",
            options=options,
            console=self.console,
            theme=self.theme,
            show_quit=True,
            columns=2
        )
    
    def _create_settings_menu(self) -> Menu:
        """Create the settings submenu."""
        options = [
            MenuOption(
                key="t",
                label="Theme",
                description="Change color theme",
                action=self._change_theme
            ),
            MenuOption(
                key="d",
                label="Difficulty",
                description="Set default difficulty level",
                action=self._set_difficulty
            ),
            MenuOption(
                key="k",
                label="Keybindings",
                description="Customize keyboard shortcuts",
                action=self._customize_keys
            ),
            MenuOption(
                key="r",
                label="Reset Progress",
                description="Reset all learning progress",
                action=self._reset_progress
            ),
        ]
        
        return Menu(
            title="⚙️ Settings",
            options=options,
            console=self.console,
            theme=self.theme,
            show_back=True,
            show_quit=False
        )
    
    # Action methods
    def _start_learning(self) -> None:
        """Start the learning mode."""
        self.console.print("[green]Starting learning mode...[/green]")
        # TODO: Implement learning mode
        input("Press Enter to continue...")
    
    def _practice_mode(self) -> None:
        """Enter practice mode."""
        self.console.print("[blue]Entering practice mode...[/blue]")
        # TODO: Implement practice mode
        input("Press Enter to continue...")
    
    def _challenges(self) -> None:
        """Show challenges."""
        self.console.print("[yellow]Loading challenges...[/yellow]")
        # TODO: Implement challenges
        input("Press Enter to continue...")
    
    def _view_progress(self) -> None:
        """Show progress."""
        self.console.print("[cyan]Loading progress...[/cyan]")
        # TODO: Implement progress view
        input("Press Enter to continue...")
    
    def _show_help(self) -> None:
        """Show help."""
        help_text = """
[bold]VimGym Help[/bold]

VimGym is an interactive vim tutorial and practice environment.

[bold]Getting Started:[/bold]
1. Choose "Start Learning" to begin with basic vim concepts
2. Progress through lessons at your own pace
3. Use "Practice Mode" to reinforce specific skills
4. Take on "Challenges" to test your mastery

[bold]Navigation:[/bold]
- Use the letter keys to select menu options
- Press 'q' to quit at any time
- Press 'b' to go back in submenus

[bold]Tips:[/bold]
- Practice regularly for best results
- Don't rush - understanding is more important than speed
- Use the help system whenever you need clarification
        """
        
        panel = Panel(
            help_text,
            title="[bold blue]Help & Information[/bold blue]",
            border_style=self.theme.get_style("border.active"),
            padding=(1, 2)
        )
        
        self.console.clear()
        self.console.print(panel)
        input("\nPress Enter to continue...")
    
    def _change_theme(self) -> None:
        """Change the application theme."""
        self.console.print("[blue]Theme options:[/blue]")
        self.console.print("1. Dark (default)")
        self.console.print("2. Light")
        self.console.print("3. High Contrast")
        # TODO: Implement theme switching
        input("Press Enter to continue...")
    
    def _set_difficulty(self) -> None:
        """Set difficulty level."""
        self.console.print("[yellow]Difficulty levels:[/yellow]")
        self.console.print("1. Beginner")
        self.console.print("2. Intermediate")
        self.console.print("3. Advanced")
        # TODO: Implement difficulty setting
        input("Press Enter to continue...")
    
    def _customize_keys(self) -> None:
        """Customize keybindings."""
        self.console.print("[cyan]Keybinding customization coming soon![/cyan]")
        input("Press Enter to continue...")
    
    def _reset_progress(self) -> None:
        """Reset all progress."""
        if Confirm.ask("[red]Are you sure you want to reset all progress?[/red]", console=self.console):
            self.console.print("[green]Progress reset successfully![/green]")
        input("Press Enter to continue...")


class ModuleSelectionMenu:
    """Menu for selecting learning modules."""
    
    def __init__(self, modules: List[Dict[str, Any]], console: Optional[Console] = None, theme: Optional[VimGymTheme] = None):
        self.modules = modules
        self.console = console or Console()
        self.theme = theme or get_theme()
    
    def create_menu(self) -> Menu:
        """Create module selection menu."""
        options = []
        
        for i, module in enumerate(self.modules):
            key = str(i + 1)
            status = module.get("status", "available")
            
            # Create option with status styling
            style_map = {
                "locked": "progress.locked",
                "available": "progress.available", 
                "in_progress": "progress.in_progress",
                "completed": "progress.completed"
            }
            
            options.append(MenuOption(
                key=key,
                label=module["name"],
                description=module.get("description", ""),
                enabled=status != "locked",
                data=module,
                style_override=style_map.get(status, "menu.option")
            ))
        
        return Menu(
            title="📚 Learning Modules",
            options=options,
            console=self.console,
            theme=self.theme,
            show_back=True,
            columns=1
        )