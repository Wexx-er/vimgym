"""
Tests for VimGym UI components.
"""

import pytest
from rich.text import Text
from rich.panel import Panel
from rich.rule import Rule
from rich.progress import Progress

from vimgym.ui.components import (
    ProgressBar,
    Header, 
    StatusIndicator,
    InfoPanel,
    KeyBindingDisplay,
    LoadingSpinner
)
from vimgym.ui.themes import VimGymTheme


class TestProgressBar:
    """Test ProgressBar component."""
    
    def test_default_progress_bar(self):
        """Test default progress bar creation."""
        bar = ProgressBar()
        
        assert bar.total == 100
        assert bar.current == 0
        assert bar.width == 40
        assert bar.show_percentage is True
    
    def test_custom_progress_bar(self):
        """Test custom progress bar configuration."""
        bar = ProgressBar(
            total=50,
            width=20,
            show_percentage=False,
            status="completed"
        )
        
        assert bar.total == 50
        assert bar.width == 20
        assert bar.show_percentage is False
        assert bar.status == "completed"
    
    def test_update_progress(self):
        """Test updating progress value."""
        bar = ProgressBar(total=100)
        
        bar.update(50)
        assert bar.current == 50
        
        # Test bounds checking
        bar.update(150)
        assert bar.current == 100
        
        bar.update(-10)
        assert bar.current == 0
    
    def test_set_status(self):
        """Test setting progress status."""
        bar = ProgressBar()
        
        bar.set_status("in_progress")
        assert bar.status == "in_progress"
    
    def test_render(self):
        """Test progress bar rendering."""
        bar = ProgressBar(total=100, width=10)
        bar.update(50)
        
        result = bar.render()
        assert isinstance(result, Text)
    
    def test_create_rich_progress(self):
        """Test Rich Progress creation."""
        bar = ProgressBar()
        progress = bar.create_rich_progress()
        
        assert isinstance(progress, Progress)


class TestHeader:
    """Test Header component."""
    
    def test_default_header(self):
        """Test default header creation."""
        header = Header()
        assert header.theme is not None
    
    def test_create_main_header(self):
        """Test main header creation."""
        header = Header()
        result = header.create_main_header()
        
        assert isinstance(result, Panel)
    
    def test_create_module_header(self):
        """Test module header creation."""
        header = Header()
        result = header.create_module_header("Test Module", "Test Subtitle")
        
        assert isinstance(result, Panel)
    
    def test_create_section_header(self):
        """Test section header creation."""
        header = Header()
        result = header.create_section_header("Test Section")
        
        assert isinstance(result, Rule)


class TestStatusIndicator:
    """Test StatusIndicator component."""
    
    def test_default_status_indicator(self):
        """Test default status indicator creation."""
        indicator = StatusIndicator()
        assert indicator.theme is not None
    
    def test_create_module_status(self):
        """Test module status creation."""
        indicator = StatusIndicator()
        result = indicator.create_module_status(
            "Test Module",
            "available",
            progress=(5, 10),
            description="Test description"
        )
        
        assert isinstance(result, Panel)
    
    def test_create_lesson_status(self):
        """Test lesson status creation."""
        indicator = StatusIndicator()
        result = indicator.create_lesson_status(
            "Test Lesson",
            "completed",
            "hard"
        )
        
        assert isinstance(result, Text)


class TestInfoPanel:
    """Test InfoPanel component."""
    
    def test_default_info_panel(self):
        """Test default info panel creation."""
        panel = InfoPanel()
        assert panel.theme is not None
    
    def test_create_tip_panel(self):
        """Test tip panel creation."""
        panel = InfoPanel()
        result = panel.create_tip_panel("Test Tip", "This is a test tip.")
        
        assert isinstance(result, Panel)
    
    def test_create_instruction_panel(self):
        """Test instruction panel creation."""
        panel = InfoPanel()
        instructions = ["Step 1", "Step 2", "Step 3"]
        result = panel.create_instruction_panel(instructions)
        
        assert isinstance(result, Panel)
    
    def test_create_vim_command_panel(self):
        """Test vim command panel creation."""
        panel = InfoPanel()
        commands = [("w", "Save file"), ("q", "Quit")]
        result = panel.create_vim_command_panel(commands)
        
        assert isinstance(result, Panel)
    
    def test_create_objective_panel(self):
        """Test objective panel creation."""
        panel = InfoPanel()
        requirements = ["Learn basic movement", "Practice commands"]
        result = panel.create_objective_panel(
            "Master vim basics",
            requirements
        )
        
        assert isinstance(result, Panel)


class TestKeyBindingDisplay:
    """Test KeyBindingDisplay component."""
    
    def test_default_key_binding_display(self):
        """Test default key binding display creation."""
        display = KeyBindingDisplay()
        assert display.theme is not None
    
    def test_create_key_help(self):
        """Test key help creation."""
        display = KeyBindingDisplay()
        bindings = [("q", "Quit"), ("h", "Help")]
        result = display.create_key_help(bindings)
        
        assert isinstance(result, Panel)
    
    def test_format_key_sequence(self):
        """Test key sequence formatting."""
        display = KeyBindingDisplay()
        keys = ["Ctrl", "w", "q"]
        result = display.format_key_sequence(keys)
        
        assert isinstance(result, Text)


class TestLoadingSpinner:
    """Test LoadingSpinner component."""
    
    def test_default_loading_spinner(self):
        """Test default loading spinner creation."""
        spinner = LoadingSpinner()
        assert spinner.message == "Loading..."
        assert spinner.theme is not None
    
    def test_custom_loading_spinner(self):
        """Test custom loading spinner creation."""
        spinner = LoadingSpinner("Custom message...")
        assert spinner.message == "Custom message..."
    
    def test_create_progress(self):
        """Test progress creation."""
        spinner = LoadingSpinner()
        progress = spinner.create_progress()
        
        assert isinstance(progress, Progress)