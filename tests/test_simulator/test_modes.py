"""Tests for Vim mode management."""

import pytest

from vimgym.simulator.modes import VimMode, ModeManager


def test_mode_manager_initialization():
    """Test mode manager starts in normal mode."""
    manager = ModeManager()
    assert manager.current_mode == VimMode.NORMAL
    assert manager.previous_mode == VimMode.NORMAL
    assert len(manager.mode_history) == 1


def test_valid_mode_transitions():
    """Test valid mode transitions."""
    manager = ModeManager()
    
    # Normal to Insert
    assert manager.can_transition_to(VimMode.INSERT)
    assert manager.switch_mode(VimMode.INSERT)
    assert manager.current_mode == VimMode.INSERT
    assert manager.previous_mode == VimMode.NORMAL
    
    # Insert back to Normal
    assert manager.can_transition_to(VimMode.NORMAL)
    assert manager.switch_mode(VimMode.NORMAL)
    assert manager.current_mode == VimMode.NORMAL
    assert manager.previous_mode == VimMode.INSERT


def test_invalid_mode_transitions():
    """Test invalid mode transitions are rejected."""
    manager = ModeManager()
    
    # Switch to insert mode
    manager.switch_mode(VimMode.INSERT)
    
    # Cannot go directly from insert to visual
    assert not manager.can_transition_to(VimMode.VISUAL)
    assert not manager.switch_mode(VimMode.VISUAL)
    assert manager.current_mode == VimMode.INSERT  # Should stay in insert


def test_mode_command_processing():
    """Test processing commands that switch modes."""
    manager = ModeManager()
    
    # Test insert mode commands
    assert manager.process_command('i')
    assert manager.current_mode == VimMode.INSERT
    
    # Test escape back to normal
    assert manager.process_command('\x1b')  # Escape
    assert manager.current_mode == VimMode.NORMAL
    
    # Test visual mode
    assert manager.process_command('v')
    assert manager.current_mode == VimMode.VISUAL


def test_mode_display_names():
    """Test mode display name generation."""
    manager = ModeManager()
    
    assert manager.get_mode_display_name(VimMode.NORMAL) == "NORMAL"
    assert manager.get_mode_display_name(VimMode.INSERT) == "INSERT"
    assert manager.get_mode_display_name(VimMode.VISUAL) == "VISUAL"
    assert manager.get_mode_display_name(VimMode.COMMAND) == "COMMAND"


def test_mode_colors():
    """Test mode color assignments."""
    manager = ModeManager()
    
    assert manager.get_mode_color(VimMode.NORMAL) == "purple"
    assert manager.get_mode_color(VimMode.INSERT) == "green"
    assert manager.get_mode_color(VimMode.VISUAL) == "yellow"
    assert manager.get_mode_color(VimMode.COMMAND) == "blue"


def test_mode_helper_methods():
    """Test mode type checking methods."""
    manager = ModeManager()
    
    # Normal mode
    assert not manager.is_insert_mode()
    assert not manager.is_visual_mode()
    assert not manager.is_command_mode()
    
    # Insert mode
    manager.switch_mode(VimMode.INSERT)
    assert manager.is_insert_mode()
    assert not manager.is_visual_mode()
    assert not manager.is_command_mode()
    
    # Visual mode
    manager.switch_mode(VimMode.NORMAL)
    manager.switch_mode(VimMode.VISUAL)
    assert not manager.is_insert_mode()
    assert manager.is_visual_mode()
    assert not manager.is_command_mode()
    
    # Command mode
    manager.switch_mode(VimMode.NORMAL)
    manager.switch_mode(VimMode.COMMAND)
    assert not manager.is_insert_mode()
    assert not manager.is_visual_mode()
    assert manager.is_command_mode()


def test_mode_history():
    """Test mode history tracking."""
    manager = ModeManager()
    
    # Start with normal mode in history
    assert len(manager.mode_history) == 1
    assert manager.mode_history[0] == VimMode.NORMAL
    
    # Switch modes and check history
    manager.switch_mode(VimMode.INSERT)
    manager.switch_mode(VimMode.NORMAL)
    manager.switch_mode(VimMode.VISUAL)
    
    assert len(manager.mode_history) == 4
    assert manager.mode_history[-1] == VimMode.VISUAL
    assert manager.mode_history[-2] == VimMode.NORMAL
    assert manager.mode_history[-3] == VimMode.INSERT


def test_mode_reset():
    """Test mode manager reset functionality."""
    manager = ModeManager()
    
    # Change mode and history
    manager.switch_mode(VimMode.INSERT)
    manager.switch_mode(VimMode.NORMAL)
    manager.switch_mode(VimMode.VISUAL)
    
    # Reset should return to normal mode and clear history
    manager.reset()
    
    assert manager.current_mode == VimMode.NORMAL
    assert manager.previous_mode == VimMode.NORMAL
    assert len(manager.mode_history) == 1
    assert manager.mode_history[0] == VimMode.NORMAL


def test_available_commands():
    """Test getting available commands for each mode."""
    manager = ModeManager()
    
    # Normal mode should have many commands
    normal_commands = manager.get_available_commands()
    assert len(normal_commands) > 0
    assert 'i' in normal_commands
    assert 'v' in normal_commands
    assert ':' in normal_commands
    
    # Insert mode should have escape commands
    manager.switch_mode(VimMode.INSERT)
    insert_commands = manager.get_available_commands()
    assert 'Esc' in insert_commands
    assert 'Ctrl+C' in insert_commands
    
    # Visual mode should have mode switching commands
    manager.switch_mode(VimMode.NORMAL)
    manager.switch_mode(VimMode.VISUAL)
    visual_commands = manager.get_available_commands()
    assert 'Esc' in visual_commands
    assert 'v' in visual_commands


def test_mode_help_text():
    """Test mode help text generation."""
    manager = ModeManager()
    
    # Each mode should have help text
    normal_help = manager.get_mode_help_text()
    assert len(normal_help) > 0
    assert "NORMAL" in normal_help.upper()
    
    manager.switch_mode(VimMode.INSERT)
    insert_help = manager.get_mode_help_text()
    assert len(insert_help) > 0
    assert "INSERT" in insert_help.upper()
    
    manager.switch_mode(VimMode.NORMAL)
    manager.switch_mode(VimMode.VISUAL)
    visual_help = manager.get_mode_help_text()
    assert len(visual_help) > 0
    assert "VISUAL" in visual_help.upper()


def test_state_persistence():
    """Test mode manager state save/restore."""
    manager = ModeManager()
    
    # Change state
    manager.switch_mode(VimMode.INSERT)
    manager.switch_mode(VimMode.NORMAL)
    manager.switch_mode(VimMode.VISUAL)
    
    # Save state
    state = manager.get_state()
    
    # Create new manager and restore state
    new_manager = ModeManager()
    new_manager.restore_state(state)
    
    assert new_manager.current_mode == manager.current_mode
    assert new_manager.previous_mode == manager.previous_mode
    assert len(new_manager.mode_history) == len(manager.mode_history)


def test_corrupted_state_handling():
    """Test handling of corrupted state data."""
    manager = ModeManager()
    
    # Try to restore invalid state
    invalid_state = {"current_mode": "invalid_mode"}
    manager.restore_state(invalid_state)
    
    # Should reset to default state
    assert manager.current_mode == VimMode.NORMAL
    assert manager.previous_mode == VimMode.NORMAL