"""
VimGym UI Components

Reusable UI components for consistent interface design including progress bars,
headers, status indicators, and information panels.
"""

from typing import Optional, List, Union, Tuple, TYPE_CHECKING
from dataclasses import dataclass
from rich.console import Console, ConsoleOptions, RenderResult
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.rule import Rule

if TYPE_CHECKING:
    from rich.console import RenderableType

from .themes import get_theme, VimGymTheme


class ProgressBar:
    """Customizable progress bar component with VimGym theming."""
    
    def __init__(
        self,
        total: int = 100,
        width: Optional[int] = None,
        show_percentage: bool = True,
        show_eta: bool = False,
        status: str = "available",
        theme: Optional[VimGymTheme] = None
    ):
        self.total = total
        self.current = 0
        self.width = width or 40
        self.show_percentage = show_percentage
        self.show_eta = show_eta
        self.status = status
        self.theme = theme or get_theme()
    
    def update(self, current: int) -> None:
        """Update the current progress value."""
        self.current = min(max(0, current), self.total)
    
    def set_status(self, status: str) -> None:
        """Update the progress bar status."""
        self.status = status
    
    def render(self) -> Text:
        """Render the progress bar as Rich Text."""
        if self.total == 0:
            percentage = 100
        else:
            percentage = (self.current / self.total) * 100
        
        # Calculate bar components
        filled_width = int((percentage / 100) * self.width)
        empty_width = self.width - filled_width
        
        # Get theme colors and characters
        style = self.theme.get_progress_style(self.status)
        fill_char = self.theme.fonts.progress_full
        empty_char = self.theme.fonts.progress_empty
        
        # Build progress bar
        bar_text = Text()
        bar_text.append("[", style="muted")
        bar_text.append(fill_char * filled_width, style=style)
        bar_text.append(empty_char * empty_width, style="muted")
        bar_text.append("]", style="muted")
        
        if self.show_percentage:
            bar_text.append(f" {percentage:.1f}%", style=style)
        
        return bar_text
    
    def create_rich_progress(self) -> Progress:
        """Create a Rich Progress instance for advanced use cases."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=self.width),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=Console()
        )


class Header:
    """Header component with ASCII art and theming support."""
    
    def __init__(self, theme: Optional[VimGymTheme] = None):
        self.theme = theme or get_theme()
    
    def create_main_header(self) -> Panel:
        """Create the main VimGym header with ASCII art."""
        ascii_art = Text.from_markup("""
[header.main]
██╗   ██╗██╗███╗   ███╗ ██████╗██╗   ██╗███╗   ███╗
██║   ██║██║████╗ ████║██╔════╝╚██╗ ██╔╝████╗ ████║
██║   ██║██║██╔████╔██║██║  ███╗╚████╔╝ ██╔████╔██║
╚██╗ ██╔╝██║██║╚██╔╝██║██║   ██║ ╚██╔╝  ██║╚██╔╝██║
 ╚████╔╝ ██║██║ ╚═╝ ██║╚██████╔╝  ██║   ██║ ╚═╝ ██║
  ╚═══╝  ╚═╝╚═╝     ╚═╝ ╚═════╝   ╚═╝   ╚═╝     ╚═╝
[/header.main]

[secondary]Interactive Vim Tutorial & Practice Environment[/secondary]
        """.strip())
        
        return Panel(
            Align.center(ascii_art),
            border_style=self.theme.get_style("border"),
            padding=(1, 2)
        )
    
    def create_module_header(self, title: str, subtitle: Optional[str] = None) -> Panel:
        """Create a module header with title and optional subtitle."""
        content = Text()
        content.append(title, style=self.theme.get_style("header.module"))
        
        if subtitle:
            content.append("\n")
            content.append(subtitle, style=self.theme.get_style("secondary"))
        
        return Panel(
            Align.center(content),
            border_style=self.theme.get_style("border.active"),
            padding=(0, 2)
        )
    
    def create_section_header(self, title: str) -> Rule:
        """Create a section header with horizontal rule."""
        return Rule(
            title,
            style=self.theme.get_style("header.section"),
            align="left"
        )


class StatusIndicator:
    """Status indicator component for modules and lessons."""
    
    def __init__(self, theme: Optional[VimGymTheme] = None):
        self.theme = theme or get_theme()
    
    def create_module_status(
        self,
        name: str,
        status: str,
        progress: Optional[Tuple[int, int]] = None,
        description: Optional[str] = None
    ) -> Panel:
        """Create a module status card."""
        
        # Get status icon and style
        icon = self.theme.get_status_icon(status)
        style = self.theme.get_progress_style(status)
        
        content = Text()
        content.append(f"{icon} ", style=style)
        content.append(name, style=style)
        
        if progress:
            current, total = progress
            progress_bar = ProgressBar(total=total, width=20, status=status, theme=self.theme)
            progress_bar.update(current)
            content.append("\n")
            content.append(progress_bar.render())
        
        if description:
            content.append("\n")
            content.append(description, style=self.theme.get_style("muted"))
        
        # Choose border style based on status
        border_style = "border.active" if status == "in_progress" else "border"
        
        return Panel(
            content,
            border_style=self.theme.get_style(border_style),
            padding=(0, 1),
            width=30
        )
    
    def create_lesson_status(self, title: str, status: str, difficulty: str = "medium") -> Text:
        """Create a compact lesson status indicator."""
        icon = self.theme.get_status_icon(status)
        style = self.theme.get_progress_style(status)
        
        # Difficulty indicators
        difficulty_map = {
            "easy": "⭐",
            "medium": "⭐⭐", 
            "hard": "⭐⭐⭐"
        }
        difficulty_stars = difficulty_map.get(difficulty, "⭐⭐")
        
        text = Text()
        text.append(f"{icon} ", style=style)
        text.append(title, style=style)
        text.append(f" {difficulty_stars}", style=self.theme.get_style("muted"))
        
        return text


class InfoPanel:
    """Information panel component for tips, instructions, and content."""
    
    def __init__(self, theme: Optional[VimGymTheme] = None):
        self.theme = theme or get_theme()
    
    def create_tip_panel(self, title: str, content: str) -> Panel:
        """Create a tip panel with helpful information."""
        tip_content = Text()
        tip_content.append("💡 ", style=self.theme.get_style("status.info"))
        tip_content.append(title, style=self.theme.get_style("bright"))
        tip_content.append("\n\n")
        tip_content.append(content, style=self.theme.get_style("primary"))
        
        return Panel(
            tip_content,
            title="[status.info]Tip[/status.info]",
            border_style=self.theme.get_style("status.info"),
            padding=(1, 2)
        )
    
    def create_instruction_panel(self, instructions: List[str]) -> Panel:
        """Create an instruction panel with numbered steps."""
        content = Text()
        
        for i, instruction in enumerate(instructions, 1):
            content.append(f"{i}. ", style=self.theme.get_style("secondary"))
            content.append(instruction, style=self.theme.get_style("primary"))
            if i < len(instructions):
                content.append("\n")
        
        return Panel(
            content,
            title="[header.section]Instructions[/header.section]",
            border_style=self.theme.get_style("border.active"),
            padding=(1, 2)
        )
    
    def create_vim_command_panel(self, commands: List[Tuple[str, str]]) -> Panel:
        """Create a panel showing vim commands and descriptions."""
        table = Table(show_header=True, header_style=self.theme.get_style("header.section"))
        table.add_column("Command", style=self.theme.get_style("vim.command"), width=15)
        table.add_column("Description", style=self.theme.get_style("primary"))
        
        for command, description in commands:
            table.add_row(f":{command}", description)
        
        return Panel(
            table,
            title="[vim.command]Vim Commands[/vim.command]",
            border_style=self.theme.get_style("vim.command"),
            padding=(1, 2)
        )
    
    def create_objective_panel(self, objective: str, requirements: List[str]) -> Panel:
        """Create a lesson objective panel."""
        content = Text()
        content.append("🎯 ", style=self.theme.get_style("secondary"))
        content.append("Objective: ", style=self.theme.get_style("bright"))
        content.append(objective, style=self.theme.get_style("lesson.objective"))
        content.append("\n\n")
        
        content.append("Requirements:\n", style=self.theme.get_style("bright"))
        for req in requirements:
            content.append("• ", style=self.theme.get_style("secondary"))
            content.append(req, style=self.theme.get_style("primary"))
            content.append("\n")
        
        return Panel(
            content,
            title="[lesson.title]Lesson Goal[/lesson.title]",
            border_style=self.theme.get_style("lesson.title"),
            padding=(1, 2)
        )


class KeyBindingDisplay:
    """Component for displaying keyboard shortcuts and bindings."""
    
    def __init__(self, theme: Optional[VimGymTheme] = None):
        self.theme = theme or get_theme()
    
    def create_key_help(self, bindings: List[Tuple[str, str]]) -> Panel:
        """Create a help panel showing keyboard shortcuts."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style=self.theme.get_style("vim.key"))
        table.add_column(style=self.theme.get_style("muted"))
        
        for key, description in bindings:
            table.add_row(f"[{key}]", description)
        
        return Panel(
            table,
            title="[muted]Keyboard Shortcuts[/muted]",
            border_style=self.theme.get_style("border"),
            padding=(1, 2)
        )
    
    def format_key_sequence(self, keys: List[str]) -> Text:
        """Format a sequence of keys with proper styling."""
        text = Text()
        for i, key in enumerate(keys):
            if i > 0:
                text.append(" → ", style=self.theme.get_style("muted"))
            text.append(key, style=self.theme.get_style("vim.key"))
        return text


class LoadingSpinner:
    """Loading spinner component for async operations."""
    
    def __init__(self, message: str = "Loading...", theme: Optional[VimGymTheme] = None):
        self.message = message
        self.theme = theme or get_theme()
    
    def create_progress(self) -> Progress:
        """Create a loading progress with spinner."""
        return Progress(
            SpinnerColumn(),
            TextColumn(f"[bold]{self.message}[/bold]"),
            transient=True
        )