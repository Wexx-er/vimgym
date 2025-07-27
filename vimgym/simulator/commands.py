"""Vim command processing for VimGym simulator."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import re

from .modes import VimMode, ModeManager
from .buffer import VimBuffer


class CommandType(Enum):
    """Types of Vim commands."""
    MOVEMENT = "movement"
    EDITING = "editing"
    MODE_SWITCH = "mode_switch"
    VISUAL = "visual"
    SEARCH = "search"
    EX_COMMAND = "ex_command"
    MACRO = "macro"


@dataclass
class CommandResult:
    """Result of command execution."""
    success: bool
    message: str = ""
    mode_changed: bool = False
    new_mode: Optional[VimMode] = None
    cursor_moved: bool = False
    buffer_modified: bool = False
    error: Optional[str] = None


class VimCommandProcessor:
    """Processes and executes Vim commands."""
    
    def __init__(self, buffer: VimBuffer, mode_manager: ModeManager):
        """Initialize command processor.
        
        Args:
            buffer: Text buffer instance
            mode_manager: Mode manager instance
        """
        self.buffer = buffer
        self.mode_manager = mode_manager
        self.command_history: List[str] = []
        self.last_command = ""
        self.repeat_count = 1
        self.pending_operator: Optional[str] = None
        
        # Build command maps
        self.normal_commands = self._build_normal_command_map()
        self.movement_commands = self._build_movement_command_map()
        self.text_objects = self._build_text_objects()
        
        # Command state
        self.awaiting_motion = False
        self.search_pattern = ""
        self.command_buffer = ""
    
    def _build_normal_command_map(self) -> Dict[str, Callable]:
        """Build map of normal mode commands."""
        return {
            # Movement commands
            'h': lambda: self._move_cursor('left'),
            'j': lambda: self._move_cursor('down'),
            'k': lambda: self._move_cursor('up'),
            'l': lambda: self._move_cursor('right'),
            
            # Word movement
            'w': lambda: self._move_word('forward'),
            'b': lambda: self._move_word('backward'),
            'e': lambda: self._move_word('end'),
            'W': lambda: self._move_WORD('forward'),
            'B': lambda: self._move_WORD('backward'),
            'E': lambda: self._move_WORD('end'),
            
            # Line movement
            '0': lambda: self._move_to_line_start(),
            '^': lambda: self._move_to_first_nonblank(),
            '$': lambda: self._move_to_line_end(),
            'g_': lambda: self._move_to_last_nonblank(),
            
            # File movement
            'gg': lambda: self._go_to_line(1),
            'G': lambda: self._go_to_line(-1),  # Last line
            
            # Editing commands
            'x': lambda: self._delete_char(),
            'X': lambda: self._delete_char_before(),
            'dd': lambda: self._delete_line(),
            'D': lambda: self._delete_to_end_of_line(),
            'yy': lambda: self._yank_line(),
            'Y': lambda: self._yank_to_end_of_line(),
            'p': lambda: self._paste_after(),
            'P': lambda: self._paste_before(),
            
            # Change commands
            'cc': lambda: self._change_line(),
            'C': lambda: self._change_to_end_of_line(),
            'cw': lambda: self._change_word(),
            's': lambda: self._substitute_char(),
            'S': lambda: self._substitute_line(),
            'r': lambda: self._replace_char_mode(),
            
            # Undo/redo
            'u': lambda: self._undo(),
            '\x12': lambda: self._redo(),  # Ctrl-R
            
            # Insert mode commands
            'i': lambda: self._insert_before(),
            'I': lambda: self._insert_at_line_start(),
            'a': lambda: self._append_after(),
            'A': lambda: self._append_at_line_end(),
            'o': lambda: self._open_line_below(),
            'O': lambda: self._open_line_above(),
            
            # Visual mode commands
            'v': lambda: self._visual_char(),
            'V': lambda: self._visual_line(),
            '\x16': lambda: self._visual_block(),  # Ctrl-V
            
            # Search commands
            '/': lambda: self._search_forward(),
            '?': lambda: self._search_backward(),
            'n': lambda: self._repeat_search(),
            'N': lambda: self._repeat_search_reverse(),
            '*': lambda: self._search_word_forward(),
            '#': lambda: self._search_word_backward(),
        }
    
    def _build_movement_command_map(self) -> Dict[str, Callable]:
        """Build map of movement commands that can be used with operators."""
        return {
            'h': lambda: self._move_cursor('left'),
            'j': lambda: self._move_cursor('down'),
            'k': lambda: self._move_cursor('up'),
            'l': lambda: self._move_cursor('right'),
            'w': lambda: self._move_word('forward'),
            'b': lambda: self._move_word('backward'),
            'e': lambda: self._move_word('end'),
            '0': lambda: self._move_to_line_start(),
            '^': lambda: self._move_to_first_nonblank(),
            '$': lambda: self._move_to_line_end(),
        }
    
    def _build_text_objects(self) -> Dict[str, Callable]:
        """Build map of text objects."""
        return {
            'iw': lambda: self._text_object_inner_word(),
            'aw': lambda: self._text_object_around_word(),
            'ip': lambda: self._text_object_inner_paragraph(),
            'ap': lambda: self._text_object_around_paragraph(),
            'i"': lambda: self._text_object_inner_quotes('"'),
            'a"': lambda: self._text_object_around_quotes('"'),
            "i'": lambda: self._text_object_inner_quotes("'"),
            "a'": lambda: self._text_object_around_quotes("'"),
            'i(': lambda: self._text_object_inner_parens(),
            'a(': lambda: self._text_object_around_parens(),
        }
    
    def process_key(self, key: str) -> CommandResult:
        """Process a single keypress.
        
        Args:
            key: Key that was pressed
            
        Returns:
            CommandResult with execution details
        """
        # Handle repeat count
        if key.isdigit() and key != '0' and not self.command_buffer:
            self.repeat_count = self.repeat_count * 10 + int(key)
            return CommandResult(success=True, message=f"Count: {self.repeat_count}")
        
        # Handle mode-specific processing
        if self.mode_manager.current_mode == VimMode.NORMAL:
            return self._process_normal_mode_key(key)
        elif self.mode_manager.current_mode == VimMode.INSERT:
            return self._process_insert_mode_key(key)
        elif self.mode_manager.is_visual_mode():
            return self._process_visual_mode_key(key)
        elif self.mode_manager.current_mode == VimMode.COMMAND:
            return self._process_command_mode_key(key)
        else:
            return CommandResult(success=False, error=f"Mode {self.mode_manager.current_mode} not implemented")
    
    def _process_normal_mode_key(self, key: str) -> CommandResult:
        """Process key in normal mode."""
        # Check for mode switch first
        if self.mode_manager.process_command(key):
            return CommandResult(
                success=True,
                mode_changed=True,
                new_mode=self.mode_manager.current_mode,
                message=f"Switched to {self.mode_manager.get_mode_display_name()}"
            )
        
        # Handle command buffer (for multi-character commands)
        self.command_buffer += key
        
        # Check for complete command
        if self.command_buffer in self.normal_commands:
            command = self.normal_commands[self.command_buffer]
            result = self._execute_command(command, self.command_buffer)
            self._reset_command_state()
            return result
        
        # Check for partial command
        if any(cmd.startswith(self.command_buffer) for cmd in self.normal_commands):
            return CommandResult(success=True, message=f"Partial command: {self.command_buffer}")
        
        # Invalid command
        self._reset_command_state()
        return CommandResult(success=False, error=f"Unknown command: {key}")
    
    def _process_insert_mode_key(self, key: str) -> CommandResult:
        """Process key in insert mode."""
        # Check for escape or Ctrl-C
        if key in ['\x1b', '\x03']:  # Escape or Ctrl-C
            self.mode_manager.switch_mode(VimMode.NORMAL)
            return CommandResult(
                success=True,
                mode_changed=True,
                new_mode=VimMode.NORMAL,
                message="Returned to NORMAL mode"
            )
        
        # Handle special characters
        if key == '\r' or key == '\n':  # Enter
            self.buffer.insert_text('\n')
            return CommandResult(success=True, buffer_modified=True, message="New line")
        elif key == '\x08' or key == '\x7f':  # Backspace
            success = self.buffer.delete_char_before_cursor()
            return CommandResult(success=success, buffer_modified=success, message="Backspace")
        elif len(key) == 1 and key.isprintable():
            # Regular character
            self.buffer.insert_text(key)
            return CommandResult(success=True, buffer_modified=True, message=f"Inserted: {key}")
        
        return CommandResult(success=False, error=f"Cannot handle key in insert mode: {repr(key)}")
    
    def _process_visual_mode_key(self, key: str) -> CommandResult:
        """Process key in visual mode."""
        # Escape - return to normal mode
        if key in ['\x1b', '\x03']:
            self.buffer.clear_visual_selection()
            self.mode_manager.switch_mode(VimMode.NORMAL)
            return CommandResult(
                success=True,
                mode_changed=True,
                new_mode=VimMode.NORMAL,
                message="Exited visual mode"
            )
        
        # Movement commands - extend selection
        if key in self.movement_commands:
            old_pos = self.buffer.cursor_pos
            result = self._execute_command(self.movement_commands[key], key)
            if result.success:
                self.buffer.update_visual_selection()
                return CommandResult(
                    success=True,
                    cursor_moved=True,
                    message=f"Extended selection with {key}"
                )
        
        # Operations on selection
        if key == 'd':
            # Delete selection
            selection = self.buffer.get_visual_selection()
            if selection:
                # TODO: Implement visual deletion
                self.buffer.clear_visual_selection()
                self.mode_manager.switch_mode(VimMode.NORMAL)
                return CommandResult(
                    success=True,
                    buffer_modified=True,
                    mode_changed=True,
                    new_mode=VimMode.NORMAL,
                    message="Deleted selection"
                )
        
        return CommandResult(success=False, error=f"Command {key} not implemented in visual mode")
    
    def _process_command_mode_key(self, key: str) -> CommandResult:
        """Process key in command mode."""
        # Escape - cancel command
        if key in ['\x1b', '\x03']:
            self.command_buffer = ""
            self.mode_manager.switch_mode(VimMode.NORMAL)
            return CommandResult(
                success=True,
                mode_changed=True,
                new_mode=VimMode.NORMAL,
                message="Cancelled command"
            )
        
        # Enter - execute command
        if key in ['\r', '\n']:
            command = self.command_buffer
            self.command_buffer = ""
            self.mode_manager.switch_mode(VimMode.NORMAL)
            
            # Execute the command
            result = self._execute_ex_command(command)
            result.mode_changed = True
            result.new_mode = VimMode.NORMAL
            return result
        
        # Backspace
        if key in ['\x08', '\x7f']:
            if self.command_buffer:
                self.command_buffer = self.command_buffer[:-1]
            return CommandResult(success=True, message=f"Command: {self.command_buffer}")
        
        # Regular character
        if len(key) == 1 and key.isprintable():
            self.command_buffer += key
            return CommandResult(success=True, message=f"Command: {self.command_buffer}")
        
        return CommandResult(success=False, error=f"Cannot handle key in command mode: {repr(key)}")
    
    def _execute_command(self, command: Callable, command_str: str) -> CommandResult:
        """Execute a command with repeat count."""
        try:
            original_pos = self.buffer.cursor_pos
            
            # Execute command repeat_count times
            for _ in range(self.repeat_count):
                command()
            
            # Record command in history
            self.command_history.append(command_str)
            self.last_command = command_str
            
            # Check if cursor moved
            cursor_moved = self.buffer.cursor_pos != original_pos
            
            return CommandResult(
                success=True,
                cursor_moved=cursor_moved,
                message=f"Executed {command_str}" + (f" {self.repeat_count} times" if self.repeat_count > 1 else "")
            )
        except Exception as e:
            return CommandResult(success=False, error=str(e))
    
    def _execute_ex_command(self, command: str) -> CommandResult:
        """Execute an Ex command."""
        if not command:
            return CommandResult(success=True, message="Empty command")
        
        # Basic Ex commands
        if command == 'q':
            return CommandResult(success=True, message="Quit (simulated)")
        elif command == 'w':
            return CommandResult(success=True, message="Write (simulated)")
        elif command == 'wq':
            return CommandResult(success=True, message="Write and quit (simulated)")
        elif command.startswith('s/'):
            # Basic substitute command
            return self._execute_substitute(command)
        else:
            return CommandResult(success=False, error=f"Unknown command: :{command}")
    
    def _execute_substitute(self, command: str) -> CommandResult:
        """Execute substitute command."""
        # Basic s/old/new/ parsing
        match = re.match(r's/([^/]*)/([^/]*)/([g]?)', command)
        if not match:
            return CommandResult(success=False, error="Invalid substitute syntax")
        
        old_text, new_text, flags = match.groups()
        
        # For now, just simulate
        return CommandResult(
            success=True,
            message=f"Substitute '{old_text}' with '{new_text}' (simulated)"
        )
    
    def _reset_command_state(self) -> None:
        """Reset command processing state."""
        self.repeat_count = 1
        self.command_buffer = ""
        self.pending_operator = None
        self.awaiting_motion = False
    
    # Movement command implementations
    def _move_cursor(self, direction: str) -> bool:
        """Move cursor in direction."""
        return self.buffer.move_cursor(direction, self.repeat_count)
    
    def _move_word(self, direction: str) -> bool:
        """Move by word."""
        # Simplified word movement
        for _ in range(self.repeat_count):
            if direction == 'forward':
                self._move_to_next_word_start()
            elif direction == 'backward':
                self._move_to_prev_word_start()
            elif direction == 'end':
                self._move_to_word_end()
        return True
    
    def _move_WORD(self, direction: str) -> bool:
        """Move by WORD (whitespace-separated)."""
        # Simplified WORD movement
        return self._move_word(direction)
    
    def _move_to_next_word_start(self) -> None:
        """Move to start of next word."""
        line, col = self.buffer.cursor_pos
        current_line = self.buffer.get_line(line)
        
        if current_line and col < len(current_line):
            # Find next word boundary
            while col < len(current_line) and not current_line[col].isalnum():
                col += 1
            while col < len(current_line) and current_line[col].isalnum():
                col += 1
            while col < len(current_line) and not current_line[col].isalnum():
                col += 1
        
        if col >= len(current_line or ''):
            # Move to next line
            if line < self.buffer.get_line_count() - 1:
                self.buffer.move_to_position(line + 1, 0)
            return
        
        self.buffer.move_to_position(line, col)
    
    def _move_to_prev_word_start(self) -> None:
        """Move to start of previous word."""
        line, col = self.buffer.cursor_pos
        
        if col > 0:
            col -= 1
            current_line = self.buffer.get_line(line)
            
            # Move back to word start
            if current_line:
                while col > 0 and not current_line[col].isalnum():
                    col -= 1
                while col > 0 and current_line[col - 1].isalnum():
                    col -= 1
        elif line > 0:
            # Move to end of previous line
            prev_line = self.buffer.get_line(line - 1)
            self.buffer.move_to_position(line - 1, len(prev_line or ''))
            return
        
        self.buffer.move_to_position(line, col)
    
    def _move_to_word_end(self) -> None:
        """Move to end of current/next word."""
        line, col = self.buffer.cursor_pos
        current_line = self.buffer.get_line(line)
        
        if current_line and col < len(current_line):
            # Move to end of current or next word
            if not current_line[col].isalnum():
                while col < len(current_line) and not current_line[col].isalnum():
                    col += 1
            
            while col < len(current_line) and current_line[col].isalnum():
                col += 1
            
            if col > 0:
                col -= 1
        
        self.buffer.move_to_position(line, col)
    
    def _move_to_line_start(self) -> bool:
        """Move to start of line."""
        line, _ = self.buffer.cursor_pos
        return self.buffer.move_to_position(line, 0)
    
    def _move_to_first_nonblank(self) -> bool:
        """Move to first non-blank character of line."""
        line, _ = self.buffer.cursor_pos
        current_line = self.buffer.get_line(line) or ''
        
        col = 0
        while col < len(current_line) and current_line[col].isspace():
            col += 1
        
        return self.buffer.move_to_position(line, col)
    
    def _move_to_line_end(self) -> bool:
        """Move to end of line."""
        line, _ = self.buffer.cursor_pos
        current_line = self.buffer.get_line(line) or ''
        return self.buffer.move_to_position(line, max(0, len(current_line) - 1))
    
    def _move_to_last_nonblank(self) -> bool:
        """Move to last non-blank character of line."""
        line, _ = self.buffer.cursor_pos
        current_line = self.buffer.get_line(line) or ''
        
        col = len(current_line) - 1
        while col >= 0 and current_line[col].isspace():
            col -= 1
        
        return self.buffer.move_to_position(line, max(0, col))
    
    def _go_to_line(self, line_num: int) -> bool:
        """Go to specific line number."""
        if line_num == -1:  # Last line
            line_num = self.buffer.get_line_count()
        
        # Convert to 0-indexed
        target_line = max(0, min(line_num - 1, self.buffer.get_line_count() - 1))
        return self.buffer.move_to_position(target_line, 0)
    
    # Editing command implementations
    def _delete_char(self) -> bool:
        """Delete character at cursor."""
        return self.buffer.delete_char_at_cursor()
    
    def _delete_char_before(self) -> bool:
        """Delete character before cursor."""
        return self.buffer.delete_char_before_cursor()
    
    def _delete_line(self) -> bool:
        """Delete current line."""
        return self.buffer.delete_line()
    
    def _delete_to_end_of_line(self) -> bool:
        """Delete to end of line."""
        # TODO: Implement
        return True
    
    def _yank_line(self) -> bool:
        """Yank (copy) current line."""
        # TODO: Implement with register support
        return True
    
    def _yank_to_end_of_line(self) -> bool:
        """Yank to end of line."""
        # TODO: Implement
        return True
    
    def _paste_after(self) -> bool:
        """Paste after cursor."""
        # TODO: Implement with register support
        return True
    
    def _paste_before(self) -> bool:
        """Paste before cursor."""
        # TODO: Implement with register support
        return True
    
    def _undo(self) -> bool:
        """Undo last change."""
        return self.buffer.undo()
    
    def _redo(self) -> bool:
        """Redo last undone change."""
        return self.buffer.redo()
    
    # Insert mode commands
    def _insert_before(self) -> None:
        """Enter insert mode before cursor."""
        self.mode_manager.switch_mode(VimMode.INSERT)
    
    def _insert_at_line_start(self) -> None:
        """Enter insert mode at start of line."""
        self._move_to_first_nonblank()
        self.mode_manager.switch_mode(VimMode.INSERT)
    
    def _append_after(self) -> None:
        """Enter insert mode after cursor."""
        self.buffer.move_cursor('right')
        self.mode_manager.switch_mode(VimMode.INSERT)
    
    def _append_at_line_end(self) -> None:
        """Enter insert mode at end of line."""
        self._move_to_line_end()
        self.buffer.move_cursor('right')
        self.mode_manager.switch_mode(VimMode.INSERT)
    
    def _open_line_below(self) -> None:
        """Open new line below and enter insert mode."""
        self.buffer.insert_line_below()
        self.mode_manager.switch_mode(VimMode.INSERT)
    
    def _open_line_above(self) -> None:
        """Open new line above and enter insert mode."""
        self.buffer.insert_line_above()
        self.mode_manager.switch_mode(VimMode.INSERT)
    
    # Change commands (TODO: Implement properly)
    def _change_line(self) -> None:
        """Change entire line."""
        self.buffer.delete_line()
        self.buffer.insert_line_below()
        self.mode_manager.switch_mode(VimMode.INSERT)
    
    def _change_to_end_of_line(self) -> None:
        """Change to end of line."""
        # TODO: Implement
        self.mode_manager.switch_mode(VimMode.INSERT)
    
    def _change_word(self) -> None:
        """Change word."""
        # TODO: Implement
        self.mode_manager.switch_mode(VimMode.INSERT)
    
    def _substitute_char(self) -> None:
        """Substitute character."""
        self.buffer.delete_char_at_cursor()
        self.mode_manager.switch_mode(VimMode.INSERT)
    
    def _substitute_line(self) -> None:
        """Substitute entire line."""
        line, _ = self.buffer.cursor_pos
        self.buffer.lines[line] = ''
        self.buffer.cursor_pos = (line, 0)
        self.mode_manager.switch_mode(VimMode.INSERT)
    
    def _replace_char_mode(self) -> None:
        """Enter replace mode."""
        self.mode_manager.switch_mode(VimMode.REPLACE)
    
    # Visual mode commands
    def _visual_char(self) -> None:
        """Enter character visual mode."""
        self.buffer.start_visual_selection()
        self.mode_manager.switch_mode(VimMode.VISUAL)
    
    def _visual_line(self) -> None:
        """Enter line visual mode."""
        self.buffer.start_visual_selection()
        self.mode_manager.switch_mode(VimMode.VISUAL_LINE)
    
    def _visual_block(self) -> None:
        """Enter block visual mode."""
        self.buffer.start_visual_selection()
        self.mode_manager.switch_mode(VimMode.VISUAL_BLOCK)
    
    # Search commands (TODO: Implement)
    def _search_forward(self) -> None:
        """Start forward search."""
        self.mode_manager.switch_mode(VimMode.COMMAND)
        self.command_buffer = ""
    
    def _search_backward(self) -> None:
        """Start backward search."""
        self.mode_manager.switch_mode(VimMode.COMMAND)
        self.command_buffer = ""
    
    def _repeat_search(self) -> None:
        """Repeat last search."""
        pass
    
    def _repeat_search_reverse(self) -> None:
        """Repeat last search in reverse direction."""
        pass
    
    def _search_word_forward(self) -> None:
        """Search for word under cursor forward."""
        pass
    
    def _search_word_backward(self) -> None:
        """Search for word under cursor backward."""
        pass
    
    # Text object implementations (TODO)
    def _text_object_inner_word(self) -> None:
        """Inner word text object."""
        pass
    
    def _text_object_around_word(self) -> None:
        """Around word text object."""
        pass
    
    def _text_object_inner_paragraph(self) -> None:
        """Inner paragraph text object."""
        pass
    
    def _text_object_around_paragraph(self) -> None:
        """Around paragraph text object."""
        pass
    
    def _text_object_inner_quotes(self, quote_char: str) -> None:
        """Inner quotes text object."""
        pass
    
    def _text_object_around_quotes(self, quote_char: str) -> None:
        """Around quotes text object."""
        pass
    
    def _text_object_inner_parens(self) -> None:
        """Inner parentheses text object."""
        pass
    
    def _text_object_around_parens(self) -> None:
        """Around parentheses text object."""
        pass