"""
Base classes for VimGym learning modules and lessons.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Callable
from datetime import datetime
import uuid

from ..core.progress import ModuleProgress, LessonProgress
from ..simulator.simulator import VimSimulator, SimulatorResponse


@dataclass
class Exercise:
    """Individual exercise within a lesson."""
    
    id: str
    title: str
    description: str
    instructions: str
    expected_commands: List[str]
    initial_text: str = ""
    validation_type: str = "commands"  # commands, cursor_position, text_content
    validation_params: Dict[str, Any] = field(default_factory=dict)
    hints: List[str] = field(default_factory=list)
    time_limit: Optional[int] = None  # seconds
    
    def validate_completion(self, executed_commands: List[str], 
                          final_state: Dict[str, Any]) -> 'ExerciseResult':
        """Validate if exercise was completed correctly."""
        if self.validation_type == "commands":
            return self._validate_commands(executed_commands)
        elif self.validation_type == "cursor_position":
            return self._validate_cursor_position(final_state)
        elif self.validation_type == "text_content":
            return self._validate_text_content(final_state)
        else:
            return ExerciseResult(False, 0, "Unknown validation type")
    
    def _validate_commands(self, executed_commands: List[str]) -> 'ExerciseResult':
        """Validate based on expected command sequence."""
        if executed_commands == self.expected_commands:
            return ExerciseResult(True, 100, "Perfect! Commands executed correctly.")
        
        # Partial credit for correct commands
        correct_count = 0
        for i, cmd in enumerate(self.expected_commands):
            if i < len(executed_commands) and executed_commands[i] == cmd:
                correct_count += 1
            else:
                break
        
        score = int((correct_count / len(self.expected_commands)) * 100)
        feedback = f"Correct commands: {correct_count}/{len(self.expected_commands)}"
        
        return ExerciseResult(score >= 70, score, feedback)
    
    def _validate_cursor_position(self, final_state: Dict[str, Any]) -> 'ExerciseResult':
        """Validate based on final cursor position."""
        expected_pos = self.validation_params.get("expected_position", (0, 0))
        actual_pos = final_state.get("cursor_position", (0, 0))
        
        if actual_pos == expected_pos:
            return ExerciseResult(True, 100, "Cursor positioned correctly!")
        else:
            return ExerciseResult(False, 0, 
                f"Cursor at {actual_pos}, expected {expected_pos}")
    
    def _validate_text_content(self, final_state: Dict[str, Any]) -> 'ExerciseResult':
        """Validate based on final text content."""
        expected_text = self.validation_params.get("expected_text", "")
        actual_text = final_state.get("buffer_content", "")
        
        if actual_text.strip() == expected_text.strip():
            return ExerciseResult(True, 100, "Text content is correct!")
        else:
            return ExerciseResult(False, 0, 
                "Text content doesn't match expected result")


@dataclass
class ExerciseResult:
    """Result of exercise completion validation."""
    passed: bool
    score: int
    feedback: str
    time_taken: Optional[int] = None
    hints_used: int = 0
    mistakes_made: int = 0


@dataclass
class LessonContent:
    """Content structure for a lesson."""
    title: str
    description: str
    learning_objectives: List[str]
    introduction: str
    instructions: str
    exercises: List[Exercise]
    summary: str = ""
    tips: List[str] = field(default_factory=list)
    common_mistakes: List[str] = field(default_factory=list)


class Lesson:
    """Individual lesson within a module."""
    
    def __init__(self, lesson_id: str, content: LessonContent):
        self.id = lesson_id
        self.content = content
        self.created_at = datetime.now()
        
    @property
    def title(self) -> str:
        return self.content.title
    
    @property
    def description(self) -> str:
        return self.content.description
    
    def start_session(self, simulator: VimSimulator, user_id: str) -> 'LessonSession':
        """Start a new lesson session."""
        return LessonSession(
            lesson=self,
            simulator=simulator,
            user_id=user_id
        )
    
    def get_exercise(self, exercise_index: int) -> Optional[Exercise]:
        """Get exercise by index."""
        if 0 <= exercise_index < len(self.content.exercises):
            return self.content.exercises[exercise_index]
        return None
    
    @property
    def exercise_count(self) -> int:
        return len(self.content.exercises)


class LessonSession:
    """Active lesson session with progress tracking."""
    
    def __init__(self, lesson: Lesson, simulator: VimSimulator, user_id: str):
        self.session_id = str(uuid.uuid4())
        self.lesson = lesson
        self.simulator = simulator
        self.user_id = user_id
        self.started_at = datetime.now()
        self.current_exercise = 0
        self.exercise_results: List[ExerciseResult] = []
        self.total_commands: List[str] = []
        self.hints_used = 0
        self.is_completed = False
        
    def get_current_exercise(self) -> Optional[Exercise]:
        """Get the current exercise."""
        return self.lesson.get_exercise(self.current_exercise)
    
    def execute_command(self, command: str) -> SimulatorResponse:
        """Execute command in simulator and track it."""
        self.total_commands.append(command)
        return self.simulator.process_input(command)
    
    def complete_current_exercise(self) -> ExerciseResult:
        """Complete current exercise and validate result."""
        exercise = self.get_current_exercise()
        if not exercise:
            return ExerciseResult(False, 0, "No current exercise")
        
        # Get final state from simulator
        final_state = {
            "cursor_position": self.simulator.buffer.cursor_pos,
            "buffer_content": self.simulator.buffer.get_content(),
            "current_mode": self.simulator.buffer.mode.value
        }
        
        # Get commands for this exercise (since last exercise completion)
        start_idx = sum(len(r.feedback) for r in self.exercise_results)
        exercise_commands = self.total_commands[start_idx:]
        
        # Validate exercise
        result = exercise.validate_completion(exercise_commands, final_state)
        result.time_taken = int((datetime.now() - self.started_at).total_seconds())
        result.hints_used = self.hints_used
        
        self.exercise_results.append(result)
        
        # Move to next exercise
        self.current_exercise += 1
        if self.current_exercise >= self.lesson.exercise_count:
            self.is_completed = True
        
        return result
    
    def use_hint(self) -> Optional[str]:
        """Use a hint for current exercise."""
        exercise = self.get_current_exercise()
        if exercise and exercise.hints and self.hints_used < len(exercise.hints):
            hint = exercise.hints[self.hints_used]
            self.hints_used += 1
            return hint
        return None
    
    def get_progress(self) -> float:
        """Get lesson completion progress (0.0 - 1.0)."""
        if not self.lesson.exercise_count:
            return 1.0
        return self.current_exercise / self.lesson.exercise_count
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get comprehensive session statistics."""
        total_score = sum(r.score for r in self.exercise_results)
        avg_score = total_score / max(len(self.exercise_results), 1)
        
        return {
            "session_id": self.session_id,
            "lesson_id": self.lesson.id,
            "started_at": self.started_at.isoformat(),
            "duration": int((datetime.now() - self.started_at).total_seconds()),
            "progress": self.get_progress(),
            "exercises_completed": len(self.exercise_results),
            "total_exercises": self.lesson.exercise_count,
            "average_score": avg_score,
            "total_commands": len(self.total_commands),
            "hints_used": self.hints_used,
            "is_completed": self.is_completed
        }


class LearningModule(ABC):
    """Abstract base class for learning modules."""
    
    def __init__(self, module_id: str, title: str, description: str):
        self.id = module_id
        self.title = title
        self.description = description
        self.lessons: List[Lesson] = []
        self.prerequisites: List[str] = []
        self.estimated_duration = 60  # minutes
        
    def add_lesson(self, lesson: Lesson) -> None:
        """Add lesson to module."""
        self.lessons.append(lesson)
    
    def get_lesson(self, lesson_index: int) -> Optional[Lesson]:
        """Get lesson by index."""
        if 0 <= lesson_index < len(self.lessons):
            return self.lessons[lesson_index]
        return None
    
    def get_lesson_by_id(self, lesson_id: str) -> Optional[Lesson]:
        """Get lesson by ID."""
        for lesson in self.lessons:
            if lesson.id == lesson_id:
                return lesson
        return None
    
    def is_unlocked(self, user_progress: ModuleProgress) -> bool:
        """Check if module is unlocked for user."""
        # Check prerequisites
        for prereq_id in self.prerequisites:
            prereq_progress = user_progress.get_module_progress(prereq_id)
            if not prereq_progress or prereq_progress.status != "completed":
                return False
        return True
    
    def get_next_lesson(self, user_progress: ModuleProgress) -> Optional[Lesson]:
        """Get next incomplete lesson for user."""
        module_progress = user_progress.get_module_progress(self.id)
        if not module_progress:
            return self.lessons[0] if self.lessons else None
        
        completed_lessons = set(module_progress.lessons_completed)
        for lesson in self.lessons:
            if lesson.id not in completed_lessons:
                return lesson
        
        return None  # All lessons completed
    
    def calculate_completion(self, user_progress: ModuleProgress) -> float:
        """Calculate module completion percentage."""
        if not self.lessons:
            return 1.0
        
        module_progress = user_progress.get_module_progress(self.id)
        if not module_progress:
            return 0.0
        
        completed_count = len(module_progress.lessons_completed)
        return completed_count / len(self.lessons)
    
    @property
    def lesson_count(self) -> int:
        return len(self.lessons)
    
    @abstractmethod
    def initialize_content(self) -> None:
        """Initialize module content - to be implemented by subclasses."""
        pass


class ModuleManager:
    """Manager for all learning modules."""
    
    def __init__(self):
        self.modules: Dict[str, LearningModule] = {}
        self.module_order: List[str] = []
    
    def register_module(self, module: LearningModule) -> None:
        """Register a learning module."""
        self.modules[module.id] = module
        if module.id not in self.module_order:
            self.module_order.append(module.id)
        
        # Initialize module content
        module.initialize_content()
    
    def get_module(self, module_id: str) -> Optional[LearningModule]:
        """Get module by ID."""
        return self.modules.get(module_id)
    
    def get_all_modules(self) -> List[LearningModule]:
        """Get all modules in order."""
        return [self.modules[mid] for mid in self.module_order if mid in self.modules]
    
    def get_available_modules(self, user_progress: ModuleProgress) -> List[LearningModule]:
        """Get modules available to user (unlocked)."""
        available = []
        for module in self.get_all_modules():
            if module.is_unlocked(user_progress):
                available.append(module)
        return available
    
    def get_next_module(self, user_progress: ModuleProgress) -> Optional[LearningModule]:
        """Get next incomplete module for user."""
        for module in self.get_all_modules():
            if not module.is_unlocked(user_progress):
                continue
            
            completion = module.calculate_completion(user_progress)
            if completion < 1.0:  # Not fully completed
                return module
        
        return None  # All modules completed