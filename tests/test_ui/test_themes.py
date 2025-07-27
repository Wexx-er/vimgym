"""
Tests for VimGym UI themes and styling system.
"""

import pytest
from rich.style import Style

from vimgym.ui.themes import (
    ColorPalette,
    FontConfig,
    VimGymTheme,
    get_theme,
    set_theme,
    create_light_theme,
    create_high_contrast_theme
)


class TestColorPalette:
    """Test ColorPalette class."""
    
    def test_default_palette(self):
        """Test default color palette values."""
        palette = ColorPalette()
        
        assert palette.primary == "#007ACC"
        assert palette.bg_primary == "#1E1E1E"
        assert palette.text_primary == "#CCCCCC"
        assert palette.success == "#4CAF50"
    
    def test_custom_palette(self):
        """Test custom color palette."""
        palette = ColorPalette(
            primary="#FF0000",
            bg_primary="#000000"
        )
        
        assert palette.primary == "#FF0000"
        assert palette.bg_primary == "#000000"
        # Defaults should still work
        assert palette.success == "#4CAF50"


class TestFontConfig:
    """Test FontConfig class."""
    
    def test_default_fonts(self):
        """Test default font configuration."""
        fonts = FontConfig()
        
        assert fonts.header_font == "standard"
        assert fonts.progress_full == "█"
        assert fonts.locked_icon == "🔒"
        assert fonts.vim_icon == "⚡"
    
    def test_custom_fonts(self):
        """Test custom font configuration."""
        fonts = FontConfig(
            header_font="big",
            progress_full="■"
        )
        
        assert fonts.header_font == "big"
        assert fonts.progress_full == "■"
        # Defaults should still work
        assert fonts.locked_icon == "🔒"


class TestVimGymTheme:
    """Test VimGymTheme class."""
    
    def test_default_theme(self):
        """Test default theme creation."""
        theme = VimGymTheme()
        
        assert theme.palette is not None
        assert theme.fonts is not None
        assert isinstance(theme._styles, dict)
    
    def test_custom_theme(self):
        """Test custom theme creation."""
        palette = ColorPalette(primary="#FF0000")
        fonts = FontConfig(header_font="big")
        
        theme = VimGymTheme(palette=palette, fonts=fonts)
        
        assert theme.palette.primary == "#FF0000"
        assert theme.fonts.header_font == "big"
    
    def test_get_style(self):
        """Test style retrieval."""
        theme = VimGymTheme()
        
        # Test existing style
        style = theme.get_style("primary")
        assert isinstance(style, Style)
        
        # Test non-existing style returns default
        style = theme.get_style("nonexistent")
        assert isinstance(style, Style)
    
    def test_get_progress_style(self):
        """Test progress style retrieval."""
        theme = VimGymTheme()
        
        # Test all progress statuses
        statuses = ["locked", "available", "in_progress", "completed"]
        for status in statuses:
            style = theme.get_progress_style(status)
            assert isinstance(style, Style)
        
        # Test unknown status
        style = theme.get_progress_style("unknown")
        assert isinstance(style, Style)
    
    def test_get_status_icon(self):
        """Test status icon retrieval."""
        theme = VimGymTheme()
        
        # Test all status icons
        assert theme.get_status_icon("locked") == "🔒"
        assert theme.get_status_icon("available") == "📖"
        assert theme.get_status_icon("in_progress") == "⚡"
        assert theme.get_status_icon("completed") == "✅"
        
        # Test unknown status returns default
        assert theme.get_status_icon("unknown") == "📖"
    
    def test_create_gradient_text(self):
        """Test gradient text creation."""
        theme = VimGymTheme()
        
        result = theme.create_gradient_text("Hello", "#FF0000", "#00FF00")
        assert isinstance(result, str)
        assert "Hello" in result


class TestThemeFunctions:
    """Test theme utility functions."""
    
    def test_get_theme(self):
        """Test getting default theme."""
        theme = get_theme()
        assert isinstance(theme, VimGymTheme)
    
    def test_set_theme(self):
        """Test setting custom theme."""
        original_theme = get_theme()
        custom_palette = ColorPalette(primary="#FF0000")
        custom_theme = VimGymTheme(palette=custom_palette)
        
        set_theme(custom_theme)
        current_theme = get_theme()
        
        assert current_theme.palette.primary == "#FF0000"
        
        # Restore original theme
        set_theme(original_theme)
    
    def test_create_light_theme(self):
        """Test light theme creation."""
        light_theme = create_light_theme()
        
        assert isinstance(light_theme, VimGymTheme)
        assert light_theme.palette.bg_primary == "#FFFFFF"
        assert light_theme.palette.text_primary == "#333333"
    
    def test_create_high_contrast_theme(self):
        """Test high contrast theme creation."""
        hc_theme = create_high_contrast_theme()
        
        assert isinstance(hc_theme, VimGymTheme)
        assert hc_theme.palette.bg_primary == "#000000"
        assert hc_theme.palette.text_primary == "#FFFFFF"