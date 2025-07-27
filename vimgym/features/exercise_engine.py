"""
Exercise execution engine that integrates lessons with the Vim simulator.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
import time

from ..modules.base import Exercise, ExerciseResult, LessonSession
from ..simulator.simulator import VimSimulator, SimulatorResponse
from ..core.progress import ProgressManager


@dataclass
class ExerciseState:
    """State of an exercise in progress."""
    exercise: Exercise
    session: LessonSession
    start_time: datetime
    commands_executed: List[str]
    hints_used: int
    mistakes_made: int
    current_hint_index: int
    is_completed: bool
    
    @property
    def elapsed_time(self) -> int:
        """Get elapsed time in seconds."""
        return int((datetime.now() - self.start_time).total_seconds())


class ExerciseEngine:
    """Engine for executing and managing exercises."""
    
    def __init__(self, simulator: VimSimulator, progress_manager: ProgressManager):
        self.simulator = simulator
        self.progress_manager = progress_manager
        self.current_exercise: Optional[ExerciseState] = None
        self.validation_functions: Dict[str, Callable] = {}
        self._setup_validators()
    
    def _setup_validators(self) -> None:
        """Setup built-in validation functions."""
        self.validation_functions = {
            "commands": self._validate_commands,
            "cursor_position": self._validate_cursor_position,
            "text_content": self._validate_text_content,
            "mode_state": self._validate_mode_state,
            "custom": self._validate_custom
        }
    
    def start_exercise(self, exercise: Exercise, session: LessonSession) -> ExerciseState:
        """Start a new exercise."""
        # Reset simulator to initial state
        self.simulator.reset()
        
        # Set up initial text if provided
        if exercise.initial_text:
            self.simulator.buffer.set_content(exercise.initial_text)
        
        # Create exercise state
        self.current_exercise = ExerciseState(
            exercise=exercise,
            session=session,
            start_time=datetime.now(),
            commands_executed=[],
            hints_used=0,
            mistakes_made=0,
            current_hint_index=0,
            is_completed=False
        )
        
        return self.current_exercise
    
    def execute_command(self, command: str) -> 'ExerciseExecutionResult':
        """Execute a command in the context of current exercise."""
        if not self.current_exercise:
            return ExerciseExecutionResult(
                success=False,
                message="No active exercise",
                simulator_response=None
            )
        
        # Execute command in simulator
        simulator_response = self.simulator.process_input(command)
        
        # Track command
        self.current_exercise.commands_executed.append(command)
        
        # Check if command was expected (for real-time feedback)
        expected_so_far = self.current_exercise.exercise.expected_commands[:len(self.current_exercise.commands_executed)]
        if self.current_exercise.commands_executed != expected_so_far:
            self.current_exercise.mistakes_made += 1
        
        # Check for completion
        completion_result = self._check_completion()
        
        return ExerciseExecutionResult(
            success=True,
            message="Command executed",
            simulator_response=simulator_response,
            is_completed=completion_result.is_completed if completion_result else False,
            completion_result=completion_result
        )
    
    def _check_completion(self) -> Optional[ExerciseResult]:
        """Check if current exercise is completed."""
        if not self.current_exercise:
            return None
        
        exercise = self.current_exercise.exercise
        
        # Get current state for validation
        current_state = {
            "cursor_position": self.simulator.buffer.cursor_pos,
            "buffer_content": self.simulator.buffer.get_content(),
            "current_mode": self.simulator.buffer.mode.value,
            "commands_executed": self.current_exercise.commands_executed.copy()
        }
        
        # Use the exercise's validation method
        if exercise.validation_type in self.validation_functions:
            validator = self.validation_functions[exercise.validation_type]
            result = validator(exercise, current_state, self.current_exercise)
            
            if result.passed:
                self.current_exercise.is_completed = True
                self._record_completion(result)
            
            return result
        
        return None
    
    def _validate_commands(self, exercise: Exercise, state: Dict[str, Any], 
                          exercise_state: ExerciseState) -> ExerciseResult:
        """Validate based on command sequence."""
        executed = state["commands_executed"]
        expected = exercise.expected_commands
        
        if executed == expected:
            return ExerciseResult(
                passed=True,
                score=100,
                feedback="Perfect! Commands executed correctly.",
                time_taken=exercise_state.elapsed_time,
                hints_used=exercise_state.hints_used,
                mistakes_made=exercise_state.mistakes_made
            )
        
        # Check partial completion
        if len(executed) <= len(expected):
            correct_count = 0
            for i, cmd in enumerate(executed):
                if i < len(expected) and cmd == expected[i]:
                    correct_count += 1
                else:
                    break
            
            if correct_count == len(executed):
                # Still on track, not completed yet
                return ExerciseResult(
                    passed=False,
                    score=int((correct_count / len(expected)) * 100),
                    feedback=f"Good progress: {correct_count}/{len(expected)} commands correct",
                    time_taken=exercise_state.elapsed_time,
                    hints_used=exercise_state.hints_used,
                    mistakes_made=exercise_state.mistakes_made
                )
        
        # Commands don't match expected sequence
        return ExerciseResult(
            passed=False,
            score=0,
            feedback="Command sequence doesn't match expected pattern",
            time_taken=exercise_state.elapsed_time,
            hints_used=exercise_state.hints_used,
            mistakes_made=exercise_state.mistakes_made
        )
    
    def _validate_cursor_position(self, exercise: Exercise, state: Dict[str, Any],
                                 exercise_state: ExerciseState) -> ExerciseResult:
        """Validate based on cursor position."""
        expected_pos = exercise.validation_params.get("expected_position", (0, 0))
        actual_pos = state["cursor_position"]
        
        if actual_pos == expected_pos:
            return ExerciseResult(
                passed=True,
                score=100,
                feedback=f"Excellent! Cursor positioned correctly at {actual_pos}",
                time_taken=exercise_state.elapsed_time,
                hints_used=exercise_state.hints_used,
                mistakes_made=exercise_state.mistakes_made
            )
        else:
            # Calculate partial score based on distance
            expected_line, expected_col = expected_pos
            actual_line, actual_col = actual_pos
            
            line_diff = abs(actual_line - expected_line)
            col_diff = abs(actual_col - expected_col)
            total_diff = line_diff + col_diff
            
            # Score based on proximity (closer = higher score)
            score = max(0, 100 - (total_diff * 10))
            
            return ExerciseResult(
                passed=False,
                score=score,
                feedback=f"Cursor at {actual_pos}, expected {expected_pos}",
                time_taken=exercise_state.elapsed_time,
                hints_used=exercise_state.hints_used,
                mistakes_made=exercise_state.mistakes_made
            )
    
    def _validate_text_content(self, exercise: Exercise, state: Dict[str, Any],
                              exercise_state: ExerciseState) -> ExerciseResult:
        """Validate based on text content."""
        expected_text = exercise.validation_params.get("expected_text", "")
        actual_text = state["buffer_content"]
        
        # Normalize whitespace for comparison
        expected_normalized = expected_text.strip()
        actual_normalized = actual_text.strip()
        
        if actual_normalized == expected_normalized:
            return ExerciseResult(
                passed=True,
                score=100,
                feedback="Perfect! Text content matches expected result.",
                time_taken=exercise_state.elapsed_time,
                hints_used=exercise_state.hints_used,
                mistakes_made=exercise_state.mistakes_made
            )
        else:
            # Calculate similarity score
            similarity = self._calculate_text_similarity(expected_normalized, actual_normalized)
            score = int(similarity * 100)
            
            return ExerciseResult(
                passed=score >= 80,  # 80% similarity threshold
                score=score,
                feedback=f"Text similarity: {score}%. Expected: '{expected_normalized}', Got: '{actual_normalized}'",
                time_taken=exercise_state.elapsed_time,
                hints_used=exercise_state.hints_used,
                mistakes_made=exercise_state.mistakes_made
            )
    
    def _validate_mode_state(self, exercise: Exercise, state: Dict[str, Any],
                           exercise_state: ExerciseState) -> ExerciseResult:
        """Validate based on Vim mode."""
        expected_mode = exercise.validation_params.get("expected_mode", "normal")
        actual_mode = state["current_mode"]
        
        if actual_mode.lower() == expected_mode.lower():
            return ExerciseResult(
                passed=True,
                score=100,
                feedback=f"Correct! You're in {actual_mode} mode.",
                time_taken=exercise_state.elapsed_time,
                hints_used=exercise_state.hints_used,
                mistakes_made=exercise_state.mistakes_made
            )
        else:
            return ExerciseResult(
                passed=False,
                score=0,
                feedback=f"Wrong mode. Expected {expected_mode}, but you're in {actual_mode}",
                time_taken=exercise_state.elapsed_time,
                hints_used=exercise_state.hints_used,
                mistakes_made=exercise_state.mistakes_made
            )
    
    def _validate_custom(self, exercise: Exercise, state: Dict[str, Any],
                        exercise_state: ExerciseState) -> ExerciseResult:
        """Custom validation logic."""
        # This would be implemented for special exercises with custom validation
        return ExerciseResult(
            passed=True,
            score=100,
            feedback="Custom validation passed",
            time_taken=exercise_state.elapsed_time,
            hints_used=exercise_state.hints_used,
            mistakes_made=exercise_state.mistakes_made
        )
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts (simple implementation)."""
        if not text1 and not text2:
            return 1.0
        if not text1 or not text2:
            return 0.0
        
        # Simple character-based similarity
        max_len = max(len(text1), len(text2))
        common_chars = sum(1 for a, b in zip(text1, text2) if a == b)
        
        return common_chars / max_len
    
    def get_hint(self) -> Optional[str]:
        """Get next hint for current exercise."""
        if not self.current_exercise:
            return None
        
        hints = self.current_exercise.exercise.hints
        if self.current_exercise.current_hint_index < len(hints):
            hint = hints[self.current_exercise.current_hint_index]
            self.current_exercise.current_hint_index += 1
            self.current_exercise.hints_used += 1
            return hint
        
        return None
    
    def skip_exercise(self, reason: str = "skipped") -> ExerciseResult:
        """Skip the current exercise."""
        if not self.current_exercise:
            return ExerciseResult(False, 0, "No active exercise")
        
        result = ExerciseResult(
            passed=False,
            score=0,
            feedback=f"Exercise skipped: {reason}",
            time_taken=self.current_exercise.elapsed_time,
            hints_used=self.current_exercise.hints_used,
            mistakes_made=self.current_exercise.mistakes_made
        )
        
        self._record_completion(result)
        return result
    
    def _record_completion(self, result: ExerciseResult) -> None:
        """Record exercise completion in progress manager."""
        if not self.current_exercise:
            return
        
        # Update lesson session with result
        self.current_exercise.session.exercise_results.append(result)
        
        # Record in progress manager if available
        # This would integrate with the progress tracking system
        
    def get_exercise_stats(self) -> Optional[Dict[str, Any]]:
        """Get current exercise statistics."""
        if not self.current_exercise:
            return None
        
        return {
            "exercise_id": self.current_exercise.exercise.id,
            "elapsed_time": self.current_exercise.elapsed_time,
            "commands_executed": len(self.current_exercise.commands_executed),
            "expected_commands": len(self.current_exercise.exercise.expected_commands),
            "hints_used": self.current_exercise.hints_used,
            "hints_available": len(self.current_exercise.exercise.hints),
            "mistakes_made": self.current_exercise.mistakes_made,
            "progress": len(self.current_exercise.commands_executed) / len(self.current_exercise.exercise.expected_commands) if self.current_exercise.exercise.expected_commands else 0
        }


@dataclass
class ExerciseExecutionResult:
    """Result of executing a command during an exercise."""
    success: bool
    message: str
    simulator_response: Optional[SimulatorResponse]
    is_completed: bool = False
    completion_result: Optional[ExerciseResult] = None


class ExerciseHintSystem:
    """Advanced hint system for exercises."""
    
    def __init__(self):
        self.context_hints: Dict[str, List[str]] = {
            "wrong_mode": [
                "You might be in the wrong mode. Press Escape to return to Normal mode.",
                "Check the mode indicator at the bottom of the screen.",
                "Remember: Normal mode is for commands, Insert mode is for typing."
            ],
            "wrong_direction": [
                "Try moving in a different direction.",
                "Remember: h=left, j=down, k=up, l=right",
                "Double-check which direction you need to go."
            ],
            "command_sequence": [
                "Make sure you're following the exact command sequence.",
                "Commands in Vim are order-sensitive.",
                "Try starting over if you've made an error."
            ],
            "case_sensitive": [
                "Vim commands are case-sensitive. Check your capitalization.",
                "Uppercase and lowercase commands often do different things.",
                "Make sure you're using the right case for each command."
            ]
        }
    
    def get_contextual_hint(self, exercise_state: ExerciseState, 
                           last_command: str) -> Optional[str]:
        """Get a contextual hint based on the current situation."""
        if not exercise_state:
            return None
        
        executed = exercise_state.commands_executed
        expected = exercise_state.exercise.expected_commands
        
        if not executed:
            return "Start by pressing the first command in the sequence."
        
        # Check if last command was wrong
        if len(executed) <= len(expected):
            expected_cmd = expected[len(executed) - 1]
            if executed[-1] != expected_cmd:
                # Wrong command
                if expected_cmd.lower() == executed[-1].lower():
                    return self._get_random_hint("case_sensitive")
                elif expected_cmd in "hjkl" and executed[-1] in "hjkl":
                    return self._get_random_hint("wrong_direction")
                else:
                    return f"Expected '{expected_cmd}' but got '{executed[-1]}'. Try again!"
        
        return None
    
    def _get_random_hint(self, category: str) -> str:
        """Get a random hint from a category."""
        import random
        hints = self.context_hints.get(category, ["Keep trying!"])
        return random.choice(hints)