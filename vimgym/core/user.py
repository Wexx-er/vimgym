"""User profile management for VimGym."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from .progress import ProgressManager


@dataclass
class UserPreferences:
    """User preferences and settings."""
    theme: str = "dark"  # dark, light
    animation_speed: str = "normal"  # slow, normal, fast
    sound_enabled: bool = True
    difficulty_preference: str = "adaptive"  # adaptive, fixed
    session_reminder: int = 1440  # minutes (24 hours)
    auto_save_interval: int = 30  # seconds
    show_hints: bool = True
    show_line_numbers: bool = True
    vim_mode_indicators: bool = True
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON storage."""
        return {
            "theme": self.theme,
            "animation_speed": self.animation_speed,
            "sound_enabled": self.sound_enabled,
            "difficulty_preference": self.difficulty_preference,
            "session_reminder": self.session_reminder,
            "auto_save_interval": self.auto_save_interval,
            "show_hints": self.show_hints,
            "show_line_numbers": self.show_line_numbers,
            "vim_mode_indicators": self.vim_mode_indicators
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserPreferences':
        """Create from dictionary."""
        return cls(
            theme=data.get("theme", "dark"),
            animation_speed=data.get("animation_speed", "normal"),
            sound_enabled=data.get("sound_enabled", True),
            difficulty_preference=data.get("difficulty_preference", "adaptive"),
            session_reminder=data.get("session_reminder", 1440),
            auto_save_interval=data.get("auto_save_interval", 30),
            show_hints=data.get("show_hints", True),
            show_line_numbers=data.get("show_line_numbers", True),
            vim_mode_indicators=data.get("vim_mode_indicators", True)
        )


@dataclass
class UserStatistics:
    """User learning statistics."""
    total_time_spent: int = 0  # seconds
    sessions_completed: int = 0
    modules_completed: int = 0
    lessons_completed: int = 0
    average_session_length: int = 0  # seconds
    total_keystrokes: int = 0
    accuracy_rate: float = 0.0  # 0.0 to 1.0
    current_wpm: int = 0  # words per minute
    favorite_commands: Dict[str, int] = field(default_factory=dict)
    improvement_rate: float = 0.0  # percentage improvement over time
    mistake_patterns: Dict[str, int] = field(default_factory=dict)
    learning_streak: int = 0  # consecutive days
    last_active_date: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON storage."""
        return {
            "total_time_spent": self.total_time_spent,
            "sessions_completed": self.sessions_completed,
            "modules_completed": self.modules_completed,
            "lessons_completed": self.lessons_completed,
            "average_session_length": self.average_session_length,
            "total_keystrokes": self.total_keystrokes,
            "accuracy_rate": self.accuracy_rate,
            "current_wpm": self.current_wpm,
            "favorite_commands": self.favorite_commands,
            "improvement_rate": self.improvement_rate,
            "mistake_patterns": self.mistake_patterns,
            "learning_streak": self.learning_streak,
            "last_active_date": self.last_active_date.isoformat() if self.last_active_date else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserStatistics':
        """Create from dictionary."""
        return cls(
            total_time_spent=data.get("total_time_spent", 0),
            sessions_completed=data.get("sessions_completed", 0),
            modules_completed=data.get("modules_completed", 0),
            lessons_completed=data.get("lessons_completed", 0),
            average_session_length=data.get("average_session_length", 0),
            total_keystrokes=data.get("total_keystrokes", 0),
            accuracy_rate=data.get("accuracy_rate", 0.0),
            current_wpm=data.get("current_wpm", 0),
            favorite_commands=data.get("favorite_commands", {}),
            improvement_rate=data.get("improvement_rate", 0.0),
            mistake_patterns=data.get("mistake_patterns", {}),
            learning_streak=data.get("learning_streak", 0),
            last_active_date=datetime.fromisoformat(data["last_active_date"]) if data.get("last_active_date") else None
        )


class User:
    """VimGym user profile and data management."""
    
    def __init__(self, username: str, user_id: Optional[str] = None):
        """Initialize user profile.
        
        Args:
            username: User's display name
            user_id: Optional user ID (generates new if not provided)
        """
        self.id = user_id or str(uuid4())
        self.username = username
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self.preferences = UserPreferences()
        self.statistics = UserStatistics()
        self.progress_manager: Optional[ProgressManager] = None
        self._database = None
    
    def initialize_with_database(self, database) -> None:
        """Initialize user with database connection.
        
        Args:
            database: Database instance for persistence
        """
        self._database = database
        self.progress_manager = ProgressManager(self.id, database)
        
        # Load existing user data if it exists
        existing_data = database.load_user(self.id)
        if existing_data:
            self._load_from_dict(existing_data)
    
    def _load_from_dict(self, data: Dict) -> None:
        """Load user data from dictionary.
        
        Args:
            data: User data dictionary
        """
        self.username = data.get("username", self.username)
        self.created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else self.created_at
        self.last_active = datetime.fromisoformat(data["last_active"]) if data.get("last_active") else self.last_active
        
        if "preferences" in data:
            self.preferences = UserPreferences.from_dict(data["preferences"])
        
        if "statistics" in data:
            self.statistics = UserStatistics.from_dict(data["statistics"])
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary for JSON storage.
        
        Returns:
            User data dictionary
        """
        return {
            "user_id": self.id,
            "username": self.username,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "preferences": self.preferences.to_dict(),
            "statistics": self.statistics.to_dict()
        }
    
    def save(self) -> None:
        """Save user data to database."""
        if self._database:
            self.last_active = datetime.now()
            self._database.save_user(self.id, self.to_dict())
            
            # Also save progress if manager exists
            if self.progress_manager:
                self.progress_manager.save_progress()
    
    @classmethod
    def load(cls, user_id: str, database) -> Optional['User']:
        """Load user from database.
        
        Args:
            user_id: User identifier
            database: Database instance
            
        Returns:
            User instance or None if not found
        """
        user_data = database.load_user(user_id)
        if not user_data:
            return None
        
        user = cls(user_data.get("username", "Unknown"), user_id)
        user.initialize_with_database(database)
        return user
    
    def update_session_stats(self, time_spent: int, keystrokes: int, 
                           mistakes: int, commands_used: List[str]) -> None:
        """Update user statistics after a session.
        
        Args:
            time_spent: Time spent in session (seconds)
            keystrokes: Number of keystrokes
            mistakes: Number of mistakes made
            commands_used: List of Vim commands used
        """
        # Update basic stats
        self.statistics.sessions_completed += 1
        self.statistics.total_time_spent += time_spent
        self.statistics.total_keystrokes += keystrokes
        
        # Calculate average session length
        self.statistics.average_session_length = (
            self.statistics.total_time_spent // max(self.statistics.sessions_completed, 1)
        )
        
        # Update accuracy rate
        if keystrokes > 0:
            accuracy = max(0.0, 1.0 - (mistakes / keystrokes))
            # Weighted average with previous accuracy
            sessions = self.statistics.sessions_completed
            self.statistics.accuracy_rate = (
                (self.statistics.accuracy_rate * (sessions - 1) + accuracy) / sessions
            )
        
        # Update WPM (approximate, assuming average word length of 5 characters)
        if time_spent > 0:
            words = keystrokes / 5
            wpm = int((words / time_spent) * 60)
            self.statistics.current_wpm = wpm
        
        # Update favorite commands
        for command in commands_used:
            self.statistics.favorite_commands[command] = (
                self.statistics.favorite_commands.get(command, 0) + 1
            )
        
        # Update learning streak
        today = datetime.now().date()
        last_active = self.statistics.last_active_date
        
        if last_active:
            last_date = last_active.date()
            if today == last_date:
                # Same day, don't change streak
                pass
            elif (today - last_date).days == 1:
                # Consecutive day
                self.statistics.learning_streak += 1
            else:
                # Streak broken
                self.statistics.learning_streak = 1
        else:
            # First session
            self.statistics.learning_streak = 1
        
        self.statistics.last_active_date = datetime.now()
        self.save()
    
    def get_recommended_module(self) -> Optional[str]:
        """Get recommended next module based on progress.
        
        Returns:
            Module ID recommendation or None
        """
        if not self.progress_manager:
            return "module_01"  # Start with basics
        
        # Simple recommendation logic
        progress = self.progress_manager.get_overall_progress()
        
        # If no modules started, recommend basics
        if progress["total_modules"] == 0:
            return "module_01"
        
        # Find first incomplete module
        module_ids = ["module_01", "module_02", "module_03", "module_04", 
                     "module_05", "module_06", "module_07"]
        
        for module_id in module_ids:
            module_progress = self.progress_manager.get_module_progress(module_id)
            if not module_progress or module_progress.completion_percentage < 100:
                return module_id
        
        # All modules completed
        return None
    
    def get_learning_insights(self) -> Dict:
        """Get personalized learning insights.
        
        Returns:
            Dictionary with learning insights and recommendations
        """
        insights = {
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "next_goals": []
        }
        
        stats = self.statistics
        
        # Analyze accuracy
        if stats.accuracy_rate > 0.9:
            insights["strengths"].append("High accuracy rate")
        elif stats.accuracy_rate < 0.7:
            insights["weaknesses"].append("Low accuracy rate")
            insights["recommendations"].append("Practice basic commands more slowly")
        
        # Analyze speed
        if stats.current_wpm > 40:
            insights["strengths"].append("Good typing speed")
        elif stats.current_wpm < 20:
            insights["weaknesses"].append("Slow typing speed")
            insights["recommendations"].append("Focus on muscle memory development")
        
        # Analyze learning streak
        if stats.learning_streak > 7:
            insights["strengths"].append("Excellent learning consistency")
        elif stats.learning_streak < 3:
            insights["recommendations"].append("Try to practice daily for better retention")
        
        # Analyze favorite commands
        if stats.favorite_commands:
            most_used = max(stats.favorite_commands.items(), key=lambda x: x[1])
            insights["strengths"].append(f"Comfortable with '{most_used[0]}' command")
        
        # Progress-based recommendations
        if self.progress_manager:
            progress = self.progress_manager.get_overall_progress()
            completion = progress["overall_completion"]
            
            if completion < 25:
                insights["next_goals"].append("Complete basic movement module")
            elif completion < 50:
                insights["next_goals"].append("Master text editing commands")
            elif completion < 75:
                insights["next_goals"].append("Learn advanced search and replace")
            else:
                insights["next_goals"].append("Explore advanced Vim features")
        
        return insights


class UserManager:
    """Manages multiple user profiles."""
    
    def __init__(self, database):
        """Initialize user manager.
        
        Args:
            database: Database instance for persistence
        """
        self.database = database
        self._current_user: Optional[User] = None
    
    def create_user(self, username: str) -> User:
        """Create a new user profile.
        
        Args:
            username: User's display name
            
        Returns:
            New User instance
        """
        user = User(username)
        user.initialize_with_database(self.database)
        user.save()
        return user
    
    def load_user(self, user_id: str) -> Optional[User]:
        """Load existing user by ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            User instance or None if not found
        """
        return User.load(user_id, self.database)
    
    def list_users(self) -> List[Dict]:
        """List all users with basic info.
        
        Returns:
            List of user info dictionaries
        """
        user_list = []
        for user_id in self.database.list_users():
            user_data = self.database.load_user(user_id)
            if user_data:
                user_list.append({
                    "user_id": user_id,
                    "username": user_data.get("username", "Unknown"),
                    "last_active": user_data.get("last_active"),
                    "created_at": user_data.get("created_at")
                })
        
        # Sort by last active date
        user_list.sort(key=lambda x: x.get("last_active", ""), reverse=True)
        return user_list
    
    def set_current_user(self, user: User) -> None:
        """Set the current active user.
        
        Args:
            user: User to set as current
        """
        self._current_user = user
    
    def get_current_user(self) -> Optional[User]:
        """Get the current active user.
        
        Returns:
            Current User instance or None
        """
        return self._current_user
    
    def switch_user(self, user_id: str) -> bool:
        """Switch to a different user.
        
        Args:
            user_id: User ID to switch to
            
        Returns:
            True if successful, False if user not found
        """
        user = self.load_user(user_id)
        if user:
            self.set_current_user(user)
            return True
        return False