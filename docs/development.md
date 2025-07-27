# VimGym Development Guide

This guide covers setting up the development environment and contributing to VimGym.

## Prerequisites

- Python 3.8 or higher
- Git
- Make (optional, for convenience commands)

## Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd vimgym
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install development dependencies (includes production dependencies)
pip install -r requirements-dev.txt

# Install the package in development mode
pip install -e .
```

### 4. Verify Installation

```bash
# Test the CLI
vimgym --help
vimgym hello
vimgym status
```

## Project Structure

```
vimgym/
├── data/                   # Tutorial data and configurations
│   ├── achievements/       # Achievement definitions
│   ├── challenges/         # Challenge configurations
│   ├── lessons/           # Lesson content
│   └── templates/         # Template files
├── docs/                  # Documentation
├── tests/                 # Test suite
│   ├── test_core/         # Core functionality tests
│   ├── test_integration/  # Integration tests
│   ├── test_modules/      # Module-specific tests
│   └── test_simulator/    # Simulator tests
├── vimgym/               # Main package
│   ├── __init__.py       # Package initialization
│   └── cli.py            # CLI interface
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── setup.py              # Package setup configuration
└── Makefile              # Development convenience commands
```

## Development Workflow

### Code Quality

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing
- **Pre-commit**: Git hooks for quality checks

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=vimgym

# Run specific test file
pytest tests/test_core/test_example.py

# Run tests in verbose mode
pytest -v
```

### Code Formatting and Linting

```bash
# Format code with Black
black vimgym/ tests/

# Check code style with Flake8
flake8 vimgym/ tests/

# Type checking with MyPy
mypy vimgym/
```

### Using Make Commands

If you have Make installed, you can use convenient commands:

```bash
# Install development dependencies
make install

# Run all quality checks
make check

# Run tests
make test

# Format code
make format

# Clean build artifacts
make clean
```

## Adding New Features

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Implement your changes
3. Add tests for new functionality
4. Run quality checks: `make check` or manually run formatting, linting, and tests
5. Commit your changes with conventional commit messages
6. Push and create a pull request

## Commit Message Convention

Use conventional commits format:

- `feat: add new tutorial module`
- `fix: resolve CLI argument parsing issue`
- `docs: update development setup guide`
- `test: add integration tests for simulator`
- `refactor: reorganize CLI command structure`
- `chore: update dependencies`

## Testing Guidelines

- Write tests for all new functionality
- Maintain test coverage above 80%
- Use descriptive test names
- Group related tests in test classes
- Mock external dependencies in unit tests

## Debugging

### CLI Development

To debug CLI commands during development:

```python
# In vimgym/cli.py, add debugging
import pdb; pdb.set_trace()  # Add breakpoint
```

### Running CLI from Source

```bash
# Activate virtual environment
source venv/bin/activate

# Run CLI directly
python -m vimgym.cli --help
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Run quality checks
6. Submit a pull request

## Getting Help

- Check existing issues in the repository
- Read the documentation in `/docs`
- Ask questions in pull request discussions

## Performance Considerations

- Keep CLI startup time minimal
- Use lazy loading for heavy modules
- Consider caching for frequently accessed data
- Profile performance-critical paths

## Release Process

1. Update version in `vimgym/__init__.py` and `setup.py`
2. Update CHANGELOG.md
3. Create a release tag
4. Build and publish to PyPI (if applicable)