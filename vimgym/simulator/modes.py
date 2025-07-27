"""Vim modes simulation for VimGym."""

from enum import Enum
from typing import Dict, Set


class VimMode(Enum):
    """Vim editor modes."""
    NORMAL = "normal"
    INSERT = "insert" 
    VISUAL = "visual"
    VISUAL_LINE = "visual_line"
    VISUAL_BLOCK = "visual_block"
    COMMAND = "command"
    REPLACE = "replace"


class ModeManager:
    """Manages Vim mode transitions and validation."""
    
    def __init__(self):
        """Initialize mode manager."""
        self.current_mode = VimMode.NORMAL
        self.previous_mode = VimMode.NORMAL
        self.mode_history = [VimMode.NORMAL]
        
        # Define valid mode transitions
        self.valid_transitions = self._build_transition_map()
        
        # Commands that can switch modes
        self.mode_commands = {
            # To INSERT mode
            'i': VimMode.INSERT,      # insert before cursor
            'I': VimMode.INSERT,      # insert at beginning of line
            'a': VimMode.INSERT,      # insert after cursor
            'A': VimMode.INSERT,      # insert at end of line
            'o': VimMode.INSERT,      # new line below
            'O': VimMode.INSERT,      # new line above
            'c': VimMode.INSERT,      # change (when combined with motion)
            'C': VimMode.INSERT,      # change to end of line
            's': VimMode.INSERT,      # substitute character
            'S': VimMode.INSERT,      # substitute line
            
            # To VISUAL mode
            'v': VimMode.VISUAL,      # character visual
            'V': VimMode.VISUAL_LINE, # line visual
            '\x16': VimMode.VISUAL_BLOCK,  # Ctrl-V, block visual
            
            # To COMMAND mode
            ':': VimMode.COMMAND,     # ex commands
            '/': VimMode.COMMAND,     # search forward
            '?': VimMode.COMMAND,     # search backward
            
            # To REPLACE mode
            'R': VimMode.REPLACE,     # replace mode
            
            # Back to NORMAL mode
            '\x1b': VimMode.NORMAL,   # Escape key
            '\x03': VimMode.NORMAL,   # Ctrl-C
        }
    
    def _build_transition_map(self) -> Dict[VimMode, Set[VimMode]]:
        """Build valid mode transition map.
        
        Returns:
            Dictionary mapping current mode to set of valid next modes
        """
        return {
            VimMode.NORMAL: {
                VimMode.INSERT, 
                VimMode.VISUAL, 
                VimMode.VISUAL_LINE,
                VimMode.VISUAL_BLOCK,
                VimMode.COMMAND,
                VimMode.REPLACE
            },
            VimMode.INSERT: {
                VimMode.NORMAL
            },
            VimMode.VISUAL: {
                VimMode.NORMAL,
                VimMode.INSERT,
                VimMode.VISUAL_LINE,
                VimMode.VISUAL_BLOCK
            },
            VimMode.VISUAL_LINE: {
                VimMode.NORMAL,
                VimMode.INSERT,
                VimMode.VISUAL,
                VimMode.VISUAL_BLOCK
            },
            VimMode.VISUAL_BLOCK: {
                VimMode.NORMAL,
                VimMode.INSERT,
                VimMode.VISUAL,
                VimMode.VISUAL_LINE
            },
            VimMode.COMMAND: {
                VimMode.NORMAL
            },
            VimMode.REPLACE: {
                VimMode.NORMAL
            }
        }
    
    def can_transition_to(self, target_mode: VimMode) -> bool:
        """Check if transition to target mode is valid.
        
        Args:
            target_mode: Mode to transition to
            
        Returns:
            True if transition is valid, False otherwise
        """
        return target_mode in self.valid_transitions.get(self.current_mode, set())
    
    def switch_mode(self, target_mode: VimMode) -> bool:
        """Switch to target mode if transition is valid.
        
        Args:
            target_mode: Mode to switch to
            
        Returns:
            True if mode was switched, False if invalid transition
        """
        if not self.can_transition_to(target_mode):
            return False
        
        self.previous_mode = self.current_mode
        self.current_mode = target_mode
        self.mode_history.append(target_mode)
        
        # Keep history limited
        if len(self.mode_history) > 100:
            self.mode_history = self.mode_history[-50:]
        
        return True
    
    def process_command(self, command: str) -> bool:
        """Process a command that might switch modes.
        
        Args:
            command: Command string to process
            
        Returns:
            True if mode was switched, False otherwise
        """
        if command in self.mode_commands:
            target_mode = self.mode_commands[command]
            return self.switch_mode(target_mode)
        return False
    
    def get_mode_display_name(self, mode: VimMode = None) -> str:
        """Get display name for mode.
        
        Args:
            mode: Mode to get name for (current mode if None)
            
        Returns:
            Display name for the mode
        """
        mode = mode or self.current_mode
        
        display_names = {
            VimMode.NORMAL: "NORMAL",
            VimMode.INSERT: "INSERT", 
            VimMode.VISUAL: "VISUAL",
            VimMode.VISUAL_LINE: "VISUAL LINE",
            VimMode.VISUAL_BLOCK: "VISUAL BLOCK",
            VimMode.COMMAND: "COMMAND",
            VimMode.REPLACE: "REPLACE"
        }
        
        return display_names.get(mode, mode.value.upper())
    
    def get_mode_color(self, mode: VimMode = None) -> str:
        """Get color for mode indicator.
        
        Args:
            mode: Mode to get color for (current mode if None)
            
        Returns:
            Color name for Rich styling
        """
        mode = mode or self.current_mode
        
        mode_colors = {
            VimMode.NORMAL: "purple",      # #c586c0
            VimMode.INSERT: "green",       # #4ec9b0
            VimMode.VISUAL: "yellow",      # #ffcc02
            VimMode.VISUAL_LINE: "yellow", # #ffcc02
            VimMode.VISUAL_BLOCK: "yellow",# #ffcc02
            VimMode.COMMAND: "blue",       # #569cd6
            VimMode.REPLACE: "red"         # #f44747
        }
        
        return mode_colors.get(mode, "white")
    
    def is_insert_mode(self) -> bool:
        """Check if currently in any insert-like mode.
        
        Returns:
            True if in insert or replace mode
        """
        return self.current_mode in [VimMode.INSERT, VimMode.REPLACE]
    
    def is_visual_mode(self) -> bool:
        """Check if currently in any visual mode.
        
        Returns:
            True if in any visual mode
        """
        return self.current_mode in [
            VimMode.VISUAL, 
            VimMode.VISUAL_LINE, 
            VimMode.VISUAL_BLOCK
        ]
    
    def is_command_mode(self) -> bool:
        """Check if currently in command mode.
        
        Returns:
            True if in command mode
        """
        return self.current_mode == VimMode.COMMAND
    
    def reset(self) -> None:
        """Reset to normal mode and clear history."""
        self.current_mode = VimMode.NORMAL
        self.previous_mode = VimMode.NORMAL
        self.mode_history = [VimMode.NORMAL]
    
    def get_available_commands(self) -> Dict[str, str]:
        """Get available mode-switching commands from current mode.
        
        Returns:
            Dictionary mapping commands to their descriptions
        """
        if self.current_mode == VimMode.NORMAL:
            return {
                'i': 'Insert before cursor',
                'I': 'Insert at beginning of line',
                'a': 'Insert after cursor', 
                'A': 'Insert at end of line',
                'o': 'Open line below',
                'O': 'Open line above',
                'v': 'Visual character mode',
                'V': 'Visual line mode',
                'Ctrl+V': 'Visual block mode',
                ':': 'Command mode',
                '/': 'Search forward',
                '?': 'Search backward',
                'R': 'Replace mode'
            }
        elif self.current_mode in [VimMode.INSERT, VimMode.REPLACE]:
            return {
                'Esc': 'Return to normal mode',
                'Ctrl+C': 'Return to normal mode'
            }
        elif self.is_visual_mode():
            return {
                'Esc': 'Return to normal mode',
                'v': 'Switch visual mode type',
                'V': 'Visual line mode',
                'Ctrl+V': 'Visual block mode'
            }
        elif self.current_mode == VimMode.COMMAND:
            return {
                'Esc': 'Return to normal mode',
                'Enter': 'Execute command'
            }
        
        return {}
    
    def get_mode_help_text(self) -> str:
        """Get help text for current mode.
        
        Returns:
            Help text describing current mode
        """
        help_texts = {
            VimMode.NORMAL: (
                "NORMAL mode is the default mode for navigation and commands. "
                "Use movement keys (h,j,k,l) to navigate, and mode keys (i,v,:) to switch modes."
            ),
            VimMode.INSERT: (
                "INSERT mode allows text input. Type normally to add text. "
                "Press Esc to return to NORMAL mode."
            ),
            VimMode.VISUAL: (
                "VISUAL mode allows text selection. Use movement keys to select text. "
                "Press y to copy, d to delete, or Esc to cancel."
            ),
            VimMode.VISUAL_LINE: (
                "VISUAL LINE mode selects entire lines. Use j/k to select more lines. "
                "Press y to copy, d to delete, or Esc to cancel."
            ),
            VimMode.VISUAL_BLOCK: (
                "VISUAL BLOCK mode selects rectangular blocks of text. "
                "Use movement keys to define the block. Press Esc to cancel."
            ),
            VimMode.COMMAND: (
                "COMMAND mode allows Ex commands. Type your command and press Enter. "
                "Press Esc to cancel."
            ),
            VimMode.REPLACE: (
                "REPLACE mode overwrites existing text. Type to replace characters. "
                "Press Esc to return to NORMAL mode."
            )
        }
        
        return help_texts.get(self.current_mode, "Unknown mode.")
    
    def get_state(self) -> Dict:
        """Get current mode manager state.
        
        Returns:
            Dictionary with current state
        """
        return {
            "current_mode": self.current_mode.value,
            "previous_mode": self.previous_mode.value,
            "mode_history": [mode.value for mode in self.mode_history[-10:]]  # Last 10 modes
        }
    
    def restore_state(self, state: Dict) -> None:
        """Restore mode manager state.
        
        Args:
            state: State dictionary to restore
        """
        try:
            self.current_mode = VimMode(state.get("current_mode", "normal"))
            self.previous_mode = VimMode(state.get("previous_mode", "normal"))
            
            # Restore history
            history = state.get("mode_history", ["normal"])
            self.mode_history = [VimMode(mode) for mode in history]
            
        except (ValueError, KeyError):
            # If state is corrupted, reset to default
            self.reset()