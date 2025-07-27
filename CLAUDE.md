# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VimGym is an interactive command-line Vim tutor designed to transform learning Vim from a frustrating experience into an engaging and efficient journey. The project combines gamification, personalized learning, and hands-on practice in a safe simulated environment.

## Project Architecture

This is currently in the design phase. The main design document (`vimgym-design.md`) contains comprehensive specifications for:

- **Core System**: Session management, progress tracking, user profiles, JSON database operations
- **Vim Simulator**: Text buffer simulation, cursor management, mode handling, command processing
- **Module System**: 7 learning modules progressing from basics to advanced configuration
- **UI Components**: Terminal-based interface using Rich library for rendering
- **Features**: Challenge system, achievements, interactive cheat sheet, analytics

### Planned Project Structure
```
vimgym/
├── vimgym.py                 # Main entry point
├── vimgym/                   # Main package
│   ├── core/                 # Core framework (session, progress, user, database)
│   ├── ui/                   # User interface components and themes
│   ├── simulator/            # Vim behavior simulation
│   ├── modules/              # Learning modules (7 modules total)
│   ├── features/             # Additional features (challenges, achievements)
│   └── utils/                # Utility functions
├── data/                     # Lesson content, challenges, achievements
└── tests/                    # Test suite
```

## Technology Stack

**Primary Dependencies**:
- `rich==13.7.0` - Terminal UI framework
- `click==8.1.7` - CLI framework  
- `questionary==2.0.1` - Interactive prompts
- `pyfiglet==1.0.2` - ASCII art headers
- `colorama==0.4.6` - Cross-platform colors
- `pyyaml==6.0.1` - YAML config files
- `jsonschema==4.20.0` - Data validation

**Development Dependencies**:
- `pytest==7.4.3` - Testing framework
- `black==23.11.0` - Code formatting
- `mypy==1.7.1` - Type checking

## Development Commands

Since this project is in early design phase, standard Python development commands would apply:

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies (when requirements.txt exists)
pip install -r requirements.txt

# Run the application (when implemented)
python vimgym.py
# or
python -m vimgym

# Run tests (when test suite exists)
pytest

# Code formatting
black .

# Type checking
mypy vimgym/

# Run linting
flake8 vimgym/
```

## Key Design Principles

1. **Progressive Learning**: Modules build from basic hjkl movement to advanced features like macros and configuration
2. **Hands-on Practice**: Vim simulator provides safe environment for learning without risk of data loss
3. **Gamification**: Achievement system, progress tracking, and challenges motivate learners
4. **Cross-platform**: Designed to work on Linux, macOS, and Windows terminals
5. **Local-first**: All data stored locally, no cloud dependencies

## Implementation Priority

The design document outlines a 14-week implementation roadmap:

1. **Weeks 1-2**: Foundation (CLI framework, user management, progress tracking)
2. **Weeks 3-4**: Vim simulator core (buffer, cursor, modes, basic commands)
3. **Weeks 5-6**: First 3 learning modules with content
4. **Weeks 7-8**: Advanced simulator features (visual mode, registers, search)
5. **Weeks 9-10**: Complete all 7 modules and challenge system
6. **Weeks 11-12**: UI/UX polish and additional features
7. **Weeks 13-14**: Testing, documentation, and deployment

## Target Users

- **Primary**: Complete Vim beginners (40%) transitioning from GUI editors
- **Secondary**: Users of other editors wanting to switch to Vim (35%)
- **Tertiary**: Occasional Vim users seeking advanced techniques (25%)

## Data Storage

- JSON-based local storage for user profiles, progress, and session data
- YAML files for lesson content, challenges, and achievements
- No external dependencies or cloud storage required