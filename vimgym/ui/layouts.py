"""
VimGym Screen Layout Managers

Provides layout management for different screen types including lesson screens,
main menu layout, and responsive handling for various terminal sizes.
"""

import shutil
from typing import Optional, List, Dict, Any, Tuple, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from rich.text import Text
from rich.rule import Rule

if TYPE_CHECKING:
    from rich.console import RenderableType

from .themes import get_theme, VimGymTheme
from .components import Header, StatusIndicator, InfoPanel, ProgressBar, KeyBindingDisplay


class ScreenSize(Enum):
    """Screen size categories for responsive design."""
    SMALL = "small"      # < 80 columns
    MEDIUM = "medium"    # 80-120 columns
    LARGE = "large"      # > 120 columns


@dataclass
class LayoutConfig:
    """Configuration for layout behavior."""
    min_width: int = 80
    min_height: int = 24
    header_height: int = 8
    footer_height: int = 3
    sidebar_width: int = 30
    content_padding: int = 2


class BaseLayout:
    """Base layout manager with common functionality."""
    
    def __init__(
        self,
        console: Optional[Console] = None,
        theme: Optional[VimGymTheme] = None,
        config: Optional[LayoutConfig] = None
    ):
        self.console = console or Console()
        self.theme = theme or get_theme()
        self.config = config or LayoutConfig()
        self._header = Header(theme=self.theme)
        self._status = StatusIndicator(theme=self.theme)
        self._info = InfoPanel(theme=self.theme)
        self._keys = KeyBindingDisplay(theme=self.theme)
    
    def get_terminal_size(self) -> Tuple[int, int]:
        """Get current terminal size."""
        size = shutil.get_terminal_size()
        return size.columns, size.lines
    
    def get_screen_size_category(self) -> ScreenSize:
        """Determine screen size category."""
        width, _ = self.get_terminal_size()
        
        if width < 80:
            return ScreenSize.SMALL
        elif width <= 120:
            return ScreenSize.MEDIUM
        else:
            return ScreenSize.LARGE
    
    def is_size_adequate(self) -> bool:
        """Check if terminal size is adequate for the UI."""
        width, height = self.get_terminal_size()
        return width >= self.config.min_width and height >= self.config.min_height
    
    def clear_screen(self) -> None:
        """Clear the screen."""
        self.console.clear()
    
    def create_footer(self, bindings: List[Tuple[str, str]]) -> Panel:
        """Create a footer with key bindings."""
        return self._keys.create_key_help(bindings)


class MainMenuLayout(BaseLayout):
    """Layout manager for the main menu screen."""
    
    def create_layout(self, menu_content: "RenderableType", show_stats: bool = True) -> Layout:
        """Create the main menu layout."""
        layout = Layout()
        
        # Header section
        layout.split_column(
            Layout(name="header", size=self.config.header_height),
            Layout(name="body"),
            Layout(name="footer", size=self.config.footer_height)
        )
        
        # Set header content
        layout["header"].update(self._header.create_main_header())
        
        # Body layout depends on screen size
        screen_size = self.get_screen_size_category()
        
        if screen_size == ScreenSize.SMALL:
            # Single column for small screens
            layout["body"].update(menu_content)
        else:
            # Two column layout for medium/large screens
            layout["body"].split_row(
                Layout(name="menu", ratio=2),
                Layout(name="sidebar", ratio=1, minimum_size=self.config.sidebar_width)
            )
            
            layout["menu"].update(menu_content)
            
            if show_stats:
                layout["sidebar"].update(self._create_stats_sidebar())
        
        # Footer with key bindings
        footer_bindings = [
            ("q", "Quit"),
            ("h", "Help"),
            ("↑↓", "Navigate")
        ]
        layout["footer"].update(self.create_footer(footer_bindings))
        
        return layout
    
    def _create_stats_sidebar(self) -> Group:
        """Create sidebar with user stats and quick info."""
        components = []
        
        # Progress overview
        progress_panel = Panel(
            self._create_progress_overview(),
            title="[bold]Progress Overview[/bold]",
            border_style=self.theme.get_style("border"),
            padding=(1, 1)
        )
        components.append(progress_panel)
        
        # Quick tips
        tip_content = Text()
        tip_content.append("💡 Tip: ", style=self.theme.get_style("status.info"))
        tip_content.append("Practice daily for 15-20 minutes to build muscle memory!", 
                          style=self.theme.get_style("primary"))
        
        tip_panel = Panel(
            tip_content,
            title="[bold]Daily Tip[/bold]",
            border_style=self.theme.get_style("status.info"),
            padding=(1, 1)
        )
        components.append(tip_panel)
        
        return Group(*components)
    
    def _create_progress_overview(self) -> Group:
        """Create a progress overview display."""
        components = []
        
        # Overall progress
        overall_progress = ProgressBar(total=100, width=20, status="in_progress", theme=self.theme)
        overall_progress.update(45)  # Example: 45% complete
        
        progress_text = Text()
        progress_text.append("Overall: ", style=self.theme.get_style("bright"))
        progress_text.append("\n")
        progress_text.append(overall_progress.render())
        
        components.append(progress_text)
        components.append(Text())  # Spacer
        
        # Module breakdown
        modules_data = [
            ("Basics", "completed", 100),
            ("Movement", "in_progress", 60),
            ("Editing", "available", 0),
            ("Advanced", "locked", 0)
        ]
        
        for name, status, progress in modules_data:
            module_text = Text()
            icon = self.theme.get_status_icon(status)
            style = self.theme.get_progress_style(status)
            
            module_text.append(f"{icon} {name}: ", style=style)
            module_text.append(f"{progress}%", style=style)
            components.append(module_text)
        
        return Group(*components)


class LessonLayout(BaseLayout):
    """Layout manager for lesson screens."""
    
    def create_layout(
        self,
        lesson_title: str,
        objective: str,
        requirements: List[str],
        content: "RenderableType",
        simulator_content: Optional["RenderableType"] = None
    ) -> Layout:
        """Create the lesson layout."""
        layout = Layout()
        
        screen_size = self.get_screen_size_category()
        
        # Basic layout structure
        layout.split_column(
            Layout(name="header", size=4),
            Layout(name="objective", size=6),
            Layout(name="body"),
            Layout(name="footer", size=self.config.footer_height)
        )
        
        # Header
        layout["header"].update(
            self._header.create_module_header(lesson_title, "Interactive Lesson")
        )
        
        # Objective panel
        layout["objective"].update(
            self._info.create_objective_panel(objective, requirements)
        )
        
        # Body layout varies by screen size
        if screen_size == ScreenSize.SMALL or not simulator_content:
            # Single column layout
            layout["body"].update(content)
        else:
            # Split layout with simulator
            layout["body"].split_row(
                Layout(name="content", ratio=1),
                Layout(name="simulator", ratio=1)
            )
            
            layout["content"].update(content)
            layout["simulator"].update(simulator_content)
        
        # Footer
        footer_bindings = [
            ("n", "Next"),
            ("p", "Previous"),
            ("h", "Hint"),
            ("r", "Reset"),
            ("q", "Quit")
        ]
        layout["footer"].update(self.create_footer(footer_bindings))
        
        return layout
    
    def create_lesson_content_panel(
        self,
        instructions: List[str],
        vim_commands: Optional[List[Tuple[str, str]]] = None,
        code_example: Optional[str] = None
    ) -> Group:
        """Create the main lesson content panel."""
        components = []
        
        # Instructions
        if instructions:
            components.append(self._info.create_instruction_panel(instructions))
        
        # Vim commands reference
        if vim_commands:
            components.append(self._info.create_vim_command_panel(vim_commands))
        
        # Code example
        if code_example:
            code_panel = Panel(
                Text(code_example, style=self.theme.get_style("lesson.code")),
                title="[lesson.title]Example[/lesson.title]",
                border_style=self.theme.get_style("lesson.title"),
                padding=(1, 2)
            )
            components.append(code_panel)
        
        return Group(*components)


class ChallengeLayout(BaseLayout):
    """Layout manager for challenge screens."""
    
    def create_layout(
        self,
        challenge_title: str,
        description: str,
        difficulty: str,
        time_limit: Optional[int],
        content: "RenderableType"
    ) -> Layout:
        """Create the challenge layout."""
        layout = Layout()
        
        # Split into main sections
        layout.split_column(
            Layout(name="header", size=4),
            Layout(name="challenge_info", size=8),
            Layout(name="body"),
            Layout(name="footer", size=self.config.footer_height)
        )
        
        # Header
        layout["header"].update(
            self._header.create_module_header(challenge_title, f"Challenge • {difficulty.title()}")
        )
        
        # Challenge info
        layout["challenge_info"].update(
            self._create_challenge_info(description, difficulty, time_limit)
        )
        
        # Body
        layout["body"].update(content)
        
        # Footer
        footer_bindings = [
            ("s", "Start"),
            ("r", "Restart"),
            ("h", "Hint"),
            ("q", "Quit")
        ]
        layout["footer"].update(self.create_footer(footer_bindings))
        
        return layout
    
    def _create_challenge_info(
        self,
        description: str,
        difficulty: str,
        time_limit: Optional[int]
    ) -> Group:
        """Create challenge information display."""
        components = []
        
        # Description
        desc_text = Text()
        desc_text.append("🎯 ", style=self.theme.get_style("secondary"))
        desc_text.append(description, style=self.theme.get_style("primary"))
        
        desc_panel = Panel(
            desc_text,
            title="[bright]Challenge Description[/bright]",
            border_style=self.theme.get_style("border.active"),
            padding=(1, 2)
        )
        components.append(desc_panel)
        
        # Challenge details
        details_content = Columns([
            self._create_difficulty_display(difficulty),
            self._create_time_display(time_limit) if time_limit else Text(),
            self._create_score_display()
        ], equal=True)
        
        components.append(details_content)
        
        return Group(*components)
    
    def _create_difficulty_display(self, difficulty: str) -> Panel:
        """Create difficulty indicator."""
        difficulty_map = {
            "easy": ("🟢", "status.success"),
            "medium": ("🟡", "status.warning"),
            "hard": ("🔴", "status.error")
        }
        
        icon, style = difficulty_map.get(difficulty.lower(), ("⚪", "muted"))
        
        content = Text()
        content.append(icon + " ", style=self.theme.get_style(style))
        content.append(difficulty.title(), style=self.theme.get_style(style))
        
        return Panel(
            Align.center(content),
            title="Difficulty",
            border_style=self.theme.get_style("border"),
            padding=(0, 1)
        )
    
    def _create_time_display(self, time_limit: int) -> Panel:
        """Create time limit display."""
        content = Text()
        content.append("⏱️ ", style=self.theme.get_style("status.warning"))
        content.append(f"{time_limit}s", style=self.theme.get_style("bright"))
        
        return Panel(
            Align.center(content),
            title="Time Limit",
            border_style=self.theme.get_style("border"),
            padding=(0, 1)
        )
    
    def _create_score_display(self) -> Panel:
        """Create score/rating display."""
        content = Text()
        content.append("⭐ ", style=self.theme.get_style("status.info"))
        content.append("Best: --", style=self.theme.get_style("muted"))
        
        return Panel(
            Align.center(content),
            title="Best Score",
            border_style=self.theme.get_style("border"),
            padding=(0, 1)
        )


class ProgressLayout(BaseLayout):
    """Layout manager for progress/statistics screens."""
    
    def create_layout(self, user_stats: Dict[str, Any]) -> Layout:
        """Create the progress view layout."""
        layout = Layout()
        
        # Main sections
        layout.split_column(
            Layout(name="header", size=4),
            Layout(name="stats_overview", size=10),
            Layout(name="detailed_progress"),
            Layout(name="footer", size=self.config.footer_height)
        )
        
        # Header
        layout["header"].update(
            self._header.create_module_header("Progress Report", "Your VimGym Journey")
        )
        
        # Stats overview
        layout["stats_overview"].update(
            self._create_stats_overview(user_stats)
        )
        
        # Detailed progress
        layout["detailed_progress"].update(
            self._create_detailed_progress(user_stats)
        )
        
        # Footer
        footer_bindings = [
            ("r", "Refresh"),
            ("e", "Export"),
            ("b", "Back"),
            ("q", "Quit")
        ]
        layout["footer"].update(self.create_footer(footer_bindings))
        
        return layout
    
    def _create_stats_overview(self, stats: Dict[str, Any]) -> Group:
        """Create overview statistics display."""
        # This would be implemented with actual user statistics
        # For now, creating a template structure
        
        overview_panels = []
        
        # Overall progress
        overall_panel = Panel(
            Text("75% Complete", style=self.theme.get_style("status.success")),
            title="Overall Progress",
            border_style=self.theme.get_style("status.success")
        )
        overview_panels.append(overall_panel)
        
        # Time spent
        time_panel = Panel(
            Text("12h 30m", style=self.theme.get_style("status.info")),
            title="Time Spent",
            border_style=self.theme.get_style("status.info")
        )
        overview_panels.append(time_panel)
        
        # Lessons completed
        lessons_panel = Panel(
            Text("23/30", style=self.theme.get_style("status.warning")),
            title="Lessons",
            border_style=self.theme.get_style("status.warning")
        )
        overview_panels.append(lessons_panel)
        
        return Group(Columns(overview_panels, equal=True))
    
    def _create_detailed_progress(self, stats: Dict[str, Any]) -> Panel:
        """Create detailed progress breakdown."""
        # Template implementation
        content = Text("Detailed progress view would go here...")
        
        return Panel(
            content,
            title="[bright]Module Progress[/bright]",
            border_style=self.theme.get_style("border.active"),
            padding=(1, 2)
        )