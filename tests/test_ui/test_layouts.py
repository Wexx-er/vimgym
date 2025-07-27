"""
Tests for VimGym UI layout managers.
"""

import pytest
from unittest.mock import Mock, patch

from rich.layout import Layout
from rich.panel import Panel
from rich.console import Group

from vimgym.ui.layouts import (
    ScreenSize,
    LayoutConfig,
    BaseLayout,
    MainMenuLayout,
    LessonLayout,
    ChallengeLayout,
    ProgressLayout
)
from vimgym.ui.themes import VimGymTheme


class TestLayoutConfig:
    """Test LayoutConfig dataclass."""
    
    def test_default_config(self):
        """Test default layout configuration."""
        config = LayoutConfig()
        
        assert config.min_width == 80
        assert config.min_height == 24
        assert config.header_height == 8
        assert config.footer_height == 3
        assert config.sidebar_width == 30
        assert config.content_padding == 2
    
    def test_custom_config(self):
        """Test custom layout configuration."""
        config = LayoutConfig(
            min_width=100,
            min_height=30,
            header_height=10
        )
        
        assert config.min_width == 100
        assert config.min_height == 30
        assert config.header_height == 10
        # Defaults should still work
        assert config.footer_height == 3


class TestBaseLayout:
    """Test BaseLayout base class."""
    
    def test_default_base_layout(self):
        """Test default base layout creation."""
        layout = BaseLayout()
        
        assert layout.console is not None
        assert layout.theme is not None
        assert layout.config is not None
        assert layout._header is not None
    
    def test_custom_base_layout(self):
        """Test custom base layout creation."""
        theme = VimGymTheme()
        config = LayoutConfig(min_width=100)
        
        layout = BaseLayout(theme=theme, config=config)
        
        assert layout.theme == theme
        assert layout.config.min_width == 100
    
    @patch('shutil.get_terminal_size')
    def test_get_terminal_size(self, mock_get_size):
        """Test terminal size detection."""
        mock_get_size.return_value = Mock(columns=120, lines=40)
        
        layout = BaseLayout()
        width, height = layout.get_terminal_size()
        
        assert width == 120
        assert height == 40
    
    @patch('shutil.get_terminal_size')
    def test_get_screen_size_category(self, mock_get_size):
        """Test screen size categorization."""
        layout = BaseLayout()
        
        # Test small screen
        mock_get_size.return_value = Mock(columns=70, lines=20)
        assert layout.get_screen_size_category() == ScreenSize.SMALL
        
        # Test medium screen
        mock_get_size.return_value = Mock(columns=100, lines=30)
        assert layout.get_screen_size_category() == ScreenSize.MEDIUM
        
        # Test large screen
        mock_get_size.return_value = Mock(columns=150, lines=50)
        assert layout.get_screen_size_category() == ScreenSize.LARGE
    
    @patch('shutil.get_terminal_size')
    def test_is_size_adequate(self, mock_get_size):
        """Test size adequacy checking."""
        layout = BaseLayout()
        
        # Test adequate size
        mock_get_size.return_value = Mock(columns=100, lines=30)
        assert layout.is_size_adequate() is True
        
        # Test inadequate size
        mock_get_size.return_value = Mock(columns=50, lines=10)
        assert layout.is_size_adequate() is False
    
    def test_create_footer(self):
        """Test footer creation."""
        layout = BaseLayout()
        bindings = [("q", "Quit"), ("h", "Help")]
        
        result = layout.create_footer(bindings)
        assert isinstance(result, Panel)


class TestMainMenuLayout:
    """Test MainMenuLayout class."""
    
    def test_default_main_menu_layout(self):
        """Test default main menu layout creation."""
        layout = MainMenuLayout()
        assert isinstance(layout, BaseLayout)
    
    @patch('shutil.get_terminal_size')
    def test_create_layout_small_screen(self, mock_get_size):
        """Test layout creation for small screens."""
        mock_get_size.return_value = Mock(columns=70, lines=30)
        
        layout = MainMenuLayout()
        menu_content = Mock()
        
        result = layout.create_layout(menu_content, show_stats=True)
        assert isinstance(result, Layout)
    
    @patch('shutil.get_terminal_size')
    def test_create_layout_large_screen(self, mock_get_size):
        """Test layout creation for large screens."""
        mock_get_size.return_value = Mock(columns=150, lines=50)
        
        layout = MainMenuLayout()
        menu_content = Mock()
        
        result = layout.create_layout(menu_content, show_stats=True)
        assert isinstance(result, Layout)
    
    def test_create_stats_sidebar(self):
        """Test stats sidebar creation."""
        layout = MainMenuLayout()
        result = layout._create_stats_sidebar()
        
        assert isinstance(result, Group)
    
    def test_create_progress_overview(self):
        """Test progress overview creation."""
        layout = MainMenuLayout()
        result = layout._create_progress_overview()
        
        assert isinstance(result, Group)


class TestLessonLayout:
    """Test LessonLayout class."""
    
    def test_default_lesson_layout(self):
        """Test default lesson layout creation."""
        layout = LessonLayout()
        assert isinstance(layout, BaseLayout)
    
    @patch('shutil.get_terminal_size')
    def test_create_layout(self, mock_get_size):
        """Test lesson layout creation."""
        mock_get_size.return_value = Mock(columns=120, lines=40)
        
        layout = LessonLayout()
        content = Mock()
        simulator_content = Mock()
        
        result = layout.create_layout(
            lesson_title="Test Lesson",
            objective="Learn testing",
            requirements=["Test requirement"],
            content=content,
            simulator_content=simulator_content
        )
        
        assert isinstance(result, Layout)
    
    def test_create_lesson_content_panel(self):
        """Test lesson content panel creation."""
        layout = LessonLayout()
        
        instructions = ["Step 1", "Step 2"]
        vim_commands = [("w", "Save"), ("q", "Quit")]
        code_example = "print('hello')"
        
        result = layout.create_lesson_content_panel(
            instructions=instructions,
            vim_commands=vim_commands,
            code_example=code_example
        )
        
        assert isinstance(result, Group)


class TestChallengeLayout:
    """Test ChallengeLayout class."""
    
    def test_default_challenge_layout(self):
        """Test default challenge layout creation."""
        layout = ChallengeLayout()
        assert isinstance(layout, BaseLayout)
    
    def test_create_layout(self):
        """Test challenge layout creation."""
        layout = ChallengeLayout()
        content = Mock()
        
        result = layout.create_layout(
            challenge_title="Test Challenge",
            description="Test description",
            difficulty="medium",
            time_limit=60,
            content=content
        )
        
        assert isinstance(result, Layout)
    
    def test_create_challenge_info(self):
        """Test challenge info creation."""
        layout = ChallengeLayout()
        
        result = layout._create_challenge_info(
            description="Test challenge",
            difficulty="hard",
            time_limit=120
        )
        
        assert isinstance(result, Group)
    
    def test_create_difficulty_display(self):
        """Test difficulty display creation."""
        layout = ChallengeLayout()
        
        # Test all difficulty levels
        difficulties = ["easy", "medium", "hard"]
        for difficulty in difficulties:
            result = layout._create_difficulty_display(difficulty)
            assert isinstance(result, Panel)
    
    def test_create_time_display(self):
        """Test time display creation."""
        layout = ChallengeLayout()
        result = layout._create_time_display(60)
        
        assert isinstance(result, Panel)
    
    def test_create_score_display(self):
        """Test score display creation."""
        layout = ChallengeLayout()
        result = layout._create_score_display()
        
        assert isinstance(result, Panel)


class TestProgressLayout:
    """Test ProgressLayout class."""
    
    def test_default_progress_layout(self):
        """Test default progress layout creation."""
        layout = ProgressLayout()
        assert isinstance(layout, BaseLayout)
    
    def test_create_layout(self):
        """Test progress layout creation."""
        layout = ProgressLayout()
        user_stats = {
            "total_time": 1200,
            "lessons_completed": 15,
            "overall_progress": 75
        }
        
        result = layout.create_layout(user_stats)
        assert isinstance(result, Layout)
    
    def test_create_stats_overview(self):
        """Test stats overview creation."""
        layout = ProgressLayout()
        stats = {"progress": 75}
        
        result = layout._create_stats_overview(stats)
        assert isinstance(result, Group)
    
    def test_create_detailed_progress(self):
        """Test detailed progress creation."""
        layout = ProgressLayout()
        stats = {"modules": []}
        
        result = layout._create_detailed_progress(stats)
        assert isinstance(result, Panel)