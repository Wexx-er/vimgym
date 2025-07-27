# VimGym 🏋️

An interactive Vim tutor that helps you learn Vim through hands-on practice in a safe, simulated environment.

## Features

🎯 **Interactive Learning Modules**
- 4 comprehensive learning modules (more coming soon!)
- From basics to advanced Vim operations
- Guided exercises with real-time feedback

🎮 **Vim Simulator**
- Safe practice environment
- Real Vim commands and behavior
- No risk of damaging files

📊 **Progress Tracking**
- Track your learning progress
- Completion statistics
- Learning streaks and achievements

💡 **Smart Hints System**
- Context-aware hints
- Step-by-step guidance
- Common mistake prevention

## Learning Path

1. **Vim Basics & Introduction** - Learn what Vim is and master basic operations
2. **Movement & Navigation** - Efficient movement and navigation techniques  
3. **Text Editing** - Master text editing, copying, pasting, and manipulation
4. **Search & Replace** - Powerful search and replace operations
5. **File Operations** (coming soon) - Working with files and buffers
6. **Advanced Features** (coming soon) - Advanced Vim techniques
7. **Configuration** (coming soon) - Customizing Vim to your needs

## Installation

### From PyPI (when published)

```bash
pip install vimgym
```

### From Source

```bash
git clone https://github.com/marekmajer/vimgym.git
cd vimgym
pip install -e .
```

## Quick Start

### Start VimGym

```bash
vimgym
```

### Command Line Options

```bash
vimgym --help                    # Show help
vimgym --data-dir /path/to/data  # Use custom data directory
vimgym --debug                   # Enable debug mode
```

### Navigation

- Use number keys to navigate menus
- In lessons, type Vim commands directly
- Use `:hint` for help, `:skip` to skip exercises
- Practice mode lets you experiment freely

## Requirements

- Python 3.8 or higher
- Terminal with Unicode support (most modern terminals)
- No actual Vim installation required!

## Example Session

```
🏋️ VimGym - Interactive Vim Learning

Welcome! Ready to master Vim?

1. 📚 Start Learning
2. 🎮 Practice Mode  
3. 📊 View Progress
4. ⚙️ Settings
5. ❓ Help
0. 🚪 Exit

Select option [0-5]: 1

📚 Module Selection

1. ✅ Vim Basics & Introduction (100%)
2. 🔄 Movement & Navigation (60%)
3. 🔓 Text Editing (0%)
4. 🔓 Search & Replace (0%)

Select module [1-4]: 3
```

## Development

### Setting up development environment

```bash
git clone https://github.com/marekmajer/vimgym.git
cd vimgym
pip install -e .[dev]
```

### Running tests

```bash
pytest
```

### Code formatting

```bash
black vimgym/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Areas where help is needed:

- 📚 Additional learning modules
- 🌐 Internationalization
- 🎨 Themes and UI improvements
- 📝 Documentation
- 🐛 Bug reports and fixes

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by `vimtutor` and other Vim learning tools
- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal UI
- Thanks to the Vim community for decades of amazing editor development

## Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/marekmajer/vimgym/issues)
- 💬 **Questions**: [GitHub Discussions](https://github.com/marekmajer/vimgym/discussions)
- 📧 **Contact**: Create an issue for questions

---

Happy Vim learning! 🎉
