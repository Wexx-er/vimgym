"""
VimGym UI Themes and Styling System

Provides comprehensive theming support with VS Code-inspired dark theme,
color palettes, and Rich style definitions.
"""

from dataclasses import dataclass
from typing import Dict, Any
from rich.style import Style
from rich.color import Color


@dataclass
class ColorPalette:
    """Color palette for consistent theming across the application."""
    
    # Primary colors
    primary: str = "#007ACC"  # VS Code blue
    primary_dark: str = "#005A9E"
    primary_light: str = "#40A6FF"
    
    # Secondary colors  
    secondary: str = "#F9826C"  # Coral/orange accent
    secondary_dark: str = "#E55100"
    secondary_light: str = "#FFB74D"
    
    # Background colors
    bg_primary: str = "#1E1E1E"  # VS Code dark background
    bg_secondary: str = "#252526"  # VS Code sidebar
    bg_tertiary: str = "#2D2D30"  # VS Code panel
    bg_hover: str = "#2A2D2E"
    
    # Text colors
    text_primary: str = "#CCCCCC"  # VS Code primary text
    text_secondary: str = "#969696"  # VS Code secondary text
    text_muted: str = "#6A6A6A"  # VS Code muted text
    text_bright: str = "#FFFFFF"
    
    # Status colors
    success: str = "#4CAF50"  # Green
    warning: str = "#FF9800"  # Orange  
    error: str = "#F44336"    # Red
    info: str = "#2196F3"     # Blue
    
    # Progress states
    locked: str = "#6A6A6A"
    available: str = "#007ACC"
    in_progress: str = "#FF9800"
    completed: str = "#4CAF50"
    
    # Interactive elements
    border: str = "#3E3E42"
    border_active: str = "#007ACC"
    button_hover: str = "#094771"
    selection: str = "#264F78"


@dataclass
class FontConfig:
    """Font configuration for terminal display."""
    
    # ASCII Art fonts for headers
    header_font: str = "standard"  # figlet font name
    mini_header_font: str = "small"
    
    # Unicode symbols
    progress_full: str = "█"
    progress_empty: str = "░" 
    progress_partial: str = "▒"
    
    # Status indicators
    locked_icon: str = "🔒"
    available_icon: str = "📖"
    in_progress_icon: str = "⚡"
    completed_icon: str = "✅"
    star_icon: str = "⭐"
    
    # Navigation
    arrow_right: str = "→"
    arrow_left: str = "←"
    arrow_up: str = "↑"
    arrow_down: str = "↓"
    
    # Vim-specific symbols
    vim_icon: str = "⚡"
    command_icon: str = ":"
    normal_mode: str = "N"
    insert_mode: str = "I" 
    visual_mode: str = "V"


class VimGymTheme:
    """Comprehensive theme system for VimGym UI."""
    
    def __init__(self, palette: ColorPalette = None, fonts: FontConfig = None):
        self.palette = palette or ColorPalette()
        self.fonts = fonts or FontConfig()
        self._styles = self._create_styles()
    
    def _create_styles(self) -> Dict[str, Style]:
        """Create Rich style definitions based on the color palette."""
        return {
            # Text styles
            "primary": Style(color=self.palette.text_primary),
            "secondary": Style(color=self.palette.text_secondary),
            "muted": Style(color=self.palette.text_muted),
            "bright": Style(color=self.palette.text_bright, bold=True),
            
            # Header styles
            "header.main": Style(
                color=self.palette.primary,
                bold=True,
                italic=False
            ),
            "header.module": Style(
                color=self.palette.secondary,
                bold=True
            ),
            "header.section": Style(
                color=self.palette.text_bright,
                bold=True,
                underline=True
            ),
            
            # Status styles
            "status.success": Style(color=self.palette.success, bold=True),
            "status.warning": Style(color=self.palette.warning, bold=True),
            "status.error": Style(color=self.palette.error, bold=True),
            "status.info": Style(color=self.palette.info, bold=True),
            
            # Progress styles
            "progress.locked": Style(color=self.palette.locked, dim=True),
            "progress.available": Style(color=self.palette.available),
            "progress.in_progress": Style(color=self.palette.in_progress, bold=True),
            "progress.completed": Style(color=self.palette.completed, bold=True),
            
            # Menu styles
            "menu.title": Style(
                color=self.palette.primary,
                bold=True,
                underline=True
            ),
            "menu.option": Style(color=self.palette.text_primary),
            "menu.option.selected": Style(
                color=self.palette.text_bright,
                bgcolor=self.palette.selection,
                bold=True
            ),
            "menu.option.disabled": Style(
                color=self.palette.text_muted,
                dim=True
            ),
            "menu.shortcut": Style(
                color=self.palette.secondary,
                bold=True
            ),
            
            # Border and panel styles
            "border": Style(color=self.palette.border),
            "border.active": Style(color=self.palette.border_active),
            "panel.title": Style(
                color=self.palette.primary,
                bold=True
            ),
            "panel.content": Style(color=self.palette.text_primary),
            
            # Interactive elements
            "button": Style(
                color=self.palette.text_bright,
                bgcolor=self.palette.primary,
                bold=True
            ),
            "button.hover": Style(
                color=self.palette.text_bright,
                bgcolor=self.palette.button_hover,
                bold=True
            ),
            "link": Style(
                color=self.palette.primary,
                underline=True
            ),
            
            # Vim-specific styles
            "vim.command": Style(
                color=self.palette.secondary,
                bold=True,
                italic=True
            ),
            "vim.normal_mode": Style(
                color=self.palette.success,
                bold=True
            ),
            "vim.insert_mode": Style(
                color=self.palette.warning,
                bold=True
            ),
            "vim.visual_mode": Style(
                color=self.palette.info,
                bold=True
            ),
            "vim.key": Style(
                bgcolor=self.palette.bg_tertiary,
                color=self.palette.text_bright,
                bold=True
            ),
            
            # Lesson content styles
            "lesson.title": Style(
                color=self.palette.primary,
                bold=True,
                underline=True
            ),
            "lesson.objective": Style(
                color=self.palette.secondary,
                italic=True
            ),
            "lesson.code": Style(
                bgcolor=self.palette.bg_tertiary,
                color=self.palette.text_primary
            ),
            "lesson.highlight": Style(
                bgcolor=self.palette.selection,
                color=self.palette.text_bright
            ),
        }
    
    def get_style(self, name: str) -> Style:
        """Get a style by name."""
        return self._styles.get(name, Style())
    
    def get_progress_style(self, status: str) -> Style:
        """Get progress bar style based on status."""
        status_map = {
            "locked": "progress.locked",
            "available": "progress.available", 
            "in_progress": "progress.in_progress",
            "completed": "progress.completed"
        }
        return self.get_style(status_map.get(status, "progress.available"))
    
    def get_status_icon(self, status: str) -> str:
        """Get status icon based on status."""
        status_map = {
            "locked": self.fonts.locked_icon,
            "available": self.fonts.available_icon,
            "in_progress": self.fonts.in_progress_icon,
            "completed": self.fonts.completed_icon
        }
        return status_map.get(status, self.fonts.available_icon)
    
    def create_gradient_text(self, text: str, start_color: str, end_color: str) -> str:
        """Create gradient text effect (simplified for terminal)."""
        # For terminal display, we'll use the start color
        # Future enhancement could implement true gradient
        return f"[{start_color}]{text}[/{start_color}]"


# Default theme instance
_default_theme = VimGymTheme()


def get_theme() -> VimGymTheme:
    """Get the default VimGym theme."""
    return _default_theme


def set_theme(theme: VimGymTheme) -> None:
    """Set a custom theme as the default."""
    global _default_theme
    _default_theme = theme


# Predefined theme variations
def create_light_theme() -> VimGymTheme:
    """Create a light theme variant."""
    light_palette = ColorPalette(
        # Light theme colors
        bg_primary="#FFFFFF",
        bg_secondary="#F3F3F3", 
        bg_tertiary="#E8E8E8",
        text_primary="#333333",
        text_secondary="#666666",
        text_muted="#999999",
        text_bright="#000000",
        border="#CCCCCC",
        selection="#E3F2FD"
    )
    return VimGymTheme(palette=light_palette)


def create_high_contrast_theme() -> VimGymTheme:
    """Create a high contrast theme for accessibility."""
    hc_palette = ColorPalette(
        # High contrast colors
        primary="#00FFFF",
        bg_primary="#000000",
        bg_secondary="#111111",
        text_primary="#FFFFFF",
        text_secondary="#CCCCCC",
        text_bright="#FFFFFF",
        success="#00FF00",
        warning="#FFFF00",
        error="#FF0000"
    )
    return VimGymTheme(palette=hc_palette)