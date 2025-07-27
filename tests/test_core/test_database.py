"""Tests for JSONDatabase."""

import json
import tempfile
from pathlib import Path

import pytest

from vimgym.core.database import JSONDatabase


@pytest.fixture
def temp_db():
    """Create temporary database for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db = JSONDatabase(Path(temp_dir))
        yield db


def test_database_initialization(temp_db):
    """Test database initialization creates necessary directories."""
    assert temp_db.base_path.exists()
    assert temp_db.users_dir.exists()
    assert temp_db.progress_dir.exists()
    assert temp_db.sessions_dir.exists()


def test_save_and_load_user(temp_db):
    """Test saving and loading user data."""
    user_id = "test_user_123"
    user_data = {
        "username": "testuser",
        "created_at": "2024-01-01T00:00:00",
        "preferences": {"theme": "dark"}
    }
    
    # Save user
    temp_db.save_user(user_id, user_data)
    
    # Load user
    loaded_data = temp_db.load_user(user_id)
    
    assert loaded_data is not None
    assert loaded_data["username"] == "testuser"
    assert loaded_data["preferences"]["theme"] == "dark"
    assert "last_updated" in loaded_data


def test_load_nonexistent_user(temp_db):
    """Test loading non-existent user returns None."""
    result = temp_db.load_user("nonexistent_user")
    assert result is None


def test_list_users(temp_db):
    """Test listing all users."""
    # Initially empty
    users = temp_db.list_users()
    assert len(users) == 0
    
    # Add some users
    temp_db.save_user("user1", {"username": "User One"})
    temp_db.save_user("user2", {"username": "User Two"})
    
    users = temp_db.list_users()
    assert len(users) == 2
    assert "user1" in users
    assert "user2" in users


def test_save_and_load_progress(temp_db):
    """Test saving and loading progress data."""
    user_id = "test_user"
    progress_data = {
        "modules": {
            "module_01": {
                "completion_percentage": 75.0,
                "lessons_completed": ["lesson_01", "lesson_02"]
            }
        }
    }
    
    temp_db.save_progress(user_id, progress_data)
    loaded_progress = temp_db.load_progress(user_id)
    
    assert loaded_progress is not None
    assert loaded_progress["modules"]["module_01"]["completion_percentage"] == 75.0
    assert "last_updated" in loaded_progress


def test_save_and_load_session(temp_db):
    """Test saving and loading session data."""
    session_id = "session_123"
    session_data = {
        "user_id": "test_user",
        "started_at": "2024-01-01T10:00:00",
        "current_module": "module_01"
    }
    
    temp_db.save_session(session_id, session_data)
    loaded_session = temp_db.load_session(session_id)
    
    assert loaded_session is not None
    assert loaded_session["user_id"] == "test_user"
    assert loaded_session["current_module"] == "module_01"
    assert "last_updated" in loaded_session


def test_delete_session(temp_db):
    """Test deleting session data."""
    session_id = "session_to_delete"
    session_data = {"user_id": "test_user"}
    
    # Save and verify it exists
    temp_db.save_session(session_id, session_data)
    assert temp_db.load_session(session_id) is not None
    
    # Delete and verify it's gone
    result = temp_db.delete_session(session_id)
    assert result is True
    assert temp_db.load_session(session_id) is None
    
    # Try to delete again
    result = temp_db.delete_session(session_id)
    assert result is False


def test_list_user_sessions(temp_db):
    """Test listing sessions for a specific user."""
    user_id = "test_user"
    
    # Create sessions for user
    temp_db.save_session("session1", {"user_id": user_id})
    temp_db.save_session("session2", {"user_id": user_id})
    temp_db.save_session("session3", {"user_id": "other_user"})
    
    sessions = temp_db.list_user_sessions(user_id)
    
    assert len(sessions) == 2
    assert "session1" in sessions
    assert "session2" in sessions
    assert "session3" not in sessions


def test_invalid_json_handling(temp_db):
    """Test handling of corrupted JSON files."""
    # Create invalid JSON file
    user_file = temp_db.users_dir / "invalid_user.json"
    user_file.write_text("invalid json content")
    
    # Should return None instead of crashing
    result = temp_db.load_user("invalid_user")
    assert result is None