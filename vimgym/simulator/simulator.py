"""Main Vim simulator controller for VimGym."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .buffer import VimBuffer
from .commands import VimCommandProcessor, CommandResult
from .modes import VimMode, ModeManager


@dataclass
class SimulatorResponse:
    """Response from simulator input processing."""
    success: bool
    message: str = ""
    cursor_position: Tuple[int, int] = (0, 0)
    mode: VimMode = VimMode.NORMAL
    buffer_content: List[str] = None
    display_lines: List[str] = None
    status_line: str = ""
    error: Optional[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.buffer_content is None:
            self.buffer_content = []
        if self.display_lines is None:
            self.display_lines = []


class VimSimulator:
    """Main Vim simulator that coordinates all components."""
    
    def __init__(self, initial_content: str = ""):
        """Initialize simulator with optional content.
        
        Args:
            initial_content: Initial text content for the buffer
        """
        # Core components
        self.buffer = VimBuffer(initial_content)
        self.mode_manager = ModeManager()
        self.command_processor = VimCommandProcessor(self.buffer, self.mode_manager)
        
        # Display settings
        self.display_width = 80
        self.display_height = 24
        self.show_line_numbers = True
        self.highlight_cursor = True
        
        # State tracking
        self.last_command = ""
        self.command_count = 0
        self.error_message = ""
        
        # Learning mode settings
        self.learning_mode = True
        self.show_command_hints = True
        self.validate_commands = True
    
    def process_input(self, key_input: str) -> SimulatorResponse:
        """Process user input and return simulator response.
        
        Args:
            key_input: Raw key input from user
            
        Returns:
            SimulatorResponse with current state
        """
        try:
            # Process the command
            result = self.command_processor.process_key(key_input)
            
            # Update state tracking
            if result.success:
                self.last_command = key_input
                self.command_count += 1
                self.error_message = ""
            else:
                self.error_message = result.error or "Command failed"
            
            # Generate response
            response = SimulatorResponse(
                success=result.success,
                message=result.message,
                cursor_position=self.buffer.cursor_pos,
                mode=self.mode_manager.current_mode,
                buffer_content=self.buffer.lines.copy(),
                display_lines=self._generate_display_lines(),
                status_line=self._generate_status_line(),
                error=result.error
            )
            
            return response
            
        except Exception as e:
            return SimulatorResponse(
                success=False,
                error=f"Simulator error: {str(e)}",
                cursor_position=self.buffer.cursor_pos,
                mode=self.mode_manager.current_mode,
                buffer_content=self.buffer.lines.copy(),
                display_lines=self._generate_display_lines(),
                status_line=self._generate_status_line()
            )
    
    def _generate_display_lines(self) -> List[str]:
        """Generate lines for display with cursor and formatting.
        
        Returns:
            List of formatted display lines
        """
        display_lines = []
        cursor_line, cursor_col = self.buffer.cursor_pos
        
        for line_idx, line in enumerate(self.buffer.lines):
            display_line = ""
            
            # Add line numbers if enabled
            if self.show_line_numbers:
                display_line += f"{line_idx + 1:4d} "
            
            # Add line content with cursor highlighting
            if line_idx == cursor_line and self.highlight_cursor:
                # Insert cursor character
                if cursor_col < len(line):
                    display_line += line[:cursor_col] + "█" + line[cursor_col + 1:]
                else:
                    display_line += line + "█"
            else:
                display_line += line
            
            # Handle visual selection highlighting
            if (self.mode_manager.is_visual_mode() and 
                self.buffer.visual_start and self.buffer.visual_end):
                display_line = self._apply_visual_highlighting(display_line, line_idx)
            
            display_lines.append(display_line)
        
        # Pad to display height
        while len(display_lines) < self.display_height:
            if self.show_line_numbers:
                display_lines.append("    ~")
            else:
                display_lines.append("~")
        
        return display_lines[:self.display_height]
    
    def _apply_visual_highlighting(self, display_line: str, line_idx: int) -> str:
        """Apply visual selection highlighting to display line.
        
        Args:
            display_line: Line to highlight
            line_idx: Index of the line
            
        Returns:
            Line with visual highlighting applied
        """
        # TODO: Implement visual selection highlighting
        # This would apply special formatting to selected text
        return display_line
    
    def _generate_status_line(self) -> str:
        """Generate status line with current information.
        
        Returns:
            Formatted status line string
        """
        mode_name = self.mode_manager.get_mode_display_name()
        line_num, col_num = self.buffer.cursor_pos
        total_lines = self.buffer.get_line_count()
        
        # Basic status
        status_parts = [
            f"Mode: {mode_name}",
            f"Line: {line_num + 1}/{total_lines}",
            f"Col: {col_num + 1}"
        ]
        
        # Add last command if available
        if self.last_command:
            status_parts.append(f"Last: {repr(self.last_command)}")
        
        # Add command count
        if self.command_count > 0:
            status_parts.append(f"Commands: {self.command_count}")
        
        # Add error message if present
        if self.error_message:
            status_parts.append(f"Error: {self.error_message}")
        
        # Add learning hints if enabled
        if self.learning_mode and self.show_command_hints:
            available_commands = self.mode_manager.get_available_commands()
            if available_commands:
                hint = next(iter(available_commands.items()))
                status_parts.append(f"Hint: {hint[0]} - {hint[1]}")
        
        return " | ".join(status_parts)
    
    def reset(self, content: str = "") -> SimulatorResponse:
        """Reset simulator to clean state.
        
        Args:
            content: New content for the buffer
            
        Returns:
            SimulatorResponse with reset state
        """
        # Reset all components
        self.buffer = VimBuffer(content)
        self.mode_manager.reset()
        self.command_processor = VimCommandProcessor(self.buffer, self.mode_manager)
        
        # Reset state tracking
        self.last_command = ""
        self.command_count = 0
        self.error_message = ""
        
        return SimulatorResponse(
            success=True,
            message="Simulator reset",
            cursor_position=self.buffer.cursor_pos,
            mode=self.mode_manager.current_mode,
            buffer_content=self.buffer.lines.copy(),
            display_lines=self._generate_display_lines(),
            status_line=self._generate_status_line()
        )
    
    def set_learning_mode(self, enabled: bool) -> None:
        """Enable or disable learning mode features.
        
        Args:
            enabled: Whether to enable learning mode
        """
        self.learning_mode = enabled
        self.command_processor.validate_commands = enabled
    
    def set_display_options(self, width: int = None, height: int = None, 
                          line_numbers: bool = None, highlight_cursor: bool = None) -> None:
        """Configure display options.
        
        Args:
            width: Display width in characters
            height: Display height in lines
            line_numbers: Whether to show line numbers
            highlight_cursor: Whether to highlight cursor position
        """
        if width is not None:
            self.display_width = width
        if height is not None:
            self.display_height = height
        if line_numbers is not None:
            self.show_line_numbers = line_numbers
        if highlight_cursor is not None:
            self.highlight_cursor = highlight_cursor
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get complete current state for persistence.
        
        Returns:
            Dictionary with complete simulator state
        """
        return {
            "buffer_state": self.buffer.get_state(),
            "mode_state": self.mode_manager.get_state(),
            "cursor_position": self.buffer.cursor_pos,
            "last_command": self.last_command,
            "command_count": self.command_count,
            "display_settings": {
                "width": self.display_width,
                "height": self.display_height,
                "line_numbers": self.show_line_numbers,
                "highlight_cursor": self.highlight_cursor
            }
        }
    
    def restore_state(self, state: Dict[str, Any]) -> bool:
        """Restore simulator state from dictionary.
        
        Args:
            state: State dictionary to restore
            
        Returns:
            True if state was successfully restored
        """
        try:
            # Restore buffer state
            if "buffer_state" in state:
                self.buffer.restore_state(state["buffer_state"])
            
            # Restore mode state
            if "mode_state" in state:
                self.mode_manager.restore_state(state["mode_state"])
            
            # Restore other state
            self.last_command = state.get("last_command", "")
            self.command_count = state.get("command_count", 0)
            
            # Restore display settings
            display_settings = state.get("display_settings", {})
            self.display_width = display_settings.get("width", self.display_width)
            self.display_height = display_settings.get("height", self.display_height)
            self.show_line_numbers = display_settings.get("line_numbers", self.show_line_numbers)
            self.highlight_cursor = display_settings.get("highlight_cursor", self.highlight_cursor)
            
            # Recreate command processor with restored components
            self.command_processor = VimCommandProcessor(self.buffer, self.mode_manager)
            
            return True
            
        except Exception as e:
            # If restoration fails, reset to clean state
            self.reset()
            return False
    
    def get_command_help(self, command: str = None) -> Dict[str, str]:
        """Get help information for commands.
        
        Args:
            command: Specific command to get help for (all if None)
            
        Returns:
            Dictionary mapping commands to descriptions
        """
        if command:
            # Get help for specific command
            available_commands = self.mode_manager.get_available_commands()
            return {command: available_commands.get(command, "Unknown command")}
        else:
            # Get all available commands for current mode
            return self.mode_manager.get_available_commands()
    
    def get_mode_help(self) -> str:
        """Get help text for current mode.
        
        Returns:
            Help text describing current mode
        """
        return self.mode_manager.get_mode_help_text()
    
    def execute_command_sequence(self, commands: List[str]) -> List[SimulatorResponse]:
        """Execute a sequence of commands.
        
        Args:
            commands: List of commands to execute
            
        Returns:
            List of responses for each command
        """
        responses = []
        
        for command in commands:
            response = self.process_input(command)
            responses.append(response)
            
            # Stop if any command fails in learning mode
            if self.learning_mode and not response.success:
                break
        
        return responses
    
    def validate_command_sequence(self, commands: List[str]) -> Tuple[bool, str]:
        """Validate a sequence of commands without executing them.
        
        Args:
            commands: List of commands to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Create a temporary simulator state
        original_state = self.get_current_state()
        
        try:
            # Try executing commands
            for command in commands:
                result = self.command_processor.process_key(command)
                if not result.success:
                    return False, f"Invalid command '{command}': {result.error}"
            
            return True, "Command sequence is valid"
            
        finally:
            # Restore original state
            self.restore_state(original_state)
    
    def get_learning_feedback(self) -> Dict[str, Any]:
        """Get learning feedback based on recent commands.
        
        Returns:
            Dictionary with learning feedback and suggestions
        """
        feedback = {
            "commands_used": self.command_count,
            "current_mode": self.mode_manager.get_mode_display_name(),
            "suggestions": [],
            "mistakes": [],
            "efficiency_tips": []
        }
        
        # Add mode-specific suggestions
        if self.mode_manager.current_mode == VimMode.NORMAL:
            feedback["suggestions"].append("Try movement commands: h, j, k, l")
            feedback["suggestions"].append("Enter insert mode with: i, a, o")
        elif self.mode_manager.current_mode == VimMode.INSERT:
            feedback["suggestions"].append("Press Esc to return to normal mode")
        
        # Add efficiency tips based on command history
        recent_commands = self.command_processor.command_history[-10:]
        if recent_commands.count('h') > 3:
            feedback["efficiency_tips"].append("Consider using 'w' or 'b' for word movement")
        
        return feedback