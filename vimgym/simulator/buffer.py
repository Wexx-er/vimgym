"""Text buffer simulation for VimGym."""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union
import copy


@dataclass
class BufferState:
    """Represents a saved state of the buffer for undo/redo."""
    lines: List[str]
    cursor_pos: Tuple[int, int]
    description: str = ""
    
    def __post_init__(self):
        """Ensure lines are properly copied."""
        self.lines = copy.deepcopy(self.lines)


class VimBuffer:
    """Simulates a Vim text buffer with undo/redo functionality."""
    
    def __init__(self, content: str = ""):
        """Initialize buffer with optional content.
        
        Args:
            content: Initial text content
        """
        self.lines = content.split('\n') if content else ['']
        self.cursor_pos = (0, 0)  # (line, column)
        self.visual_start: Optional[Tuple[int, int]] = None
        self.visual_end: Optional[Tuple[int, int]] = None
        
        # Undo/redo stacks
        self.undo_stack: List[BufferState] = []
        self.redo_stack: List[BufferState] = []
        self.max_undo_levels = 100
        
        # Save initial state
        self.save_state("Initial buffer state")
        
        # Buffer metadata
        self.modified = False
        self.filename: Optional[str] = None
    
    def save_state(self, description: str = "") -> None:
        """Save current buffer state for undo.
        
        Args:
            description: Description of the change being made
        """
        state = BufferState(
            lines=self.lines.copy(),
            cursor_pos=self.cursor_pos,
            description=description
        )
        
        self.undo_stack.append(state)
        
        # Limit undo stack size
        if len(self.undo_stack) > self.max_undo_levels:
            self.undo_stack = self.undo_stack[-self.max_undo_levels:]
        
        # Clear redo stack when new change is made
        self.redo_stack.clear()
    
    def undo(self) -> bool:
        """Undo the last change.
        
        Returns:
            True if undo was performed, False if nothing to undo
        """
        if len(self.undo_stack) <= 1:  # Keep at least initial state
            return False
        
        # Save current state to redo stack
        current_state = BufferState(
            lines=self.lines.copy(),
            cursor_pos=self.cursor_pos,
            description="Current state"
        )
        self.redo_stack.append(current_state)
        
        # Restore previous state
        previous_state = self.undo_stack.pop()
        self.lines = previous_state.lines.copy()
        self.cursor_pos = previous_state.cursor_pos
        
        return True
    
    def redo(self) -> bool:
        """Redo the last undone change.
        
        Returns:
            True if redo was performed, False if nothing to redo
        """
        if not self.redo_stack:
            return False
        
        # Save current state to undo stack
        self.save_state("Redo operation")
        
        # Restore next state
        next_state = self.redo_stack.pop()
        self.lines = next_state.lines.copy()
        self.cursor_pos = next_state.cursor_pos
        
        return True
    
    def get_line(self, line_num: int) -> Optional[str]:
        """Get line by number.
        
        Args:
            line_num: Line number (0-indexed)
            
        Returns:
            Line content or None if line doesn't exist
        """
        if 0 <= line_num < len(self.lines):
            return self.lines[line_num]
        return None
    
    def get_line_count(self) -> int:
        """Get total number of lines.
        
        Returns:
            Number of lines in buffer
        """
        return len(self.lines)
    
    def get_content(self) -> str:
        """Get all buffer content as string.
        
        Returns:
            Complete buffer content
        """
        return '\n'.join(self.lines)
    
    def set_content(self, content: str) -> None:
        """Set buffer content.
        
        Args:
            content: New content for the buffer
        """
        self.save_state("Set buffer content")
        self.lines = content.split('\n') if content else ['']
        self.cursor_pos = (0, 0)
        self.modified = True
    
    def is_valid_position(self, line: int, col: int) -> bool:
        """Check if position is valid.
        
        Args:
            line: Line number
            col: Column number
            
        Returns:
            True if position is valid
        """
        if line < 0 or line >= len(self.lines):
            return False
        
        line_content = self.lines[line]
        return 0 <= col <= len(line_content)
    
    def clamp_position(self, line: int, col: int) -> Tuple[int, int]:
        """Clamp position to valid bounds.
        
        Args:
            line: Line number
            col: Column number
            
        Returns:
            Clamped (line, column) position
        """
        line = max(0, min(line, len(self.lines) - 1))
        line_content = self.lines[line]
        col = max(0, min(col, len(line_content)))
        return (line, col)
    
    def move_cursor(self, direction: str, count: int = 1) -> bool:
        """Move cursor in specified direction.
        
        Args:
            direction: Direction to move ('up', 'down', 'left', 'right')
            count: Number of times to move
            
        Returns:
            True if cursor was moved, False if at boundary
        """
        line, col = self.cursor_pos
        moved = False
        
        for _ in range(count):
            if direction == 'up' and line > 0:
                line -= 1
                # Clamp column to line length
                col = min(col, len(self.lines[line]))
                moved = True
            elif direction == 'down' and line < len(self.lines) - 1:
                line += 1
                # Clamp column to line length
                col = min(col, len(self.lines[line]))
                moved = True
            elif direction == 'left' and col > 0:
                col -= 1
                moved = True
            elif direction == 'right':
                line_content = self.lines[line]
                if col < len(line_content):
                    col += 1
                    moved = True
        
        self.cursor_pos = (line, col)
        return moved
    
    def move_to_position(self, line: int, col: int) -> bool:
        """Move cursor to specific position.
        
        Args:
            line: Target line number
            col: Target column number
            
        Returns:
            True if position was valid and cursor moved
        """
        if self.is_valid_position(line, col):
            self.cursor_pos = (line, col)
            return True
        return False
    
    def insert_text(self, text: str) -> bool:
        """Insert text at cursor position.
        
        Args:
            text: Text to insert
            
        Returns:
            True if text was inserted
        """
        if not text:
            return False
        
        self.save_state(f"Insert text: '{text[:20]}{'...' if len(text) > 20 else ''}'")
        
        line, col = self.cursor_pos
        current_line = self.lines[line]
        
        # Handle newlines in inserted text
        if '\n' in text:
            lines_to_insert = text.split('\n')
            
            # Split current line at cursor
            before_cursor = current_line[:col]
            after_cursor = current_line[col:]
            
            # Replace current line with first part + first inserted line
            self.lines[line] = before_cursor + lines_to_insert[0]
            
            # Insert additional lines
            for i, line_text in enumerate(lines_to_insert[1:], 1):
                self.lines.insert(line + i, line_text)
            
            # Add remaining text to last inserted line
            if len(lines_to_insert) > 1:
                last_line_idx = line + len(lines_to_insert) - 1
                self.lines[last_line_idx] += after_cursor
                
                # Update cursor position
                self.cursor_pos = (last_line_idx, len(lines_to_insert[-1]))
            else:
                self.cursor_pos = (line, col + len(text))
        else:
            # Simple text insertion
            new_line = current_line[:col] + text + current_line[col:]
            self.lines[line] = new_line
            self.cursor_pos = (line, col + len(text))
        
        self.modified = True
        return True
    
    def delete_char_at_cursor(self) -> bool:
        """Delete character at cursor position.
        
        Returns:
            True if character was deleted
        """
        line, col = self.cursor_pos
        current_line = self.lines[line]
        
        if col < len(current_line):
            self.save_state("Delete character")
            new_line = current_line[:col] + current_line[col + 1:]
            self.lines[line] = new_line
            self.modified = True
            return True
        elif line < len(self.lines) - 1:
            # At end of line, merge with next line
            self.save_state("Join lines")
            next_line = self.lines[line + 1]
            self.lines[line] = current_line + next_line
            del self.lines[line + 1]
            self.modified = True
            return True
        
        return False
    
    def delete_char_before_cursor(self) -> bool:
        """Delete character before cursor (backspace).
        
        Returns:
            True if character was deleted
        """
        line, col = self.cursor_pos
        
        if col > 0:
            self.save_state("Backspace")
            current_line = self.lines[line]
            new_line = current_line[:col - 1] + current_line[col:]
            self.lines[line] = new_line
            self.cursor_pos = (line, col - 1)
            self.modified = True
            return True
        elif line > 0:
            # At beginning of line, merge with previous line
            self.save_state("Join with previous line")
            current_line = self.lines[line]
            previous_line = self.lines[line - 1]
            
            # Move cursor to end of previous line
            new_col = len(previous_line)
            
            # Merge lines
            self.lines[line - 1] = previous_line + current_line
            del self.lines[line]
            
            self.cursor_pos = (line - 1, new_col)
            self.modified = True
            return True
        
        return False
    
    def delete_line(self, line_num: Optional[int] = None) -> bool:
        """Delete entire line.
        
        Args:
            line_num: Line to delete (current line if None)
            
        Returns:
            True if line was deleted
        """
        if line_num is None:
            line_num = self.cursor_pos[0]
        
        if 0 <= line_num < len(self.lines):
            self.save_state(f"Delete line {line_num + 1}")
            
            # Don't delete if it's the only line
            if len(self.lines) == 1:
                self.lines[0] = ''
            else:
                del self.lines[line_num]
                
                # Adjust cursor position
                if line_num >= len(self.lines):
                    line_num = len(self.lines) - 1
                
                # Clamp column to new line
                col = min(self.cursor_pos[1], len(self.lines[line_num]))
                self.cursor_pos = (line_num, col)
            
            self.modified = True
            return True
        
        return False
    
    def insert_line_below(self, content: str = "") -> bool:
        """Insert new line below current line.
        
        Args:
            content: Content for new line
            
        Returns:
            True if line was inserted
        """
        self.save_state("Insert line below")
        
        line, _ = self.cursor_pos
        self.lines.insert(line + 1, content)
        self.cursor_pos = (line + 1, len(content))
        self.modified = True
        return True
    
    def insert_line_above(self, content: str = "") -> bool:
        """Insert new line above current line.
        
        Args:
            content: Content for new line
            
        Returns:
            True if line was inserted
        """
        self.save_state("Insert line above")
        
        line, _ = self.cursor_pos
        self.lines.insert(line, content)
        self.cursor_pos = (line, len(content))
        self.modified = True
        return True
    
    def get_visual_selection(self) -> Optional[str]:
        """Get text in visual selection.
        
        Returns:
            Selected text or None if no selection
        """
        if not self.visual_start or not self.visual_end:
            return None
        
        start_line, start_col = self.visual_start
        end_line, end_col = self.visual_end
        
        # Ensure start is before end
        if (start_line > end_line or 
            (start_line == end_line and start_col > end_col)):
            start_line, start_col, end_line, end_col = end_line, end_col, start_line, start_col
        
        if start_line == end_line:
            # Single line selection
            return self.lines[start_line][start_col:end_col + 1]
        else:
            # Multi-line selection
            selected_lines = []
            
            # First line (from start_col to end)
            selected_lines.append(self.lines[start_line][start_col:])
            
            # Middle lines (complete lines)
            for line_num in range(start_line + 1, end_line):
                selected_lines.append(self.lines[line_num])
            
            # Last line (from beginning to end_col)
            selected_lines.append(self.lines[end_line][:end_col + 1])
            
            return '\n'.join(selected_lines)
    
    def start_visual_selection(self) -> None:
        """Start visual selection at cursor position."""
        self.visual_start = self.cursor_pos
        self.visual_end = self.cursor_pos
    
    def update_visual_selection(self) -> None:
        """Update visual selection end to cursor position."""
        if self.visual_start is not None:
            self.visual_end = self.cursor_pos
    
    def clear_visual_selection(self) -> None:
        """Clear visual selection."""
        self.visual_start = None
        self.visual_end = None
    
    def get_state(self) -> dict:
        """Get buffer state for persistence.
        
        Returns:
            Dictionary with buffer state
        """
        return {
            "lines": self.lines.copy(),
            "cursor_pos": self.cursor_pos,
            "visual_start": self.visual_start,
            "visual_end": self.visual_end,
            "modified": self.modified,
            "filename": self.filename
        }
    
    def restore_state(self, state: dict) -> None:
        """Restore buffer state from dictionary.
        
        Args:
            state: State dictionary to restore
        """
        self.lines = state.get("lines", ['']).copy()
        self.cursor_pos = tuple(state.get("cursor_pos", (0, 0)))
        self.visual_start = tuple(state["visual_start"]) if state.get("visual_start") else None
        self.visual_end = tuple(state["visual_end"]) if state.get("visual_end") else None
        self.modified = state.get("modified", False)
        self.filename = state.get("filename")
        
        # Ensure cursor position is valid
        self.cursor_pos = self.clamp_position(*self.cursor_pos)