"""Progress tracking system for VimGym."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set
from uuid import uuid4


class ModuleStatus(Enum):
    """Status of a learning module."""
    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class LessonProgress:
    """Progress data for a specific lesson."""
    lesson_id: str
    attempts: int = 0
    best_score: int = 0
    completion_time: Optional[int] = None  # seconds
    mistakes_made: int = 0
    hints_used: int = 0
    commands_practiced: List[str] = field(default_factory=list)
    first_attempted: Optional[datetime] = None
    last_accessed: Optional[datetime] = None
    completed: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON storage."""
        return {
            "lesson_id": self.lesson_id,
            "attempts": self.attempts,
            "best_score": self.best_score,
            "completion_time": self.completion_time,
            "mistakes_made": self.mistakes_made,
            "hints_used": self.hints_used,
            "commands_practiced": self.commands_practiced,
            "first_attempted": self.first_attempted.isoformat() if self.first_attempted else None,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "completed": self.completed
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'LessonProgress':
        """Create from dictionary."""
        return cls(
            lesson_id=data["lesson_id"],
            attempts=data.get("attempts", 0),
            best_score=data.get("best_score", 0),
            completion_time=data.get("completion_time"),
            mistakes_made=data.get("mistakes_made", 0),
            hints_used=data.get("hints_used", 0),
            commands_practiced=data.get("commands_practiced", []),
            first_attempted=datetime.fromisoformat(data["first_attempted"]) if data.get("first_attempted") else None,
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") else None,
            completed=data.get("completed", False)
        )


@dataclass
class ModuleProgress:
    """Progress data for a learning module."""
    module_id: str
    status: ModuleStatus = ModuleStatus.LOCKED
    completion_percentage: float = 0.0
    lessons_completed: Set[str] = field(default_factory=set)
    best_score: Optional[int] = None
    time_spent: int = 0  # seconds
    first_started: Optional[datetime] = None
    last_accessed: Optional[datetime] = None
    lesson_progress: Dict[str, LessonProgress] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON storage."""
        return {
            "module_id": self.module_id,
            "status": self.status.value,
            "completion_percentage": self.completion_percentage,
            "lessons_completed": list(self.lessons_completed),
            "best_score": self.best_score,
            "time_spent": self.time_spent,
            "first_started": self.first_started.isoformat() if self.first_started else None,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "lesson_progress": {k: v.to_dict() for k, v in self.lesson_progress.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ModuleProgress':
        """Create from dictionary."""
        return cls(
            module_id=data["module_id"],
            status=ModuleStatus(data.get("status", "locked")),
            completion_percentage=data.get("completion_percentage", 0.0),
            lessons_completed=set(data.get("lessons_completed", [])),
            best_score=data.get("best_score"),
            time_spent=data.get("time_spent", 0),
            first_started=datetime.fromisoformat(data["first_started"]) if data.get("first_started") else None,
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") else None,
            lesson_progress={k: LessonProgress.from_dict(v) for k, v in data.get("lesson_progress", {}).items()}
        )


@dataclass
class Achievement:
    """User achievement data."""
    id: str
    unlocked_at: datetime
    progress: int = 100
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON storage."""
        return {
            "id": self.id,
            "unlocked_at": self.unlocked_at.isoformat(),
            "progress": self.progress
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Achievement':
        """Create from dictionary."""
        return cls(
            id=data["id"],
            unlocked_at=datetime.fromisoformat(data["unlocked_at"]),
            progress=data.get("progress", 100)
        )


class ProgressManager:
    """Manages user progress tracking across modules and lessons."""
    
    def __init__(self, user_id: str, database):
        """Initialize progress manager.
        
        Args:
            user_id: Unique user identifier
            database: Database instance for persistence
        """
        self.user_id = user_id
        self.database = database
        self.module_progress: Dict[str, ModuleProgress] = {}
        self.achievements: List[Achievement] = []
        self.total_time_spent = 0
        self.last_updated = datetime.now()
        
        # Load existing progress
        self._load_progress()
    
    def _load_progress(self) -> None:
        """Load progress data from database."""
        progress_data = self.database.load_progress(self.user_id)
        
        if progress_data:
            # Load module progress
            for module_id, module_data in progress_data.get("modules", {}).items():
                self.module_progress[module_id] = ModuleProgress.from_dict(module_data)
            
            # Load achievements
            for achievement_data in progress_data.get("achievements", []):
                self.achievements.append(Achievement.from_dict(achievement_data))
            
            self.total_time_spent = progress_data.get("total_time_spent", 0)
            if progress_data.get("last_updated"):
                self.last_updated = datetime.fromisoformat(progress_data["last_updated"])
    
    def save_progress(self) -> None:
        """Save progress data to database."""
        progress_data = {
            "user_id": self.user_id,
            "modules": {k: v.to_dict() for k, v in self.module_progress.items()},
            "achievements": [a.to_dict() for a in self.achievements],
            "total_time_spent": self.total_time_spent,
            "last_updated": datetime.now().isoformat()
        }
        
        self.database.save_progress(self.user_id, progress_data)
        self.last_updated = datetime.now()
    
    def unlock_module(self, module_id: str) -> None:
        """Unlock a module for learning.
        
        Args:
            module_id: Module identifier to unlock
        """
        if module_id not in self.module_progress:
            self.module_progress[module_id] = ModuleProgress(module_id=module_id)
        
        if self.module_progress[module_id].status == ModuleStatus.LOCKED:
            self.module_progress[module_id].status = ModuleStatus.AVAILABLE
            self.save_progress()
    
    def start_module(self, module_id: str) -> None:
        """Start working on a module.
        
        Args:
            module_id: Module identifier to start
        """
        if module_id not in self.module_progress:
            self.module_progress[module_id] = ModuleProgress(module_id=module_id)
        
        module = self.module_progress[module_id]
        if module.status in [ModuleStatus.AVAILABLE, ModuleStatus.LOCKED]:
            module.status = ModuleStatus.IN_PROGRESS
            module.first_started = datetime.now()
        
        module.last_accessed = datetime.now()
        self.save_progress()
    
    def update_lesson_progress(self, module_id: str, lesson_id: str, 
                             score: int, time_taken: int, mistakes: int = 0, 
                             hints: int = 0, commands: List[str] = None) -> None:
        """Update progress for a specific lesson.
        
        Args:
            module_id: Module identifier
            lesson_id: Lesson identifier
            score: Score achieved (0-100)
            time_taken: Time taken in seconds
            mistakes: Number of mistakes made
            hints: Number of hints used
            commands: List of commands practiced
        """
        if module_id not in self.module_progress:
            self.module_progress[module_id] = ModuleProgress(module_id=module_id)
        
        module = self.module_progress[module_id]
        
        # Initialize lesson progress if not exists
        if lesson_id not in module.lesson_progress:
            module.lesson_progress[lesson_id] = LessonProgress(lesson_id=lesson_id)
            module.lesson_progress[lesson_id].first_attempted = datetime.now()
        
        lesson = module.lesson_progress[lesson_id]
        
        # Update lesson data
        lesson.attempts += 1
        lesson.best_score = max(lesson.best_score, score)
        lesson.completion_time = time_taken
        lesson.mistakes_made = mistakes
        lesson.hints_used = hints
        lesson.last_accessed = datetime.now()
        
        if commands:
            # Add new commands to practiced list
            lesson.commands_practiced.extend(commands)
            lesson.commands_practiced = list(set(lesson.commands_practiced))  # Remove duplicates
        
        # Mark as completed if score is high enough
        if score >= 80:  # 80% passing score
            lesson.completed = True
            module.lessons_completed.add(lesson_id)
        
        # Update module stats
        module.time_spent += time_taken
        module.last_accessed = datetime.now()
        self.total_time_spent += time_taken
        
        # Calculate completion percentage
        self._update_module_completion(module_id)
        
        self.save_progress()
    
    def _update_module_completion(self, module_id: str) -> None:
        """Update module completion percentage.
        
        Args:
            module_id: Module identifier
        """
        # This would normally check against actual module lesson count
        # For now, assume 5 lessons per module
        LESSONS_PER_MODULE = 5
        
        module = self.module_progress[module_id]
        completed_lessons = len(module.lessons_completed)
        module.completion_percentage = (completed_lessons / LESSONS_PER_MODULE) * 100
        
        # Update module status
        if module.completion_percentage >= 100:
            module.status = ModuleStatus.COMPLETED
        elif module.completion_percentage > 0:
            module.status = ModuleStatus.IN_PROGRESS
    
    def get_module_progress(self, module_id: str) -> Optional[ModuleProgress]:
        """Get progress for a specific module.
        
        Args:
            module_id: Module identifier
            
        Returns:
            ModuleProgress instance or None
        """
        return self.module_progress.get(module_id)
    
    def get_lesson_progress(self, module_id: str, lesson_id: str) -> Optional[LessonProgress]:
        """Get progress for a specific lesson.
        
        Args:
            module_id: Module identifier
            lesson_id: Lesson identifier
            
        Returns:
            LessonProgress instance or None
        """
        module = self.module_progress.get(module_id)
        if module:
            return module.lesson_progress.get(lesson_id)
        return None
    
    def unlock_achievement(self, achievement_id: str) -> bool:
        """Unlock an achievement for the user.
        
        Args:
            achievement_id: Achievement identifier
            
        Returns:
            True if newly unlocked, False if already unlocked
        """
        # Check if already unlocked
        for achievement in self.achievements:
            if achievement.id == achievement_id:
                return False
        
        # Add new achievement
        self.achievements.append(Achievement(
            id=achievement_id,
            unlocked_at=datetime.now()
        ))
        
        self.save_progress()
        return True
    
    def get_overall_progress(self) -> Dict:
        """Get overall progress summary.
        
        Returns:
            Dictionary with overall progress statistics
        """
        total_modules = len(self.module_progress)
        completed_modules = sum(1 for m in self.module_progress.values() 
                              if m.status == ModuleStatus.COMPLETED)
        
        total_lessons = sum(len(m.lesson_progress) for m in self.module_progress.values())
        completed_lessons = sum(len(m.lessons_completed) for m in self.module_progress.values())
        
        return {
            "total_modules": total_modules,
            "completed_modules": completed_modules,
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "total_time_spent": self.total_time_spent,
            "achievements_count": len(self.achievements),
            "overall_completion": (completed_modules / max(total_modules, 1)) * 100
        }