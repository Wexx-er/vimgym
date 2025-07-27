"""Session management for VimGym."""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class SessionState:
    """Current session state data."""
    current_module: Optional[str] = None
    current_lesson: Optional[str] = None
    current_step: int = 0
    simulator_state: Dict[str, Any] = field(default_factory=dict)
    lesson_start_time: Optional[datetime] = None
    commands_used: List[str] = field(default_factory=list)
    mistakes_made: int = 0
    hints_used: int = 0
    keystrokes: int = 0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON storage."""
        return {
            "current_module": self.current_module,
            "current_lesson": self.current_lesson,
            "current_step": self.current_step,
            "simulator_state": self.simulator_state,
            "lesson_start_time": self.lesson_start_time.isoformat() if self.lesson_start_time else None,
            "commands_used": self.commands_used,
            "mistakes_made": self.mistakes_made,
            "hints_used": self.hints_used,
            "keystrokes": self.keystrokes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SessionState':
        """Create from dictionary."""
        return cls(
            current_module=data.get("current_module"),
            current_lesson=data.get("current_lesson"),
            current_step=data.get("current_step", 0),
            simulator_state=data.get("simulator_state", {}),
            lesson_start_time=datetime.fromisoformat(data["lesson_start_time"]) if data.get("lesson_start_time") else None,
            commands_used=data.get("commands_used", []),
            mistakes_made=data.get("mistakes_made", 0),
            hints_used=data.get("hints_used", 0),
            keystrokes=data.get("keystrokes", 0)
        )


class SessionManager:
    """Manages VimGym learning sessions with auto-save and resume functionality."""
    
    def __init__(self, user_id: str, database, auto_save_interval: int = 30):
        """Initialize session manager.
        
        Args:
            user_id: User identifier
            database: Database instance for persistence
            auto_save_interval: Auto-save interval in seconds
        """
        self.user_id = user_id
        self.database = database
        self.auto_save_interval = auto_save_interval
        
        # Session data
        self.session_id = str(uuid4())
        self.started_at = datetime.now()
        self.last_saved = datetime.now()
        self.state = SessionState()
        self.is_active = False
        
        # Auto-save task
        self._auto_save_task: Optional[asyncio.Task] = None
        self._save_lock = asyncio.Lock()
    
    def start_session(self) -> str:
        """Start a new learning session.
        
        Returns:
            Session ID
        """
        self.session_id = str(uuid4())
        self.started_at = datetime.now()
        self.last_saved = datetime.now()
        self.state = SessionState()
        self.is_active = True
        
        # Start auto-save if not already running
        self._start_auto_save()
        
        # Save initial session
        self.save_session()
        
        return self.session_id
    
    def resume_session(self, session_id: str) -> bool:
        """Resume an existing session.
        
        Args:
            session_id: Session ID to resume
            
        Returns:
            True if successful, False if session not found
        """
        session_data = self.database.load_session(session_id)
        if not session_data or session_data.get("user_id") != self.user_id:
            return False
        
        # Load session data
        self.session_id = session_id
        self.started_at = datetime.fromisoformat(session_data["started_at"])
        self.last_saved = datetime.fromisoformat(session_data.get("last_saved", session_data["started_at"]))
        self.state = SessionState.from_dict(session_data.get("state", {}))
        self.is_active = True
        
        # Start auto-save
        self._start_auto_save()
        
        return True
    
    def end_session(self) -> Dict[str, Any]:
        """End the current session and return session summary.
        
        Returns:
            Session summary dictionary
        """
        if not self.is_active:
            return {}
        
        # Stop auto-save
        self._stop_auto_save()
        
        # Calculate session duration
        duration = (datetime.now() - self.started_at).total_seconds()
        
        # Create session summary
        summary = {
            "session_id": self.session_id,
            "duration": int(duration),
            "commands_used": len(set(self.state.commands_used)),
            "total_keystrokes": self.state.keystrokes,
            "mistakes_made": self.state.mistakes_made,
            "hints_used": self.state.hints_used,
            "modules_visited": [self.state.current_module] if self.state.current_module else [],
            "lessons_visited": [self.state.current_lesson] if self.state.current_lesson else []
        }
        
        # Final save
        self.save_session(ended_at=datetime.now())
        
        self.is_active = False
        return summary
    
    def save_session(self, ended_at: Optional[datetime] = None) -> None:
        """Save current session state to database.
        
        Args:
            ended_at: Optional end time if session is ending
        """
        session_data = {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "started_at": self.started_at.isoformat(),
            "last_saved": datetime.now().isoformat(),
            "state": self.state.to_dict(),
            "is_active": self.is_active
        }
        
        if ended_at:
            session_data["ended_at"] = ended_at.isoformat()
            session_data["is_active"] = False
        
        self.database.save_session(self.session_id, session_data)
        self.last_saved = datetime.now()
    
    async def _auto_save_loop(self) -> None:
        """Auto-save loop that runs in background."""
        while self.is_active:
            try:
                await asyncio.sleep(self.auto_save_interval)
                if self.is_active:
                    async with self._save_lock:
                        self.save_session()
            except asyncio.CancelledError:
                break
            except Exception as e:
                # Log error but continue auto-save
                print(f"Auto-save error: {e}")
    
    def _start_auto_save(self) -> None:
        """Start the auto-save background task."""
        if self._auto_save_task is None or self._auto_save_task.done():
            self._auto_save_task = asyncio.create_task(self._auto_save_loop())
    
    def _stop_auto_save(self) -> None:
        """Stop the auto-save background task."""
        if self._auto_save_task and not self._auto_save_task.done():
            self._auto_save_task.cancel()
    
    def start_lesson(self, module_id: str, lesson_id: str) -> None:
        """Start a lesson within the session.
        
        Args:
            module_id: Module identifier
            lesson_id: Lesson identifier
        """
        # End previous lesson if active
        if self.state.lesson_start_time:
            self.end_lesson()
        
        self.state.current_module = module_id
        self.state.current_lesson = lesson_id
        self.state.current_step = 0
        self.state.lesson_start_time = datetime.now()
        
        # Reset lesson-specific counters
        self.state.mistakes_made = 0
        self.state.hints_used = 0
        self.state.commands_used = []
        self.state.keystrokes = 0
        
        self.save_session()
    
    def end_lesson(self) -> Optional[Dict[str, Any]]:
        """End the current lesson and return lesson summary.
        
        Returns:
            Lesson summary dictionary or None if no active lesson
        """
        if not self.state.lesson_start_time:
            return None
        
        # Calculate lesson duration
        duration = (datetime.now() - self.state.lesson_start_time).total_seconds()
        
        lesson_summary = {
            "module_id": self.state.current_module,
            "lesson_id": self.state.current_lesson,
            "duration": int(duration),
            "commands_used": list(set(self.state.commands_used)),
            "keystrokes": self.state.keystrokes,
            "mistakes_made": self.state.mistakes_made,
            "hints_used": self.state.hints_used,
            "steps_completed": self.state.current_step
        }
        
        # Clear lesson state
        self.state.lesson_start_time = None
        self.state.current_step = 0
        
        self.save_session()
        return lesson_summary
    
    def record_command(self, command: str) -> None:
        """Record a Vim command used in the session.
        
        Args:
            command: Vim command that was used
        """
        self.state.commands_used.append(command)
        self.state.keystrokes += len(command)
    
    def record_mistake(self) -> None:
        """Record a mistake made during the session."""
        self.state.mistakes_made += 1
    
    def record_hint_used(self) -> None:
        """Record that a hint was used."""
        self.state.hints_used += 1
    
    def advance_step(self) -> None:
        """Advance to the next step in the current lesson."""
        self.state.current_step += 1
    
    def update_simulator_state(self, simulator_state: Dict[str, Any]) -> None:
        """Update the simulator state for session persistence.
        
        Args:
            simulator_state: Current simulator state
        """
        self.state.simulator_state = simulator_state
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics.
        
        Returns:
            Dictionary with session stats
        """
        if not self.is_active:
            return {}
        
        duration = (datetime.now() - self.started_at).total_seconds()
        
        return {
            "session_id": self.session_id,
            "duration": int(duration),
            "current_module": self.state.current_module,
            "current_lesson": self.state.current_lesson,
            "current_step": self.state.current_step,
            "commands_used": len(set(self.state.commands_used)),
            "unique_commands": len(set(self.state.commands_used)),
            "total_keystrokes": self.state.keystrokes,
            "mistakes_made": self.state.mistakes_made,
            "hints_used": self.state.hints_used,
            "last_saved": self.last_saved.isoformat()
        }
    
    def get_resumable_sessions(self) -> List[Dict[str, Any]]:
        """Get list of resumable sessions for the user.
        
        Returns:
            List of session info dictionaries
        """
        session_ids = self.database.list_user_sessions(self.user_id)
        resumable_sessions = []
        
        for session_id in session_ids:
            session_data = self.database.load_session(session_id)
            if session_data and session_data.get("is_active", False):
                # Check if session is not too old (e.g., older than 7 days)
                started_at = datetime.fromisoformat(session_data["started_at"])
                if datetime.now() - started_at < timedelta(days=7):
                    state = SessionState.from_dict(session_data.get("state", {}))
                    resumable_sessions.append({
                        "session_id": session_id,
                        "started_at": started_at.isoformat(),
                        "current_module": state.current_module,
                        "current_lesson": state.current_lesson,
                        "current_step": state.current_step
                    })
        
        # Sort by most recent first
        resumable_sessions.sort(key=lambda x: x["started_at"], reverse=True)
        return resumable_sessions
    
    def cleanup_old_sessions(self, max_age_days: int = 30) -> int:
        """Clean up old session files.
        
        Args:
            max_age_days: Maximum age in days before cleanup
            
        Returns:
            Number of sessions cleaned up
        """
        return self.database.cleanup_old_sessions(max_age_days)
    
    def create_checkpoint(self, checkpoint_name: str = "") -> str:
        """Create a named checkpoint of current session state.
        
        Args:
            checkpoint_name: Optional name for the checkpoint
            
        Returns:
            Checkpoint ID
        """
        checkpoint_id = str(uuid4())
        checkpoint_data = {
            "checkpoint_id": checkpoint_id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "created_at": datetime.now().isoformat(),
            "name": checkpoint_name or f"Checkpoint {datetime.now().strftime('%H:%M:%S')}",
            "state": self.state.to_dict()
        }
        
        # Save as a special session
        self.database.save_session(f"checkpoint_{checkpoint_id}", checkpoint_data)
        return checkpoint_id
    
    def restore_checkpoint(self, checkpoint_id: str) -> bool:
        """Restore session state from a checkpoint.
        
        Args:
            checkpoint_id: Checkpoint to restore
            
        Returns:
            True if successful, False if checkpoint not found
        """
        checkpoint_data = self.database.load_session(f"checkpoint_{checkpoint_id}")
        if not checkpoint_data or checkpoint_data.get("user_id") != self.user_id:
            return False
        
        # Restore state
        self.state = SessionState.from_dict(checkpoint_data.get("state", {}))
        self.save_session()
        return True