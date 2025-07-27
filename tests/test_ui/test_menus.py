"""
Tests for VimGym UI menu systems.
"""

import pytest
from unittest.mock import Mock, patch

from vimgym.ui.menus import (
    MenuResult,
    MenuOption,
    Menu,
    MainMenu,
    ModuleSelectionMenu
)
from vimgym.ui.themes import VimGymTheme


class TestMenuOption:
    """Test MenuOption dataclass."""
    
    def test_default_menu_option(self):
        """Test default menu option creation."""
        option = MenuOption(key="a", label="Test Option")
        
        assert option.key == "a"
        assert option.label == "Test Option"
        assert option.description is None
        assert option.enabled is True
        assert option.data is None
    
    def test_custom_menu_option(self):
        """Test custom menu option creation."""
        def test_action():
            return True
        
        option = MenuOption(
            key="b",
            label="Custom Option",
            description="Test description",
            action=test_action,
            enabled=False,
            data={"test": "data"}
        )
        
        assert option.key == "b"
        assert option.label == "Custom Option"
        assert option.description == "Test description"
        assert option.action == test_action
        assert option.enabled is False
        assert option.data == {"test": "data"}


class TestMenu:
    """Test Menu component."""
    
    def test_default_menu(self):
        """Test default menu creation."""
        options = [
            MenuOption(key="a", label="Option A"),
            MenuOption(key="b", label="Option B")
        ]
        menu = Menu("Test Menu", options)
        
        assert menu.title == "Test Menu"
        assert len(menu.options) >= 2  # Original options plus navigation
        assert menu.show_quit is True
        assert menu.columns == 1
    
    def test_custom_menu(self):
        """Test custom menu configuration."""
        options = [MenuOption(key="a", label="Option A")]
        menu = Menu(
            "Custom Menu",
            options,
            show_back=True,
            show_quit=False,
            columns=2
        )
        
        assert menu.title == "Custom Menu"
        assert menu.show_back is True
        assert menu.show_quit is False
        assert menu.columns == 2
    
    def test_render(self):
        """Test menu rendering."""
        options = [MenuOption(key="a", label="Option A")]
        menu = Menu("Test Menu", options)
        
        result = menu.render()
        # Should return a Panel or similar renderable
        assert result is not None
    
    @patch('rich.prompt.Prompt.ask')
    @patch('rich.prompt.Confirm.ask')
    def test_menu_navigation_options(self, mock_confirm, mock_prompt):
        """Test that navigation options are added correctly."""
        options = [MenuOption(key="a", label="Option A")]
        
        # Test with back and quit
        menu = Menu("Test", options, show_back=True, show_quit=True)
        # Should have original option + separator + back + quit
        assert len(menu.options) >= 4
        
        # Test with only quit
        menu = Menu("Test", options, show_back=False, show_quit=True)
        # Should have original option + separator + quit
        assert len(menu.options) >= 3


class TestMainMenu:
    """Test MainMenu component."""
    
    def test_default_main_menu(self):
        """Test default main menu creation."""
        main_menu = MainMenu()
        assert main_menu.console is not None
        assert main_menu.theme is not None
    
    def test_create_menu(self):
        """Test main menu creation."""
        main_menu = MainMenu()
        menu = main_menu.create_menu()
        
        assert isinstance(menu, Menu)
        assert "VimGym Main Menu" in menu.title
        assert len(menu.options) > 0
    
    @patch('builtins.input')
    def test_action_methods(self, mock_input):
        """Test that action methods execute without error."""
        mock_input.return_value = ""
        main_menu = MainMenu()
        
        # Test various action methods
        main_menu._start_learning()
        main_menu._practice_mode()
        main_menu._challenges()
        main_menu._view_progress()
        main_menu._show_help()
        main_menu._change_theme()
        main_menu._set_difficulty()
        main_menu._customize_keys()
    
    @patch('rich.prompt.Confirm.ask')
    @patch('builtins.input')
    def test_reset_progress(self, mock_input, mock_confirm):
        """Test reset progress action."""
        mock_input.return_value = ""
        mock_confirm.return_value = True
        
        main_menu = MainMenu()
        main_menu._reset_progress()
        
        mock_confirm.assert_called_once()


class TestModuleSelectionMenu:
    """Test ModuleSelectionMenu component."""
    
    def test_default_module_menu(self):
        """Test default module selection menu creation."""
        modules = [
            {
                "name": "Module 1",
                "description": "Test module",
                "status": "available"
            }
        ]
        menu = ModuleSelectionMenu(modules)
        
        assert menu.modules == modules
        assert menu.console is not None
        assert menu.theme is not None
    
    def test_create_menu(self):
        """Test module menu creation."""
        modules = [
            {
                "name": "Module 1",
                "description": "Test module 1",
                "status": "completed"
            },
            {
                "name": "Module 2", 
                "description": "Test module 2",
                "status": "in_progress"
            },
            {
                "name": "Module 3",
                "description": "Test module 3", 
                "status": "locked"
            }
        ]
        
        module_menu = ModuleSelectionMenu(modules)
        menu = module_menu.create_menu()
        
        assert isinstance(menu, Menu)
        assert "Learning Modules" in menu.title
        
        # Check that locked modules are disabled
        for option in menu.options:
            if hasattr(option, 'data') and option.data:
                if option.data.get('status') == 'locked':
                    assert option.enabled is False
                else:
                    assert option.enabled is True