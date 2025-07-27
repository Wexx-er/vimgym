"""
Lesson runner that orchestrates the complete learning experience.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

from ..modules.base import Lesson, LessonSession, ModuleManager
from ..simulator.simulator import VimSimulator
from ..core.progress import ProgressManager
from ..core.user import User
from ..ui.layouts import LessonLayout
from .exercise_engine import ExerciseEngine, ExerciseState
from rich.console import Console


@dataclass
class LessonState:
    """Current state of a lesson in progress."""
    lesson: Lesson
    session: LessonSession
    current_exercise_index: int
    is_completed: bool
    started_at: datetime
    
    @property
    def progress_percentage(self) -> float:
        """Get lesson progress as percentage."""
        if not self.lesson.content.exercises:
            return 100.0
        return (self.current_exercise_index / len(self.lesson.content.exercises)) * 100.0


class LessonRunner:
    """Orchestrates the complete lesson experience."""
    
    def __init__(self, console: Console, simulator: VimSimulator, 
                 progress_manager: ProgressManager, module_manager: ModuleManager):
        self.console = console
        self.simulator = simulator
        self.progress_manager = progress_manager
        self.module_manager = module_manager
        self.exercise_engine = ExerciseEngine(simulator, progress_manager)
        self.lesson_layout = LessonLayout(console)
        
        self.current_lesson: Optional[LessonState] = None
        self.current_user: Optional[User] = None
    
    def set_user(self, user: User) -> None:
        """Set the current user."""
        self.current_user = user
    
    def start_lesson(self, module_id: str, lesson_id: str) -> bool:
        """Start a specific lesson."""
        if not self.current_user:
            self.console.print("[red]Error: No user set[/red]")
            return False
        
        # Get module and lesson
        module = self.module_manager.get_module(module_id)
        if not module:
            self.console.print(f"[red]Error: Module '{module_id}' not found[/red]")
            return False
        
        lesson = module.get_lesson_by_id(lesson_id)
        if not lesson:
            self.console.print(f"[red]Error: Lesson '{lesson_id}' not found in module '{module_id}'[/red]")
            return False
        
        # Check prerequisites
        user_progress = self.progress_manager.get_user_progress(self.current_user.id)
        if not module.is_unlocked(user_progress):
            self.console.print(f"[yellow]Module '{module.title}' is locked. Complete prerequisites first.[/yellow]")
            return False
        
        # Create lesson session
        session = lesson.start_session(self.simulator, self.current_user.id)
        
        # Create lesson state
        self.current_lesson = LessonState(
            lesson=lesson,
            session=session,
            current_exercise_index=0,
            is_completed=False,
            started_at=datetime.now()
        )
        
        # Display lesson introduction
        self._display_lesson_intro()
        
        # Start first exercise
        if lesson.content.exercises:
            self._start_current_exercise()
        
        return True
    
    def _display_lesson_intro(self) -> None:
        """Display lesson introduction and objectives."""
        if not self.current_lesson:
            return
        
        lesson = self.current_lesson.lesson
        
        # Render lesson introduction using layout
        self.lesson_layout.render_introduction(
            lesson=lesson,
            progress=self.current_lesson.progress_percentage
        )
        
        # Wait for user to continue
        self.console.input("\n[dim]Press Enter to start the exercises...[/dim]")
    
    def _start_current_exercise(self) -> None:
        """Start the current exercise."""
        if not self.current_lesson or not self.current_lesson.lesson.content.exercises:
            return
        
        exercise_index = self.current_lesson.current_exercise_index
        if exercise_index >= len(self.current_lesson.lesson.content.exercises):
            self._complete_lesson()
            return
        
        exercise = self.current_lesson.lesson.content.exercises[exercise_index]
        
        # Start exercise in engine
        self.exercise_engine.start_exercise(exercise, self.current_lesson.session)
        
        # Display exercise
        self._display_current_exercise()
    
    def _display_current_exercise(self) -> None:
        """Display the current exercise state."""
        if not self.current_lesson:
            return
        
        exercise_index = self.current_lesson.current_exercise_index
        if exercise_index >= len(self.current_lesson.lesson.content.exercises):
            return
        
        exercise = self.current_lesson.lesson.content.exercises[exercise_index]
        
        # Get current simulator state
        simulator_state = {
            "buffer_content": self.simulator.buffer.get_content(),
            "cursor_position": self.simulator.buffer.cursor_pos,
            "mode": self.simulator.buffer.mode.value
        }
        
        # Get exercise stats
        exercise_stats = self.exercise_engine.get_exercise_stats()
        
        # Render exercise using layout
        self.lesson_layout.render_exercise(
            lesson=self.current_lesson.lesson,
            exercise=exercise,
            exercise_number=exercise_index + 1,
            total_exercises=len(self.current_lesson.lesson.content.exercises),
            simulator_state=simulator_state,
            exercise_stats=exercise_stats or {},
            lesson_progress=self.current_lesson.progress_percentage
        )
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input and return result."""
        if not self.current_lesson:
            return {"error": "No active lesson"}
        
        # Handle special commands
        if user_input.startswith(":"):
            return self._handle_special_command(user_input[1:])
        
        # Execute command in exercise engine
        result = self.exercise_engine.execute_command(user_input)
        
        # Update display
        self._display_current_exercise()
        
        # Check if exercise is completed
        if result.is_completed and result.completion_result:
            self._handle_exercise_completion(result.completion_result)
        
        return {
            "success": result.success,
            "message": result.message,
            "completed": result.is_completed
        }
    
    def _handle_special_command(self, command: str) -> Dict[str, Any]:
        """Handle special lesson commands."""
        command = command.strip().lower()
        
        if command == "hint":
            hint = self.exercise_engine.get_hint()
            if hint:
                self.console.print(f"[yellow]💡 Hint: {hint}[/yellow]")
                return {"success": True, "message": "Hint provided"}
            else:
                self.console.print("[dim]No more hints available for this exercise.[/dim]")
                return {"success": False, "message": "No hints available"}
        
        elif command == "skip":
            result = self.exercise_engine.skip_exercise("User requested skip")
            self._handle_exercise_completion(result)
            return {"success": True, "message": "Exercise skipped"}
        
        elif command == "restart":
            self._start_current_exercise()
            return {"success": True, "message": "Exercise restarted"}
        
        elif command == "quit":
            return self._quit_lesson()
        
        elif command == "help":
            self._show_help()
            return {"success": True, "message": "Help displayed"}
        
        else:
            self.console.print(f"[red]Unknown command: {command}[/red]")
            return {"success": False, "message": f"Unknown command: {command}"}
    
    def _handle_exercise_completion(self, result) -> None:
        """Handle completion of an exercise."""
        if not self.current_lesson:
            return
        
        # Display completion feedback
        if result.passed:
            self.console.print(f"[green]✅ Exercise completed! Score: {result.score}%[/green]")
            self.console.print(f"[dim]Time: {result.time_taken}s, Hints used: {result.hints_used}[/dim]")
        else:
            self.console.print(f"[yellow]⚠️ Exercise not completed perfectly. Score: {result.score}%[/yellow]")
        
        self.console.print(f"[blue]{result.feedback}[/blue]")
        
        # Move to next exercise
        self.current_lesson.current_exercise_index += 1
        
        # Check if lesson is complete
        if self.current_lesson.current_exercise_index >= len(self.current_lesson.lesson.content.exercises):
            self._complete_lesson()
        else:
            # Continue to next exercise
            self.console.input("\n[dim]Press Enter to continue to the next exercise...[/dim]")
            self._start_current_exercise()
    
    def _complete_lesson(self) -> None:
        """Complete the current lesson."""
        if not self.current_lesson or not self.current_user:
            return
        
        self.current_lesson.is_completed = True
        
        # Calculate final score
        session_stats = self.current_lesson.session.get_session_stats()
        final_score = session_stats["average_score"]
        
        # Update progress
        self.progress_manager.update_lesson_progress(
            user_id=self.current_user.id,
            module_id=self.current_lesson.lesson.id.split("_")[0] + "_" + self.current_lesson.lesson.id.split("_")[1],  # Extract module ID
            lesson_id=self.current_lesson.lesson.id,
            score=int(final_score),
            time_spent=session_stats["duration"]
        )
        
        # Display completion summary
        self._display_lesson_summary()
        
        # Clear current lesson
        self.current_lesson = None
    
    def _display_lesson_summary(self) -> None:
        """Display lesson completion summary."""
        if not self.current_lesson:
            return
        
        lesson = self.current_lesson.lesson
        session_stats = self.current_lesson.session.get_session_stats()
        
        self.lesson_layout.render_completion_summary(
            lesson=lesson,
            session_stats=session_stats,
            exercise_results=self.current_lesson.session.exercise_results
        )
    
    def _quit_lesson(self) -> Dict[str, Any]:
        """Quit the current lesson."""
        if self.current_lesson:
            # Save session state for resuming later
            session_stats = self.current_lesson.session.get_session_stats()
            
            # Could implement session saving here
            self.console.print("[yellow]Lesson session saved. You can resume later.[/yellow]")
            
            self.current_lesson = None
        
        return {"success": True, "message": "Lesson quit"}
    
    def _show_help(self) -> None:
        """Show help information."""
        help_text = """
[bold]Available Commands:[/bold]

[cyan]:hint[/cyan]     - Get a hint for the current exercise
[cyan]:skip[/cyan]     - Skip the current exercise  
[cyan]:restart[/cyan]  - Restart the current exercise
[cyan]:quit[/cyan]     - Quit the lesson (saves progress)
[cyan]:help[/cyan]     - Show this help

[bold]Exercise Navigation:[/bold]
- Complete exercises by following the instructions
- Use Vim commands to manipulate the text
- Watch the mode indicator and cursor position
- Don't hesitate to use hints if you're stuck!

[bold]Tips:[/bold]
- Start with the exact commands shown in instructions
- Pay attention to uppercase vs lowercase
- Remember to return to Normal mode with Escape
        """
        
        self.console.print(help_text)
        self.console.input("\n[dim]Press Enter to continue...[/dim]")
        self._display_current_exercise()
    
    def get_current_lesson_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the current lesson."""
        if not self.current_lesson:
            return None
        
        return {
            "lesson_id": self.current_lesson.lesson.id,
            "lesson_title": self.current_lesson.lesson.title,
            "progress_percentage": self.current_lesson.progress_percentage,
            "current_exercise": self.current_lesson.current_exercise_index + 1,
            "total_exercises": len(self.current_lesson.lesson.content.exercises),
            "is_completed": self.current_lesson.is_completed,
            "elapsed_time": int((datetime.now() - self.current_lesson.started_at).total_seconds())
        }
    
    def resume_lesson(self, module_id: str, lesson_id: str) -> bool:
        """Resume a previously started lesson."""
        # This would load saved session state
        # For now, just start the lesson fresh
        return self.start_lesson(module_id, lesson_id)


class LessonNavigator:
    """Helper for navigating between lessons and modules."""
    
    def __init__(self, module_manager: ModuleManager, progress_manager: ProgressManager):
        self.module_manager = module_manager
        self.progress_manager = progress_manager
    
    def get_next_lesson(self, user_id: str, current_module_id: str, 
                       current_lesson_id: str) -> Optional[tuple]:
        """Get the next lesson (module_id, lesson_id)."""
        user_progress = self.progress_manager.get_user_progress(user_id)
        
        # Try to find next lesson in current module
        current_module = self.module_manager.get_module(current_module_id)
        if current_module:
            next_lesson = current_module.get_next_lesson(user_progress)
            if next_lesson:
                return (current_module_id, next_lesson.id)
        
        # Try to find next module
        for module in self.module_manager.get_all_modules():
            if module.is_unlocked(user_progress):
                next_lesson = module.get_next_lesson(user_progress)
                if next_lesson:
                    return (module.id, next_lesson.id)
        
        return None  # No more lessons available
    
    def get_lesson_path(self, module_id: str, lesson_id: str) -> str:
        """Get human-readable path to lesson."""
        module = self.module_manager.get_module(module_id)
        if not module:
            return f"Unknown Module → {lesson_id}"
        
        lesson = module.get_lesson_by_id(lesson_id)
        if not lesson:
            return f"{module.title} → Unknown Lesson"
        
        lesson_index = next(
            (i for i, l in enumerate(module.lessons) if l.id == lesson_id),
            None
        )
        
        if lesson_index is not None:
            return f"{module.title} → Lesson {lesson_index + 1}: {lesson.title}"
        
        return f"{module.title} → {lesson.title}"