# VimGym

Interactive tutorial for vim - Learn vim through hands-on exercises and challenges.

## Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd vimgym
   ```

2. **Set up the development environment:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install --upgrade pip
   pip install -r requirements-dev.txt
   
   # Install VimGym in development mode
   pip install -e .
   ```

3. **Verify installation:**
   ```bash
   vimgym --help
   vimgym hello
   ```

### Basic Usage

- `vimgym --help` - Show available commands
- `vimgym hello` - Test command to verify installation
- `vimgym status` - Show VimGym status and configuration

## Development

For detailed development setup and contribution guidelines, see [docs/development.md](docs/development.md).

### Quick Development Setup

```bash
# Use Make for convenience (optional)
make install    # Install dependencies
make test       # Run tests
make check      # Run all quality checks
make format     # Format code
```

## Project Structure

- `vimgym/` - Main Python package
- `data/` - Tutorial data and configurations
- `tests/` - Test suite
- `docs/` - Documentation

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run quality checks: `make check`
5. Commit using conventional commits: `git commit -m "feat: add amazing feature"`
6. Push and create a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
