"""
Content management system for VimGym lessons and modules.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import asdict

from .base import LearningModule, Lesson, LessonContent, Exercise, ModuleManager
from .module01_basics import Module01Basics
from .module02_movement import Module02Movement
from .module03_text_editing import Module03TextEditing
from .module04_search_replace import Module04SearchReplace


class ContentManager:
    """Manages lesson content, including loading, saving, and validation."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent.parent / "data"
        self.lessons_dir = self.data_dir / "lessons"
        self.modules_dir = self.data_dir / "modules"
        self.templates_dir = self.data_dir / "templates"
        
        # Create directories if they don't exist
        self.lessons_dir.mkdir(parents=True, exist_ok=True)
        self.modules_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        self.module_manager = ModuleManager()
        self._initialize_builtin_modules()
    
    def _initialize_builtin_modules(self) -> None:
        """Initialize built-in modules."""
        # Register built-in modules
        self.module_manager.register_module(Module01Basics())
        self.module_manager.register_module(Module02Movement())
        self.module_manager.register_module(Module03TextEditing())
        self.module_manager.register_module(Module04SearchReplace())
    
    def get_module_manager(self) -> ModuleManager:
        """Get the module manager instance."""
        return self.module_manager
    
    def export_lesson_to_yaml(self, lesson: Lesson, filepath: Path) -> None:
        """Export a lesson to YAML format."""
        lesson_data = {
            "id": lesson.id,
            "title": lesson.content.title,
            "description": lesson.content.description,
            "learning_objectives": lesson.content.learning_objectives,
            "introduction": lesson.content.introduction,
            "instructions": lesson.content.instructions,
            "summary": lesson.content.summary,
            "tips": lesson.content.tips,
            "common_mistakes": lesson.content.common_mistakes,
            "exercises": [
                {
                    "id": ex.id,
                    "title": ex.title,
                    "description": ex.description,
                    "instructions": ex.instructions,
                    "expected_commands": ex.expected_commands,
                    "initial_text": ex.initial_text,
                    "validation_type": ex.validation_type,
                    "validation_params": ex.validation_params,
                    "hints": ex.hints,
                    "time_limit": ex.time_limit
                }
                for ex in lesson.content.exercises
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(lesson_data, f, default_flow_style=False, allow_unicode=True)
    
    def load_lesson_from_yaml(self, filepath: Path) -> Lesson:
        """Load a lesson from YAML format."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        exercises = [
            Exercise(
                id=ex["id"],
                title=ex["title"],
                description=ex["description"],
                instructions=ex["instructions"],
                expected_commands=ex["expected_commands"],
                initial_text=ex.get("initial_text", ""),
                validation_type=ex.get("validation_type", "commands"),
                validation_params=ex.get("validation_params", {}),
                hints=ex.get("hints", []),
                time_limit=ex.get("time_limit")
            )
            for ex in data["exercises"]
        ]
        
        content = LessonContent(
            title=data["title"],
            description=data["description"],
            learning_objectives=data["learning_objectives"],
            introduction=data["introduction"],
            instructions=data["instructions"],
            exercises=exercises,
            summary=data.get("summary", ""),
            tips=data.get("tips", []),
            common_mistakes=data.get("common_mistakes", [])
        )
        
        return Lesson(data["id"], content)
    
    def export_module_to_json(self, module: LearningModule, filepath: Path) -> None:
        """Export a module structure to JSON format."""
        module_data = {
            "id": module.id,
            "title": module.title,
            "description": module.description,
            "prerequisites": module.prerequisites,
            "estimated_duration": module.estimated_duration,
            "lesson_ids": [lesson.id for lesson in module.lessons],
            "metadata": {
                "created_at": module.lessons[0].created_at.isoformat() if module.lessons else None,
                "lesson_count": module.lesson_count
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(module_data, f, indent=2, ensure_ascii=False)
    
    def create_lesson_template(self, lesson_id: str, title: str) -> Dict[str, Any]:
        """Create a lesson template for content creators."""
        template = {
            "id": lesson_id,
            "title": title,
            "description": "Brief description of what this lesson teaches",
            "learning_objectives": [
                "Objective 1: What students will learn",
                "Objective 2: Skills they will gain",
                "Objective 3: Knowledge they will acquire"
            ],
            "introduction": """
# Lesson Title

Introduction text explaining the concept.

## Key Concepts:
- Concept 1
- Concept 2  
- Concept 3

## Why This Matters:
Explain the practical benefits and real-world applications.
            """.strip(),
            "instructions": """
Practice instructions for the student.

**Important Notes:**
- Note 1
- Note 2
            """.strip(),
            "exercises": [
                {
                    "id": f"{lesson_id}_exercise_01",
                    "title": "Exercise 1 Title",
                    "description": "What this exercise teaches",
                    "instructions": "Step-by-step instructions for the student",
                    "expected_commands": ["command1", "command2"],
                    "initial_text": "Starting text (if needed)",
                    "validation_type": "commands",
                    "validation_params": {},
                    "hints": [
                        "Hint 1: First hint if student is stuck",
                        "Hint 2: More specific guidance",
                        "Hint 3: Almost the answer"
                    ],
                    "time_limit": None
                }
            ],
            "summary": """
Lesson summary highlighting what was learned:

✅ Key point 1
✅ Key point 2
✅ Key point 3

Next steps or what comes next.
            """.strip(),
            "tips": [
                "Practical tip 1",
                "Best practice tip 2",
                "Efficiency tip 3"
            ],
            "common_mistakes": [
                "Mistake 1 students often make",
                "Mistake 2 and how to avoid it"
            ]
        }
        
        return template
    
    def validate_lesson_content(self, lesson_data: Dict[str, Any]) -> List[str]:
        """Validate lesson content structure and return list of errors."""
        errors = []
        
        # Required fields
        required_fields = ["id", "title", "description", "learning_objectives", 
                          "introduction", "instructions", "exercises"]
        
        for field in required_fields:
            if field not in lesson_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate exercises
        if "exercises" in lesson_data:
            exercises = lesson_data["exercises"]
            if not exercises:
                errors.append("Lesson must have at least one exercise")
            
            for i, exercise in enumerate(exercises):
                ex_required = ["id", "title", "description", "instructions", "expected_commands"]
                for field in ex_required:
                    if field not in exercise:
                        errors.append(f"Exercise {i+1}: Missing required field '{field}'")
                
                # Validate expected_commands
                if "expected_commands" in exercise:
                    commands = exercise["expected_commands"]
                    if not isinstance(commands, list) or not commands:
                        errors.append(f"Exercise {i+1}: expected_commands must be non-empty list")
        
        # Validate learning objectives
        if "learning_objectives" in lesson_data:
            objectives = lesson_data["learning_objectives"]
            if not isinstance(objectives, list) or not objectives:
                errors.append("learning_objectives must be non-empty list")
        
        return errors
    
    def get_content_statistics(self) -> Dict[str, Any]:
        """Get statistics about the content library."""
        stats = {
            "modules": {
                "total": len(self.module_manager.modules),
                "details": []
            },
            "lessons": {
                "total": 0,
                "exercises": 0
            }
        }
        
        for module in self.module_manager.get_all_modules():
            module_info = {
                "id": module.id,
                "title": module.title,
                "lessons": len(module.lessons),
                "estimated_duration": module.estimated_duration,
                "prerequisites": len(module.prerequisites)
            }
            
            # Count exercises in this module
            exercise_count = sum(len(lesson.content.exercises) for lesson in module.lessons)
            module_info["exercises"] = exercise_count
            
            stats["modules"]["details"].append(module_info)
            stats["lessons"]["total"] += len(module.lessons)
            stats["lessons"]["exercises"] += exercise_count
        
        return stats
    
    def search_content(self, query: str, content_type: str = "all") -> List[Dict[str, Any]]:
        """Search through content by keywords."""
        results = []
        query_lower = query.lower()
        
        for module in self.module_manager.get_all_modules():
            if content_type in ["all", "modules"]:
                # Search in module
                if (query_lower in module.title.lower() or 
                    query_lower in module.description.lower()):
                    results.append({
                        "type": "module",
                        "id": module.id,
                        "title": module.title,
                        "description": module.description
                    })
            
            if content_type in ["all", "lessons"]:
                # Search in lessons
                for lesson in module.lessons:
                    if (query_lower in lesson.title.lower() or
                        query_lower in lesson.description.lower() or
                        query_lower in lesson.content.introduction.lower()):
                        results.append({
                            "type": "lesson",
                            "id": lesson.id,
                            "module_id": module.id,
                            "title": lesson.title,
                            "description": lesson.description
                        })
        
        return results
    
    def get_lesson_path(self, module_id: str, lesson_id: str) -> Optional[str]:
        """Get the navigation path to a specific lesson."""
        module = self.module_manager.get_module(module_id)
        if not module:
            return None
        
        lesson = module.get_lesson_by_id(lesson_id)
        if not lesson:
            return None
        
        lesson_index = next(
            (i for i, l in enumerate(module.lessons) if l.id == lesson_id), 
            None
        )
        
        if lesson_index is None:
            return None
        
        return f"{module.title} → Lesson {lesson_index + 1}: {lesson.title}"


class ContentValidator:
    """Validates lesson and module content for quality and consistency."""
    
    def __init__(self):
        self.validation_rules = {
            "lesson_title_length": (10, 80),
            "description_length": (20, 200),
            "introduction_length": (100, 2000),
            "exercise_count": (1, 10),
            "hint_count": (1, 5),
            "objective_count": (2, 6)
        }
    
    def validate_lesson(self, lesson: Lesson) -> Dict[str, Any]:
        """Comprehensive lesson validation."""
        issues = []
        warnings = []
        suggestions = []
        
        content = lesson.content
        
        # Title validation
        title_len = len(content.title)
        min_title, max_title = self.validation_rules["lesson_title_length"]
        if title_len < min_title:
            issues.append(f"Title too short ({title_len} chars, min {min_title})")
        elif title_len > max_title:
            warnings.append(f"Title quite long ({title_len} chars, max {max_title})")
        
        # Description validation
        desc_len = len(content.description)
        min_desc, max_desc = self.validation_rules["description_length"]
        if desc_len < min_desc:
            issues.append(f"Description too short ({desc_len} chars, min {min_desc})")
        
        # Exercise validation
        exercise_count = len(content.exercises)
        min_ex, max_ex = self.validation_rules["exercise_count"]
        if exercise_count < min_ex:
            issues.append(f"Too few exercises ({exercise_count}, min {min_ex})")
        elif exercise_count > max_ex:
            warnings.append(f"Many exercises ({exercise_count}, consider splitting)")
        
        # Learning objectives validation
        obj_count = len(content.learning_objectives)
        min_obj, max_obj = self.validation_rules["objective_count"]
        if obj_count < min_obj:
            issues.append(f"Too few learning objectives ({obj_count}, min {min_obj})")
        
        # Exercise-specific validation
        for i, exercise in enumerate(content.exercises):
            if not exercise.expected_commands:
                issues.append(f"Exercise {i+1}: No expected commands")
            
            if len(exercise.hints) == 0:
                warnings.append(f"Exercise {i+1}: No hints provided")
            
            if not exercise.instructions.strip():
                issues.append(f"Exercise {i+1}: Empty instructions")
        
        # Content quality suggestions
        if not content.tips:
            suggestions.append("Consider adding practical tips")
        
        if not content.common_mistakes:
            suggestions.append("Consider documenting common mistakes")
        
        if not content.summary:
            suggestions.append("Consider adding a lesson summary")
        
        return {
            "lesson_id": lesson.id,
            "issues": issues,
            "warnings": warnings,
            "suggestions": suggestions,
            "score": self._calculate_quality_score(lesson),
            "is_valid": len(issues) == 0
        }
    
    def _calculate_quality_score(self, lesson: Lesson) -> int:
        """Calculate a quality score (0-100) for a lesson."""
        score = 100
        content = lesson.content
        
        # Deduct for missing or poor content
        if len(content.learning_objectives) < 3:
            score -= 10
        
        if len(content.exercises) < 2:
            score -= 15
        
        if not content.tips:
            score -= 5
        
        if not content.common_mistakes:
            score -= 5
        
        if not content.summary:
            score -= 5
        
        # Check exercise quality
        for exercise in content.exercises:
            if len(exercise.hints) == 0:
                score -= 3
            if len(exercise.expected_commands) > 10:
                score -= 2  # Too complex
        
        # Bonus for comprehensive content
        if len(content.introduction) > 500:
            score += 5
        
        if all(len(ex.hints) >= 2 for ex in content.exercises):
            score += 5
        
        return max(0, min(100, score))