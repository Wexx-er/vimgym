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
    
    def render_introduction(self, lesson, progress: float) -> None:
        """Render lesson introduction with objectives and content."""
        self.console.clear()
        
        # Header with lesson info
        from rich.text import Text
        title_text = Text(f"📚 {lesson.title}", style="bold cyan")
        progress_text = Text(f"Progress: {progress:.0f}%", style="dim")
        header = Panel(
            title_text + "\n" + progress_text,
            border_style="bright_blue",
            padding=(1, 2)
        )
        self.console.print(header)
        
        # Learning objectives
        if lesson.content.learning_objectives:
            self.console.print("\n[bold yellow]🎯 Learning Objectives:[/bold yellow]")
            for objective in lesson.content.learning_objectives:
                self.console.print(f"  • {objective}")
        
        # Introduction content  
        if lesson.content.introduction:
            self.console.print("\n" + lesson.content.introduction)
        
        # Instructions
        if lesson.content.instructions:
            instructions_panel = Panel(
                lesson.content.instructions,
                title="📋 Instructions",
                border_style="green",
                padding=(1, 2)
            )
            self.console.print("\n")
            self.console.print(instructions_panel)
    
    def render_exercise(self, lesson, exercise, exercise_number: int,
                       total_exercises: int, simulator_state: Dict[str, Any],
                       exercise_stats: Dict[str, Any], lesson_progress: float) -> None:
        """Render current exercise with simulator state and progress."""
        self.console.clear()
        
        # Header with lesson and exercise info
        from rich.text import Text
        lesson_title = Text(f"📚 {lesson.title}", style="bold cyan")
        exercise_title = Text(f"Exercise {exercise_number}/{total_exercises}: {exercise.title}", style="bold yellow")
        progress_text = Text(f"Lesson Progress: {lesson_progress:.0f}%", style="dim")
        
        header_content = lesson_title + "\n" + exercise_title + "\n" + progress_text
        header = Panel(header_content, border_style="bright_blue", padding=(1, 2))
        self.console.print(header)
        
        # Exercise description and instructions
        description_panel = Panel(
            f"[bold]{exercise.description}[/bold]\n\n{exercise.instructions}",
            title="📋 Exercise Instructions",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(description_panel)
        
        # Current simulator state
        self._render_simulator_state(simulator_state)
        
        # Exercise statistics
        if exercise_stats:
            self._render_exercise_stats(exercise_stats)
    
    def _render_simulator_state(self, state: Dict[str, Any]) -> None:
        """Render the current state of the Vim simulator."""
        content = state.get("buffer_content", "")
        cursor_pos = state.get("cursor_position", (0, 0))
        mode = state.get("mode", "normal")
        
        # Display buffer content with cursor
        lines = content.split('\n') if content else ['']
        
        buffer_content = []
        for i, line in enumerate(lines):
            if i == cursor_pos[0]:
                # Show cursor position
                if cursor_pos[1] < len(line):
                    cursor_line = line[:cursor_pos[1]] + "[reverse]" + line[cursor_pos[1]] + "[/reverse]" + line[cursor_pos[1]+1:]
                else:
                    cursor_line = line + "[reverse] [/reverse]"
                buffer_content.append(f"{i+1:2d}: {cursor_line}")
            else:
                buffer_content.append(f"{i+1:2d}: {line}")
        
        # Create buffer panel
        buffer_text = "\n".join(buffer_content)
        buffer_panel = Panel(
            buffer_text,
            title=f"📝 Buffer (Mode: {mode.upper()})",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(buffer_panel)
    
    def _render_exercise_stats(self, stats: Dict[str, Any]) -> None:
        """Render exercise statistics and progress."""
        if not stats:
            return
        
        # Create a table for statistics
        from rich.table import Table
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Metric", style="dim")
        table.add_column("Value", style="bold")
        
        # Add statistics
        if "elapsed_time" in stats:
            table.add_row("⏱️ Time:", f"{stats['elapsed_time']}s")
        
        if "commands_executed" in stats and "expected_commands" in stats:
            progress = stats["commands_executed"] / max(stats["expected_commands"], 1)
            table.add_row("📊 Progress:", f"{stats['commands_executed']}/{stats['expected_commands']} ({progress:.0%})")
        
        if "hints_used" in stats and "hints_available" in stats:
            table.add_row("💡 Hints:", f"{stats['hints_used']}/{stats['hints_available']}")
        
        if "mistakes_made" in stats:
            table.add_row("❌ Mistakes:", str(stats["mistakes_made"]))
        
        # Display stats in a panel
        stats_panel = Panel(
            table,
            title="📈 Exercise Stats",
            border_style="yellow",
            padding=(0, 1)
        )
        self.console.print(stats_panel)
    
    def render_completion_summary(self, lesson, session_stats: Dict[str, Any],
                                 exercise_results: List[Any]) -> None:
        """Render lesson completion summary with final statistics."""
        self.console.clear()
        
        # Celebration header
        from rich.text import Text
        celebration = Text("🎉 Lesson Completed! 🎉", style="bold green")
        lesson_title = Text(f"'{lesson.title}'", style="bold cyan")
        header = Panel(
            celebration + "\n" + lesson_title,
            border_style="bright_green",
            padding=(2, 4)
        )
        self.console.print(header)
        
        # Session statistics
        if session_stats:
            self._render_session_stats(session_stats)
        
        # Exercise results summary
        if exercise_results:
            self._render_exercise_results(exercise_results)
        
        # Lesson summary
        if lesson.content.summary:
            summary_panel = Panel(
                lesson.content.summary,
                title="📋 Lesson Summary",
                border_style="green",
                padding=(1, 2)
            )
            self.console.print(summary_panel)
        
        # Tips for future
        if lesson.content.tips:
            self.console.print("\n[bold blue]💡 Tips to Remember:[/bold blue]")
            for tip in lesson.content.tips:
                self.console.print(f"  • {tip}")
    
    def _render_session_stats(self, stats: Dict[str, Any]) -> None:
        """Render session-level statistics."""
        from rich.table import Table
        table = Table(title="📊 Session Statistics", show_header=False, box=None)
        table.add_column("Metric", style="dim")
        table.add_column("Value", style="bold")
        
        if "duration" in stats:
            minutes = stats["duration"] // 60
            seconds = stats["duration"] % 60
            table.add_row("⏱️ Total Time:", f"{minutes}m {seconds}s")
        
        if "average_score" in stats:
            table.add_row("🎯 Average Score:", f"{stats['average_score']:.0f}%")
        
        if "exercises_completed" in stats:
            table.add_row("✅ Exercises:", str(stats["exercises_completed"]))
        
        if "total_hints_used" in stats:
            table.add_row("💡 Total Hints:", str(stats["total_hints_used"]))
        
        stats_panel = Panel(table, border_style="blue", padding=(1, 2))
        self.console.print(stats_panel)
    
    def _render_exercise_results(self, results: List[Any]) -> None:
        """Render individual exercise results."""
        if not results:
            return
        
        self.console.print("\n[bold blue]📝 Exercise Results:[/bold blue]")
        
        for i, result in enumerate(results, 1):
            status = "✅" if result.passed else "⚠️"
            score_color = "green" if result.score >= 80 else "yellow" if result.score >= 60 else "red"
            
            self.console.print(f"  {status} Exercise {i}: [{score_color}]{result.score}%[/{score_color}] "
                             f"({result.time_taken}s, {result.hints_used} hints)")


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