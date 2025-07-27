"""JSON database operations for VimGym."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class JSONDatabase:
    """Simple JSON-based database for VimGym data storage."""
    
    def __init__(self, base_path: Path):
        """Initialize database with base path.
        
        Args:
            base_path: Base directory for database files
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.users_dir = self.base_path / "users"
        self.progress_dir = self.base_path / "progress"
        self.sessions_dir = self.base_path / "sessions"
        
        for dir_path in [self.users_dir, self.progress_dir, self.sessions_dir]:
            dir_path.mkdir(exist_ok=True)
    
    def save_user(self, user_id: str, user_data: Dict[str, Any]) -> None:
        """Save user data to JSON file.
        
        Args:
            user_id: Unique user identifier
            user_data: User data dictionary
        """
        user_file = self.users_dir / f"{user_id}.json"
        user_data["last_updated"] = datetime.now().isoformat()
        
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
    
    def load_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Load user data from JSON file.
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            User data dictionary or None if not found
        """
        user_file = self.users_dir / f"{user_id}.json"
        
        if not user_file.exists():
            return None
            
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def list_users(self) -> List[str]:
        """List all user IDs.
        
        Returns:
            List of user IDs
        """
        users = []
        for user_file in self.users_dir.glob("*.json"):
            users.append(user_file.stem)
        return sorted(users)
    
    def save_progress(self, user_id: str, progress_data: Dict[str, Any]) -> None:
        """Save user progress data.
        
        Args:
            user_id: Unique user identifier
            progress_data: Progress data dictionary
        """
        progress_file = self.progress_dir / f"{user_id}.json"
        progress_data["last_updated"] = datetime.now().isoformat()
        
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2, ensure_ascii=False)
    
    def load_progress(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Load user progress data.
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            Progress data dictionary or None if not found
        """
        progress_file = self.progress_dir / f"{user_id}.json"
        
        if not progress_file.exists():
            return None
            
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def save_session(self, session_id: str, session_data: Dict[str, Any]) -> None:
        """Save session data.
        
        Args:
            session_id: Unique session identifier
            session_data: Session data dictionary
        """
        session_file = self.sessions_dir / f"{session_id}.json"
        session_data["last_updated"] = datetime.now().isoformat()
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session data.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Session data dictionary or None if not found
        """
        session_file = self.sessions_dir / f"{session_id}.json"
        
        if not session_file.exists():
            return None
            
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def delete_session(self, session_id: str) -> bool:
        """Delete session data.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            True if deleted, False if not found
        """
        session_file = self.sessions_dir / f"{session_id}.json"
        
        if session_file.exists():
            session_file.unlink()
            return True
        return False
    
    def list_user_sessions(self, user_id: str) -> List[str]:
        """List all sessions for a user.
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            List of session IDs for the user
        """
        sessions = []
        for session_file in self.sessions_dir.glob("*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    if session_data.get('user_id') == user_id:
                        sessions.append(session_file.stem)
            except (json.JSONDecodeError, IOError):
                continue
        return sorted(sessions)
    
    def cleanup_old_sessions(self, max_age_days: int = 30) -> int:
        """Clean up old session files.
        
        Args:
            max_age_days: Maximum age in days before cleanup
            
        Returns:
            Number of sessions cleaned up
        """
        cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 60 * 60)
        cleaned_count = 0
        
        for session_file in self.sessions_dir.glob("*.json"):
            if session_file.stat().st_mtime < cutoff_time:
                session_file.unlink()
                cleaned_count += 1
                
        return cleaned_count