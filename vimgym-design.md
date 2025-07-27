# VimGym - Interaktivní Vim Tutor
## Kompletní Design a Implementační Dokumentace

---

## 📈 AKTUÁLNÍ STAV PROJEKTU

### ✅ **DOKONČENÉ KOMPONENTY (100%)**

#### Core Framework
- **JSONDatabase** - Multi-entity storage s timestamping a cleanup
- **ProgressManager** - Granular progress tracking, achievements, statistics  
- **SessionManager** - Auto-save, resume, checkpoint system
- **UserManager** - Multi-user support, preferences, detailed stats

#### Vim Simulator Engine  
- **VimBuffer** - Text management s undo/redo (100-level stack)
- **VimCommandProcessor** - Comprehensive command mapping s repeat counts
- **ModeManager** - Complete mode system (Normal/Insert/Visual/Command)
- **VimSimulator** - Unified interface s learning mode a display generation

#### UI Component System
- **Themes** - VS Code-inspired color palette, multiple themes
- **Components** - ProgressBar, Header, StatusIndicator, InfoPanel, KeyBindings
- **Menus** - Interactive navigation s keyboard support
- **Layouts** - Responsive design pro různé velikosti terminálů

#### Testing Infrastructure
- **76+ test cases** covering all components
- **Integration tests** pro workflow validation
- **Performance tests** pro memory a speed optimization

### 🎯 **DALŠÍ KROKY (Priority)**

1. **Lesson Content Creation** - Implementace jednotlivých modulů a lekcí
2. **Module Integration** - Propojení simulátoru s learning obsahem  
3. **Challenge System** - Implementace výzev a gamifikace
4. **Polish & Testing** - Finalizace a comprehensive testing

---

## 🎯 TODOLIST - Implementační Plán

### Fáze 1: Projekt Setup (1-2 dny) ✅ HOTOVO
- [x] Vytvořit základní strukturu projektu
- [x] Nastavit Python virtual environment
- [x] Instalace dependencies (rich, click, questionary, etc.)
- [x] Vytvořit main entry point (vimgym.py)
- [x] Základní CLI rozhraní s menu
- [x] Git repository setup + .gitignore

### Fáze 2: Core Framework (3-4 dny) ✅ HOTOVO
- [x] Implementovat Progress Manager (JSON databáze)
- [x] User Profile System (multiple users)
- [x] Session Manager (save/resume)
- [x] Základní UI komponenty (headers, menus, progress bars)
- [x] Color themes a styling systém
- [x] Error handling a logging

### Fáze 3: Vim Simulátor (4-5 dní) ✅ HOTOVO
- [x] Základní text buffer simulace
- [x] Kurzor management a pozicování
- [x] Vim módy simulation (Normal, Insert, Visual, Command)
- [x] Základní příkazy (hjkl, i, a, o, etc.)
- [x] Visual feedback systém
- [x] Command history a undo/redo
- [x] Real-time command validation

### Fáze 4: Moduly a Obsah (6-7 dní) 🔄 PRIORITY
- [ ] Modul 1: Úvod a základy
- [ ] Modul 2: Pohyb a navigace
- [ ] Modul 3: Editace textu
- [ ] Modul 4: Vyhledávání a nahrazování
- [ ] Modul 5: Práce se soubory
- [ ] Modul 6: Pokročilé funkce
- [ ] Modul 7: Konfigurace a pluginy
- [ ] Lesson content management systém
- [ ] Integration testing mezi moduly a simulátorem

### Fáze 5: Interaktivní Features (3-4 dny) ⏳ PŘIPRAVENO
- [ ] Challenge system (framework již hotový)
- [ ] Achievement/badge systém (foundation hotová)
- [ ] Interactive cheat sheet (UI komponenty hotové)
- [ ] Hints a help systém
- [ ] Quiz questions
- [ ] Typing speed measurement
- [ ] Mistake tracking a analytics (základy v progress trackingu)

### Fáze 6: Advanced Features (3-4 dny)
- [ ] Adaptive learning algoritmus
- [ ] Personalized recommendations
- [ ] Export funkcionalita (.vimrc, cheat sheets)
- [ ] Statistics a reporting
- [ ] Leaderboard systém
- [ ] Plugin recommendations

### Fáze 7: Testing a Polish (2-3 dny)
- [ ] Unit testy pro core komponenty
- [ ] Integration testy
- [ ] Cross-platform testing
- [ ] Performance optimizace
- [ ] Bug fixes a refinements
- [ ] Documentation a README

### Fáze 8: Distribution (1-2 dny)
- [ ] PyPI package setup
- [ ] Installation instructions
- [ ] Docker container (optional)
- [ ] CLI man page
- [ ] Release preparation

---

## 📋 PROJEKT OVERVIEW

### Vize Projektu
VimGym je moderní, interaktivní příkazový řádek tutor pro učení Vim editoru. Kombinuje gamifikaci, personalizované učení a hands-on praxi v bezpečném simulovaném prostředí. Cílem je transformovat tradiční učení Vimu z frustrující zkušenosti na zábavné a efektivní dobrodružství.

### Hlavní Hodnoty
- **Progressivní učení**: Od úplných základů po pokročilé techniky
- **Hands-on přístup**: Učení děláním, ne čtením
- **Bezpečné prostředí**: Simulátor bez rizika ztráty dat
- **Personalizace**: Adaptivní obsah založený na výkonu
- **Gamifikace**: Achievements, progress tracking, challenges

### Target Audience

#### Primární
- **Úplní začátečníci** (40% uživatelů)
  - Nikdy nepoužili Vim
  - Přicházejí z GUI editorů (VS Code, Sublime)
  - Potřebují motivaci a strukturované vedení

#### Sekundární  
- **Současní uživatelé jiných editorů** (35% uživatelů)
  - Chtějí přejít na Vim pro produktivitu
  - Znají základy programování
  - Hledají efektivní způsob přechodu

#### Terciární
- **Občasní Vim uživatelé** (25% uživatelů)
  - Už Vim trochu znají
  - Chtějí se naučit pokročilé techniky
  - Potřebují systematické prohloubení znalostí

### Success Metrics
- **Completion Rate**: >70% uživatelů dokončí alespoň 4 moduly
- **Retention**: >50% uživatelů se vrátí po týdnu
- **Real Usage**: >60% absolventů používá Vim po měsíci
- **Satisfaction**: >4.5/5 stars user rating

---

## 🏗️ ARCHITEKTURA SYSTÉMU

### Celková Struktura Projektu
```
vimgym/
├── vimgym.py                 # Main entry point
├── setup.py                 # Package installation
├── requirements.txt         # Dependencies
├── README.md                # Project documentation
├── LICENSE                  # MIT license
├── .gitignore               # Git ignore rules
│
├── vimgym/                  # Main package
│   ├── __init__.py
│   ├── main.py              # CLI application core
│   ├── config.py            # Configuration management
│   └── constants.py         # Global constants
│
├── vimgym/core/             # Core framework
│   ├── __init__.py
│   ├── session.py           # Session management
│   ├── progress.py          # Progress tracking
│   ├── user.py              # User profiles
│   └── database.py          # JSON database operations
│
├── vimgym/ui/               # User interface
│   ├── __init__.py
│   ├── components.py        # Reusable UI components
│   ├── themes.py            # Color themes and styling
│   ├── menus.py             # Menu systems
│   └── layouts.py           # Screen layouts
│
├── vimgym/simulator/        # Vim simulator
│   ├── __init__.py
│   ├── buffer.py            # Text buffer simulation
│   ├── cursor.py            # Cursor management
│   ├── modes.py             # Vim modes (Normal, Insert, etc.)
│   ├── commands.py          # Vim command processing
│   └── validator.py         # Command validation
│
├── vimgym/modules/          # Learning modules
│   ├── __init__.py
│   ├── module_base.py       # Base class for modules
│   ├── module01_basics.py   # Module 1: Basics
│   ├── module02_movement.py # Module 2: Movement
│   ├── module03_editing.py  # Module 3: Editing
│   ├── module04_search.py   # Module 4: Search/Replace
│   ├── module05_files.py    # Module 5: File operations
│   ├── module06_advanced.py # Module 6: Advanced features
│   └── module07_config.py   # Module 7: Configuration
│
├── vimgym/features/         # Additional features
│   ├── __init__.py
│   ├── challenges.py        # Challenge system
│   ├── achievements.py      # Achievement tracking
│   ├── cheatsheet.py        # Interactive cheat sheet
│   ├── analytics.py         # Learning analytics
│   └── export.py            # Export functionality
│
├── vimgym/utils/            # Utility functions
│   ├── __init__.py
│   ├── helpers.py           # General helpers
│   ├── validators.py        # Input validation
│   └── formatters.py        # Text formatting
│
├── data/                    # Data files
│   ├── lessons/             # Lesson content (JSON/YAML)
│   ├── challenges/          # Challenge definitions
│   ├── achievements/        # Achievement definitions
│   └── templates/           # Template files
│
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_core/           # Core functionality tests
│   ├── test_simulator/      # Simulator tests
│   ├── test_modules/        # Module tests
│   └── test_integration/    # Integration tests
│
└── docs/                    # Documentation
    ├── api.md               # API documentation
    ├── contributing.md      # Contribution guidelines
    └── architecture.md      # Architecture details
```

### Klíčové Komponenty

#### 1. Session Manager
**Účel**: Správa uživatelských sessions, save/resume funkcionalita
**Klíčové funkce**:
- Automatic session saving každých 30 sekund
- Resume z přesného místa po restartu
- Multiple session slots pro různé učební paths
- Session backup a recovery

#### 2. Progress Manager
**Účel**: Tracking pokroku uživatele napříč moduly
**Klíčové funkce**:
- Granular progress tracking (per lesson, per command)
- Achievement systém s unlocking
- Statistics collection (time spent, mistakes, etc.)
- Progress visualization

#### 3. Vim Simulator
**Účel**: Bezpečná simulace Vim prostředí pro cvičení
**Klíčové funkce**:
- Faithful Vim behavior simulation
- Real-time visual feedback
- Command history a undo system
- Mode indication a state management

#### 4. Module System
**Účel**: Strukturované učební moduly s progresivní obtížností
**Klíčové funkce**:
- Prerequisite checking
- Adaptive content based na performance
- Rich multimedia lessons (text, examples, exercises)
- Self-assessment quizzes

---

## 🎨 UI/UX DESIGN

### Design Principy

#### 1. Minimalistický Interface
- Čistý, uncluttered design
- Focus na obsah, ne na dekorace
- Konzistentní spacing a typography
- Intuitivní navigace

#### 2. Progressive Disclosure
- Zobrazovat pouze relevantní informace
- Gradual unveiling pokročilých features
- Context-sensitive nápověda
- Layered complexity

#### 3. Immediate Feedback
- Real-time response na user actions
- Clear success/error indicators
- Progress visualization
- Encouraging positive reinforcement

### Color Scheme

#### Primary Palette
```
Background:    #1e1e1e (Dark Gray)
Foreground:    #d4d4d4 (Light Gray)
Primary:       #007acc (VS Code Blue)
Success:       #4ec9b0 (Mint Green)
Warning:       #ffcc02 (Yellow)
Error:         #f44747 (Red)
```

#### Secondary Palette
```
Vim Normal:    #c586c0 (Purple)
Vim Insert:    #4ec9b0 (Green)
Vim Visual:    #ffcc02 (Yellow)
Vim Command:   #569cd6 (Blue)
```

#### Syntax Highlighting
```
Keywords:      #569cd6 (Blue)
Strings:       #ce9178 (Orange)
Comments:      #6a9955 (Green)
Numbers:       #b5cea8 (Light Green)
Operators:     #d4d4d4 (White)
```

### Typography

#### Font Stack
```
Primary:   'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace
Fallback:  'Courier New', monospace
```

#### Font Sizes
```
Title:     18px (Bold)
Header:    16px (Bold)
Body:      14px (Regular)
Small:     12px (Regular)
Tiny:      10px (Regular)
```

### Layout Patterns

#### 1. Main Menu Layout
```
┌─────────────────────────────────────────────────────┐
│  🏋️ VimGym - Interactive Vim Training               │
├─────────────────────────────────────────────────────┤
│  Progress: ████████░░ 80% | Level: Intermediate     │
│                                                     │
│  📚 Modules:                                        │
│    ✅ 1. Basics & Introduction                      │
│    ✅ 2. Movement & Navigation                      │
│    ✅ 3. Text Editing                               │
│    🔄 4. Search & Replace (In Progress)             │
│    🔒 5. File Operations                            │
│    🔒 6. Advanced Features                          │
│    🔒 7. Configuration & Plugins                    │
│                                                     │
│  🎯 Quick Actions:                                  │
│    [C] Continue Current Lesson                      │
│    [P] Practice Mode                                │
│    [S] Statistics                                   │
│    [H] Help & Cheat Sheet                           │
│    [Q] Quit                                         │
│                                                     │
│  💡 Tip: Use arrow keys to navigate, Enter to select│
└─────────────────────────────────────────────────────┘
```

#### 2. Lesson Layout
```
┌─────────────────────────────────────────────────────┐
│  📖 Module 2: Movement & Navigation - Lesson 3      │
├─────────────────────────────────────────────────────┤
│  Progress: ████████░░ 80% (4/5) | Time: 12:34      │
└─────────────────────────────────────────────────────┘

🎯 Learning Objective:
Master word-level movement commands in Vim

📝 Commands to Learn:
• w - move forward by word
• b - move backward by word  
• e - move to end of word
• W, B, E - WORD variants (whitespace delimited)

┌─ VIM SIMULATOR ─────────────────────────────────────┐
│ The quick brown fox jumps over the lazy dog.       │
│ This is a sample sentence for practicing.          │
│ Try moving around with word commands.               │
│ █                                                   │
│                                                     │
│ [empty lines for practice]                          │
│                                                     │
└─────────────────────────────────────────────────────┘
Mode: NORMAL | Last Command: w | Commands Used: 3

🔥 Current Task: Move to the word "fox" using w command
💡 Hint: Count how many words to skip and use repetition

[Space] Show Hint | [Tab] Next Task | [Esc] Menu | [?] Help
```

#### 3. Challenge Layout
```
┌─────────────────────────────────────────────────────┐
│  🏆 Challenge: "Speed Editing"                      │
├─────────────────────────────────────────────────────┤
│  Time Limit: 02:30 | Score: 145/200 | Mistakes: 2  │
└─────────────────────────────────────────────────────┘

🎯 Task: Fix all syntax errors in this Python code as quickly as possible

┌─ CODE TO FIX ───────────────────────────────────────┐
│ def fibonacci(n):                                   │
│     if n <= 1                                       │
│         return n                                    │
│     else:                                           │
│         return fibonacci(n-1) + fibonacci(n-2      │
│ █                                                   │
│                                                     │
│ print(fibonacci(10)                                 │
└─────────────────────────────────────────────────────┘

✅ Fixed: Missing colon after if statement
❌ Missing: Closing parenthesis in function call
❌ Missing: Closing parenthesis in return statement

[Enter] Submit | [R] Reset | [Esc] Give Up
```

---

## 📚 MODULY A OBSAH

### Module 1: Úvod a Základy Vimu
**Doba trvání**: 30-45 minut
**Předpoklady**: Žádné

#### Lesson 1.1: Co je Vim a proč ho používat (5 min)
**Obsah**:
- Historie a filozofie Vimu
- Výhody modálního editoru
- Porovnání s GUI editory
- Motivation pro učení

**Interaktivní prvky**:
- Quiz: "Které výhody Vim nabízí?"
- Video ukázka: Speed comparison Vim vs. VS Code

#### Lesson 1.2: Spuštění a ukončení Vimu (5 min)
**Obsah**:
- `vim filename` - spuštění s souborem
- `:q` - quit (pokud není modified)
- `:q!` - force quit (discard changes)
- `:wq` - write and quit
- `:x` - write and quit (alternative)
- `ZZ` - write and quit (Normal mode)

**Praktické cvičení**:
- Simulátor: Procvičit každý způsob ukončení
- Challenge: "Escape the Vim" - ukončit Vim 5 různými způsoby

#### Lesson 1.3: Vim módy - základ všeho (10 min)
**Obsah**:
- **Normal Mode**: Výchozí mód, navigace a příkazy
- **Insert Mode**: Vkládání textu
- **Visual Mode**: Označování textu
- **Command Mode**: Ex příkazy

**Praktické cvičení**:
- Mode transition practice: N→I→N→V→N→:→N
- Visual indicators: Barevné označení aktuálního módu
- Common mistakes: Jak se nedostat "stuck" v módu

#### Lesson 1.4: Základní pohyb - hjkl (10 min)
**Obsah**:
- `h` - left (←)
- `j` - down (↓)  
- `k` - up (↑)
- `l` - right (→)
- Proč ne šipky? (efficiency, finger position)

**Praktické cvičení**:
- Navigation maze: Projít bludištěm pomocí hjkl
- Typing speed test: Měření rychlosti oproti šipkám
- Muscle memory builder: Repetitivní cvičení

#### Lesson 1.5: Základní vkládání textu (10 min)
**Obsah**:
- `i` - insert before cursor
- `a` - insert after cursor (append)
- `o` - insert new line below (open)
- `O` - insert new line above
- `I` - insert at beginning of line
- `A` - insert at end of line

**Praktické cvičení**:
- Text insertion challenge: Doplnit chybějící slova
- Position awareness: Kde se objeví text pro každý command
- Real-world simulation: Editace konfiguračního souboru

#### Assessment 1: Module Completion Test
- Multiple choice questions (10 otázek)
- Practical simulation test (5 úkolů)
- Speed test: Basic operations pod určitý time limit
- Minimum passing score: 80%

---

### Module 2: Pohyb a Navigace
**Doba trvání**: 45-60 minut  
**Předpoklady**: Module 1 completed

#### Lesson 2.1: Efektivní pohyb po řádcích (10 min)
**Obsah**:
- `0` - beginning of line
- `^` - first non-whitespace character
- `$` - end of line
- `g_` - last non-whitespace character

**Praktické cvičení**:
- Code navigation: Pohyb v indented code
- Efficiency comparison: Počet keystroků vs. šipky
- Real scenarios: Debugging session simulation

#### Lesson 2.2: Pohyb po slovech (15 min)
**Obsah**:
- `w` - next word beginning
- `b` - previous word beginning
- `e` - end of current/next word
- `W`, `B`, `E` - WORD variants (whitespace-separated)
- Rozdíl mezi word a WORD

**Praktické cvičení**:
- Word vs WORD distinction: "file.txt vs hello,world"
- Navigation efficiency: Najít target slovo nejrychleji
- Code editing: Pohyb v function names a variables

#### Lesson 2.3: Skoky a rychlá navigace (10 min)
**Obsah**:
- `gg` - go to first line
- `G` - go to last line
- `[number]G` - go to specific line number
- `Ctrl+f` - page forward
- `Ctrl+b` - page backward
- `Ctrl+d` - half page down
- `Ctrl+u` - half page up

**Praktické cvičení**:
- Large file navigation: 1000+ line file navigation
- Line number jumping: Go to specific line challenges
- Page scrolling efficiency: Navigate long documents

#### Lesson 2.4: Vyhledávání pro navigaci (10 min)
**Obsah**:
- `/pattern` - search forward
- `?pattern` - search backward  
- `n` - next match
- `N` - previous match
- `*` - search word under cursor forward
- `#` - search word under cursor backward

**Praktické cvičení**:
- Code search scenarios: Find function definitions
- Pattern matching basics: Simple regex patterns
- Search efficiency: Navigate large codebase

#### Assessment 2: Navigation Mastery
- Timed navigation challenges
- Efficiency metrics: Keystroke counting
- Real-world scenarios: Debug session simulation
- Advanced: Custom navigation patterns

---

### Module 3: Editace Textu
**Doba trvání**: 60-75 minut
**Předpoklady**: Module 2 completed

#### Lesson 3.1: Mazání textu (15 min)
**Obsah**:
- `x` - delete character under cursor
- `X` - delete character before cursor
- `dd` - delete entire line
- `dw` - delete word
- `d$` / `D` - delete to end of line
- `d0` - delete to beginning of line

**Praktické cvičení**:
- Precision deletion: Remove specific characters/words
- Line cleaning: Remove trailing whitespace
- Code refactoring: Delete unused variables

#### Lesson 3.2: Kopírování a vkládání (15 min)
**Obsah**:
- `yy` - yank (copy) entire line
- `yw` - yank word
- `y$` - yank to end of line
- `p` - paste after cursor/line
- `P` - paste before cursor/line
- Concept of "registers" (basic introduction)

**Praktické cvičení**:
- Code duplication: Copy function templates
- Text rearrangement: Move paragraphs around
- Clipboard efficiency: Multiple copy-paste operations

#### Lesson 3.3: Změny a nahrazování (15 min)
**Obsah**:
- `r` - replace single character
- `R` - replace mode (overwrite)
- `cw` - change word
- `cc` - change entire line
- `c$` / `C` - change to end of line
- `s` - substitute character (delete + insert)
- `S` - substitute line (delete line + insert)

**Praktické cvičení**:
- Variable renaming: Change variable names
- Text correction: Fix typos efficiently
- Refactoring practice: Update function signatures

#### Lesson 3.4: Undo a Redo (5 min)
**Obsah**:
- `u` - undo last change
- `Ctrl+r` - redo
- Concept of change tree
- Multiple levels of undo

**Praktické cvičení**:
- Mistake recovery: Practice making and undoing changes
- Complex editing: Multi-step edits with undo safety
- Experimentation: Try different approaches safely

#### Lesson 3.5: Kombinace s čísly (10 min)
**Obsah**:
- Number prefixes: `3dd`, `5yy`, `10x`
- Efficiency through repetition
- Common patterns: `3cw`, `2dd`, `4p`

**Praktické cvičení**:
- Bulk operations: Delete multiple lines efficiently
- Pattern recognition: When to use number prefixes
- Speed challenges: Complete tasks with minimal keystrokes

#### Assessment 3: Text Editing Proficiency
- Complex editing scenarios
- Efficiency benchmarks
- Error recovery tests
- Creative challenges: Solve editing puzzles

---

### Module 4: Vyhledávání a Nahrazování
**Doba trvání**: 45-60 minut
**Předpoklady**: Module 3 completed

#### Lesson 4.1: Pokročilé vyhledávání (15 min)
**Obsah**:
- Case sensitivity: `/\c` ignorovat case, `/\C` enforce case
- Word boundaries: `/\<word\>`
- Incremental search highlighting
- Search history: `/<Up>` pro previous searches
- Search direction switching: `n` vs `N`

#### Lesson 4.2: Základní regex patterns (20 min)
**Obsah**:
- `.` - any character
- `*` - zero or more  
- `+` - one or more
- `?` - zero or one
- `[]` - character class
- `^` - start of line
- `$` - end of line

**Praktické cvičení**:
- Email validation patterns
- Log file searching
- Code pattern matching

#### Lesson 4.3: Substituční příkazy (15 min)
**Obsah**:
- `:s/old/new/` - substitute first occurrence on line
- `:s/old/new/g` - substitute all on line  
- `:%s/old/new/g` - substitute all in file
- `:%s/old/new/gc` - substitute with confirmation
- `:s/\<word\>/replacement/g` - word boundaries

#### Lesson 4.4: Pokročilé substituční techniky (10 min)
**Obsah**:
- Capture groups: `\(` a `\)`
- Backreferences: `\1`, `\2`
- Case conversions: `\u`, `\l`, `\U`, `\L`
- Range specifiers: `:10,20s/old/new/g`

#### Assessment 4: Search & Replace Mastery
- Complex regex challenges
- Large file refactoring
- Pattern recognition tests
- Real-world scenarios

---

### Module 5: Práce se Soubory
**Doba trvání**: 30-45 minut
**Předpoklady**: Module 4 completed

#### Lesson 5.1: Otevírání a ukládání souborů (10 min)
**Obsah**:
- `:e filename` - edit file
- `:w` - write current file
- `:w filename` - write to specific file
- `:wa` - write all modified buffers
- `:sav filename` - save as

#### Lesson 5.2: Buffer management (15 min)
**Obsah**:
- `:ls` - list buffers
- `:b [number]` - switch to buffer
- `:bn` - next buffer
- `:bp` - previous buffer
- `:bd` - delete buffer
- `:ball` - open all buffers

#### Lesson 5.3: Windows a Tabs (15 min)
**Obsah**:
- `:sp` - horizontal split
- `:vsp` - vertical split
- `Ctrl+w + h/j/k/l` - navigate windows
- `:tabnew` - new tab
- `gt` / `gT` - tab navigation
- `:tabclose` - close tab

#### Assessment 5: File Management
- Multi-file editing scenarios
- Workflow efficiency tests
- Buffer juggling challenges

---

### Module 6: Pokročilé Funkce
**Doba trvání**: 75-90 minut
**Předpoklady**: Module 5 completed

#### Lesson 6.1: Visual Mode (20 min)
**Obsah**:
- `v` - character-wise visual
- `V` - line-wise visual  
- `Ctrl+v` - block-wise visual
- Visual mode operations: `d`, `y`, `c`, `>`，`<`
- `gv` - reselect last visual selection

#### Lesson 6.2: Registers a Clipboard (20 min)
**Obsah**:
- Named registers: `"a`, `"b`, `"c`
- Special registers: `"0` (yank), `""` (default)
- System clipboard: `"+` a `"*`
- Register inspection: `:reg`
- Appending to registers: `"A` (capital)

#### Lesson 6.3: Makra (20 min)
**Obsah**:
- Recording: `q[register]` ... `q`
- Playing: `@[register]`
- Repeat last macro: `@@`  
- Editing macros: Registers jsou jen text
- Macro best practices

#### Lesson 6.4: Text Objects (10 min)
**Obsah**:
- `iw` / `aw` - inner/around word
- `ip` / `ap` - inner/around paragraph
- `i"` / `a"` - inner/around quotes
- `i(` / `a(` - inner/around parentheses
- `it` / `at` - inner/around tags (HTML/XML)

#### Assessment 6: Advanced Features Mastery
- Complex macro scenarios
- Register management challenges  
- Text object manipulation tests
- Productivity measurement

---

### Module 7: Konfigurace a Pluginy
**Doba trvání**: 45-60 minut
**Předpoklady**: Module 6 completed

#### Lesson 7.1: .vimrc základy (20 min)
**Obsah**:
- Lokace .vimrc souboru
- Základní nastavení: `set number`, `set nowrap`
- Key mappings: `map`, `imap`, `nmap`
- Leader key concept
- Comments ve Vimu

#### Lesson 7.2: Must-have nastavení (15 min)
**Obsah**:
- `set hlsearch` / `set incsearch`
- `set autoindent` / `set smartindent`
- `set tabstop`, `set shiftwidth`, `set expandtab`
- `set clipboard=unnamedplus`
- `syntax enable`

#### Lesson 7.3: Plugin management (15 min)
**Obsah**:
- Plugin managers: vim-plug, Vundle, Pathogen
- Installing vim-plug
- Základní pluginy: NERDTree, fzf, airline
- Plugin configuration basics

#### Assessment 7: Configuration Master
- Custom .vimrc creation
- Plugin installation practice
- Personalization challenges
- Productivity optimization

---

## 🎮 INTERAKTIVNÍ FEATURES

### Challenge System

#### Challenge Categories

**Speed Challenges**
- Typing speed tests s Vim commands
- Navigation races
- Editing efficiency competitions
- Timed problem solving

**Accuracy Challenges**  
- Precision editing without mistakes
- Perfect command sequences
- Error-free text manipulation
- Clean code refactoring

**Creativity Challenges**
- Najít nejkratší způsob řešení
- Alternative solution exploration
- Macro optimization
- Custom workflow development

#### Achievement System

**Beginner Achievements**
- 🎯 "First Steps" - Complete Module 1
- ⚡ "Speed Demon" - 30+ WPM with hjkl
- 🎪 "Mode Master" - Switch modes 100 times
- 📝 "Text Ninja" - Edit 1000 characters

**Intermediate Achievements**
- 🔍 "Search Guru" - Master all search patterns
- 📁 "Buffer Boss" - Manage 5+ buffers simultaneously  
- 🎨 "Visual Virtuoso" - Complete all visual mode challenges
- 🔄 "Macro Wizard" - Record and use 10 different macros

**Advanced Achievements**
- 🏆 "Vim Master" - Complete all modules with >90%
- ⚡ "Lightning Fast" - 60+ WPM sustained
- 🛠️ "Configurator" - Create custom .vimrc
- 🎓 "Teacher" - Help other users (future social feature)

**Special Achievements**
- 🌟 "Perfectionist" - Complete module with 0 mistakes
- 🔥 "Streak Master" - 30-day learning streak
- 💎 "Efficiency Expert" - Average <2 keystrokes per task
- 🚀 "Plugin Pioneer" - Install and configure 5+ plugins

### Interactive Cheat Sheet

#### Organization Structure
```
📚 VimGym Cheat Sheet
├── 🎯 Basics
│   ├── Modes
│   ├── Movement (hjkl)
│   └── Insert/Exit
├── 🏃 Navigation  
│   ├── Line Movement
│   ├── Word Movement
│   └── Page Movement
├── ✂️ Editing
│   ├── Delete
│   ├── Copy/Paste
│   └── Change
├── 🔍 Search
│   ├── Basic Search
│   ├── Replace
│   └── Regex
├── 📁 Files
│   ├── Open/Save
│   ├── Buffers
│   └── Windows/Tabs
└── 🚀 Advanced
    ├── Visual Mode
    ├── Registers
    └── Macros
```

#### Interactive Features
- **Live Search**: Najít command podle popisu
- **Difficulty Filter**: Beginner/Intermediate/Advanced
- **Favorites**: Bookmark často používané commands
- **Practice Mode**: Direct jump to simulator
- **Copy to Clipboard**: Easy reference outside app

### Analytics a Progress Tracking

#### Metrics Collection
- **Commands Used**: Frequency analysis všech Vim commandů
- **Time Spent**: Per module, per lesson, total
- **Mistakes Made**: Tracking špatných příkazů
- **Speed Metrics**: Keystrokes per minute, task completion time  
- **Learning Velocity**: Rate of improvement over time
- **Difficulty Patterns**: Which concepts jsou challenging

#### Personalized Insights
- **Weak Areas**: Commands requiring more practice
- **Strength Areas**: Already mastered skills
- **Learning Style**: Visual vs. kinesthetic preferences
- **Optimal Session Length**: When performance drops
- **Recommendation Engine**: Next steps for improvement

#### Progress Visualization
```
📊 Your VimGym Progress

Overall Completion: 67% ████████████████████░░░░░░░░

Module Breakdown:
✅ Basics:        100% ████████████████████████████████
✅ Movement:      100% ████████████████████████████████  
✅ Editing:       100% ████████████████████████████████
🔄 Search:         80% ████████████████████████░░░░░░░░
⏳ Files:          45% ██████████████░░░░░░░░░░░░░░░░░░
🔒 Advanced:        0% ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
🔒 Config:          0% ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

📈 Performance Trends:
Speed:           ▲ +15 WPM (last week)
Accuracy:        ▲ +8% (last week)  
Session Length:  ► 23 min average
Consistency:     ▲ 6/7 days active

🎯 Current Goals:
• Master search & replace patterns
• Improve visual mode efficiency  
• Reduce mistake rate below 5%

💡 Recommendations:
• Practice regex patterns daily
• Try advanced movement challenges
• Review word object commands
```

---

## 🛠️ TECHNICKÁ SPECIFIKACE

### Vývojové Prostředí

#### Požadavky
- **Python**: 3.8+ (compatibility až do 3.11)
- **Terminal**: Support pro ANSI colors a UTF-8
- **OS Support**: Linux, macOS, Windows (with WSL)
- **RAM**: Minimum 512MB, recommended 1GB
- **Storage**: 50MB for application + data

#### Dependencies
```python
# Core dependencies
rich==13.7.0           # Terminal UI framework
click==8.1.7           # CLI framework  
questionary==2.0.1     # Interactive prompts
pyfiglet==1.0.2        # ASCII art headers
colorama==0.4.6        # Cross-platform colors

# Data & Configuration
pyyaml==6.0.1          # YAML config files
jsonschema==4.20.0     # Data validation
python-dateutil==2.8.2 # Date/time handling

# Testing & Development  
pytest==7.4.3         # Testing framework
pytest-cov==4.1.0     # Coverage reporting
black==23.11.0        # Code formatting
mypy==1.7.1           # Type checking

# Optional Enhancements
psutil==5.9.6         # System monitoring
keyboard==0.13.5      # Advanced key handling (optional)
```

### Databázová Architektura

#### User Profile Schema
```json
{
  "user_id": "uuid4_string",
  "username": "string",
  "created_at": "ISO_datetime",
  "last_active": "ISO_datetime",
  "preferences": {
    "theme": "dark|light",
    "animation_speed": "slow|normal|fast",
    "sound_enabled": true,
    "difficulty_preference": "adaptive|fixed",
    "session_reminder": 1440
  },
  "statistics": {
    "total_time_spent": 12345,
    "sessions_completed": 45,
    "modules_completed": 6,
    "average_session_length": 1800,
    "total_keystrokes": 50000,
    "accuracy_rate": 0.92,
    "current_wpm": 45
  }
}
```

#### Progress Schema  
```json
{
  "user_id": "uuid4_string",
  "module_progress": {
    "module_01": {
      "status": "completed|in_progress|locked",
      "completion_percentage": 100,
      "lessons_completed": [1, 2, 3, 4, 5],
      "time_spent": 2700,
      "best_score": 95,
      "attempts": 2,
      "first_completed": "ISO_datetime",
      "last_accessed": "ISO_datetime"
    }
  },
  "lesson_details": {
    "module_01_lesson_03": {
      "completion_time": 420,
      "mistakes_made": 3,
      "hints_used": 1,
      "commands_practiced": ["hjkl", "i", "a", "o"],
      "efficiency_score": 87
    }
  },
  "achievements": [
    {
      "id": "first_steps",
      "unlocked_at": "ISO_datetime",
      "progress": 100
    }
  ]
}
```

#### Session Schema
```json
{
  "session_id": "uuid4_string", 
  "user_id": "uuid4_string",
  "started_at": "ISO_datetime",
  "ended_at": "ISO_datetime",
  "current_module": "module_04",
  "current_lesson": "lesson_02",
  "current_step": 5,
  "simulator_state": {
    "buffer_content": "text content here",
    "cursor_position": [2, 15],
    "current_mode": "normal",
    "command_history": ["h", "h", "j", "i"],
    "undo_stack": ["state1", "state2"]
  },
  "auto_save": true,
  "save_interval": 30
}
```

### Simulator Engine

#### Buffer Management
```python
class VimBuffer:
    def __init__(self, content: str = ""):
        self.lines: List[str] = content.split('\n')
        self.cursor_pos: Tuple[int, int] = (0, 0)
        self.mode: VimMode = VimMode.NORMAL
        self.undo_stack: List[BufferState] = []
        self.redo_stack: List[BufferState] = []
        
    def insert_text(self, text: str) -> None:
        """Insert text at cursor position"""
        
    def delete_char(self) -> None:
        """Delete character at cursor"""
        
    def move_cursor(self, direction: Direction, count: int = 1) -> bool:
        """Move cursor with bounds checking"""
        
    def save_state(self) -> None:
        """Save current state for undo"""
```

#### Command Processing
```python
class CommandProcessor:
    def __init__(self, buffer: VimBuffer):
        self.buffer = buffer
        self.command_map = self._build_command_map()
        self.repeat_count = 1
        
    def process_key(self, key: str) -> CommandResult:
        """Process single keypress and return result"""
        
    def validate_command(self, command: str) -> ValidationResult:
        """Validate command sequence"""
        
    def get_suggestions(self, partial_command: str) -> List[str]:
        """Get command suggestions for help"""
```

#### State Management
```python
@dataclass
class SimulatorState:
    buffer_content: str
    cursor_line: int
    cursor_col: int
    mode: str
    last_command: str
    command_count: int
    registers: Dict[str, str]
    
    def to_dict(self) -> Dict:
        """Serialize state for saving"""
        
    @classmethod  
    def from_dict(cls, data: Dict) -> 'SimulatorState':
        """Deserialize state from save"""
```

### Performance Optimizations

#### Memory Management
- **Lazy Loading**: Moduly se načítají až při prvním použití
- **Buffer Limits**: Undo stack má maximum 100 states
- **Garbage Collection**: Automatic cleanup starých session dat
- **Caching**: Frequently used lesson content

#### Response Time Optimization
- **Async Operations**: Non-blocking file I/O pro save operations
- **Efficient Rendering**: Only redraw changed screen portions
- **Keyboard Handling**: Direct terminal input bez buffering delays
- **Database Indexing**: Fast user lookup a progress queries

#### Cross-Platform Compatibility
```python
# Terminal detection and optimization
def detect_terminal_capabilities():
    """Detect terminal features and optimize accordingly"""
    capabilities = {
        'colors': detect_color_support(),
        'unicode': detect_unicode_support(), 
        'size': get_terminal_size(),
        'mouse': detect_mouse_support()
    }
    return TerminalConfig(capabilities)

# Platform-specific optimizations
class PlatformAdapter:
    @staticmethod
    def get_config_path() -> Path:
        """Get platform-appropriate config directory"""
        if platform.system() == "Windows":
            return Path(os.environ['APPDATA']) / 'vimgym'
        else:
            return Path.home() / '.config' / 'vimgym'
```

---

## 🚀 IMPLEMENTAČNÍ ROADMAP

### Sprint 1: Foundation (Week 1-2)
**Goals**: Základní infrastruktura a CLI framework

**Deliverables**:
- [ ] Project structure setup
- [ ] Basic CLI menu system  
- [ ] User profile management
- [ ] Progress tracking foundation
- [ ] Configuration system
- [ ] Error handling framework

**Key Features**:
- Functional main menu
- User creation/selection
- Basic progress display
- Settings management

### Sprint 2: Simulator Core (Week 3-4)
**Goals**: Funkční Vim simulátor s básic commands

**Deliverables**:
- [ ] Text buffer implementation
- [ ] Cursor management
- [ ] Mode switching (Normal/Insert/Visual)
- [ ] Basic movement commands (hjkl)
- [ ] Insert/delete operations
- [ ] Undo/redo system

**Key Features**:
- Working text editor simulation
- Visual mode indication
- Command validation
- State persistence

### Sprint 3: Content Foundation (Week 5-6)  
**Goals**: První 3 moduly s kompletním obsahem

**Deliverables**:
- [ ] Module 1: Basics (complete)
- [ ] Module 2: Movement (complete)  
- [ ] Module 3: Editing (complete)
- [ ] Lesson progression system
- [ ] Assessment framework
- [ ] Progress tracking integration

**Key Features**:
- Structured learning path
- Interactive lessons
- Progress validation
- Achievement unlocking

### Sprint 4: Advanced Simulator (Week 7-8)
**Goals**: Pokročilé Vim funkce v simulátoru

**Deliverables**:
- [ ] Visual mode operations
- [ ] Register system
- [ ] Search functionality
- [ ] Command mode (:commands)
- [ ] Macro recording/playback
- [ ] Text objects

**Key Features**:
- Full Vim command coverage
- Advanced editing operations
- Complex text manipulation
- Real-world scenarios

### Sprint 5: Content Completion (Week 9-10)
**Goals**: Dokončení všech 7 modulů

**Deliverables**:
- [ ] Module 4: Search & Replace
- [ ] Module 5: File Operations  
- [ ] Module 6: Advanced Features
- [ ] Module 7: Configuration
- [ ] Challenge system
- [ ] Interactive cheat sheet

**Key Features**:
- Complete curriculum
- Advanced challenges
- Comprehensive reference
- Skill assessments

### Sprint 6: Polish & Features (Week 11-12)
**Goals**: UI/UX improvements a additional features

**Deliverables**:
- [ ] Advanced analytics
- [ ] Achievement system completion
- [ ] Export functionality
- [ ] Theme customization
- [ ] Performance optimization
- [ ] Cross-platform testing

**Key Features**:
- Professional UI/UX
- Rich analytics dashboard
- Personalization options
- Export capabilities

### Sprint 7: Testing & Deployment (Week 13-14)
**Goals**: Finalizace a release preparation

**Deliverables**:
- [ ] Comprehensive testing suite
- [ ] Documentation completion
- [ ] Package preparation
- [ ] Installation scripts
- [ ] Release automation
- [ ] User manual

**Key Features**:
- Production-ready code
- Easy installation
- Complete documentation
- Automated releases

---

## 📖 API DOKUMENTACE

### Core Classes

#### VimGym Main Application
```python
class VimGym:
    """Main application controller"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize application with optional config"""
        
    def run(self) -> None:
        """Start the application main loop"""
        
    def shutdown(self) -> None:
        """Clean shutdown with state saving"""
        
    @property 
    def current_user(self) -> Optional[User]:
        """Get currently active user"""
        
    def switch_user(self, user_id: str) -> bool:
        """Switch to different user profile"""
```

#### User Management
```python
class User:
    """User profile and preferences"""
    
    def __init__(self, username: str):
        self.id: str = str(uuid4())
        self.username: str = username
        self.created_at: datetime = datetime.now()
        self.preferences: UserPreferences = UserPreferences()
        self.statistics: UserStatistics = UserStatistics()
        
    def save(self) -> None:
        """Persist user data to storage"""
        
    @classmethod
    def load(cls, user_id: str) -> 'User':
        """Load user from storage"""
        
    def update_progress(self, module: str, lesson: str, score: int) -> None:
        """Update learning progress"""
```

#### Module System
```python
class LearningModule:
    """Base class for all learning modules"""
    
    def __init__(self, module_id: str, title: str):
        self.id: str = module_id
        self.title: str = title
        self.lessons: List[Lesson] = []
        self.prerequisites: List[str] = []
        
    def is_unlocked(self, user_progress: Progress) -> bool:
        """Check if user meets prerequisites"""
        
    def get_next_lesson(self, user_progress: Progress) -> Optional[Lesson]:
        """Get next incomplete lesson"""
        
    def calculate_completion(self, user_progress: Progress) -> float:
        """Calculate completion percentage"""

class Lesson:
    """Individual lesson within a module"""
    
    def __init__(self, lesson_id: str, title: str, content: LessonContent):
        self.id: str = lesson_id
        self.title: str = title
        self.content: LessonContent = content
        self.exercises: List[Exercise] = []
        
    def start(self, simulator: VimSimulator) -> LessonSession:
        """Begin lesson with simulator"""
        
    def validate_completion(self, session: LessonSession) -> AssessmentResult:
        """Check if lesson requirements are met"""
```

#### Simulator Engine
```python
class VimSimulator:
    """Core Vim behavior simulation"""
    
    def __init__(self):
        self.buffer: VimBuffer = VimBuffer()
        self.processor: CommandProcessor = CommandProcessor(self.buffer)
        self.state_history: List[SimulatorState] = []
        
    def process_input(self, key_input: str) -> SimulatorResponse:
        """Process user input and return response"""
        
    def reset(self, content: str = "") -> None:
        """Reset simulator to clean state"""
        
    def get_display_buffer(self) -> DisplayBuffer:
        """Get formatted buffer for display"""
        
    def save_checkpoint(self) -> str:
        """Save current state and return checkpoint ID"""
        
    def restore_checkpoint(self, checkpoint_id: str) -> bool:
        """Restore previous state"""
```

### Data Models

#### Progress Tracking
```python
@dataclass
class ModuleProgress:
    module_id: str
    status: Literal['locked', 'available', 'in_progress', 'completed']
    completion_percentage: float
    lessons_completed: List[str]
    best_score: Optional[int]
    time_spent: int  # seconds
    first_started: Optional[datetime]
    last_accessed: Optional[datetime]

@dataclass  
class LessonProgress:
    lesson_id: str
    attempts: int
    best_score: int
    completion_time: Optional[int]
    mistakes_made: int
    hints_used: int
    commands_practiced: List[str]
    
@dataclass
class UserStatistics:
    total_time_spent: int
    sessions_completed: int
    total_keystrokes: int
    accuracy_rate: float
    current_wpm: int
    favorite_commands: Dict[str, int]
    improvement_rate: float
```

#### Assessment System
```python
class Assessment:
    """Base assessment class"""
    
    def __init__(self, assessment_id: str, questions: List[Question]):
        self.id = assessment_id
        self.questions = questions
        self.passing_score = 80
        
    def evaluate(self, responses: List[Response]) -> AssessmentResult:
        """Evaluate user responses"""

@dataclass
class AssessmentResult:
    score: int
    passed: bool
    feedback: List[str]
    areas_for_improvement: List[str]
    time_taken: int
```

### Event System

#### Event Types
```python
class EventType(Enum):
    USER_LOGIN = "user_login"
    MODULE_STARTED = "module_started"  
    LESSON_COMPLETED = "lesson_completed"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    COMMAND_EXECUTED = "command_executed"
    MISTAKE_MADE = "mistake_made"
    SESSION_ENDED = "session_ended"

@dataclass
class Event:
    event_type: EventType
    timestamp: datetime
    user_id: str
    data: Dict[str, Any]
```

#### Event Handlers
```python
class EventBus:
    """Central event coordination"""
    
    def __init__(self):
        self.handlers: Dict[EventType, List[Callable]] = defaultdict(list)
        
    def subscribe(self, event_type: EventType, handler: Callable) -> None:
        """Subscribe handler to event type"""
        
    def publish(self, event: Event) -> None:
        """Publish event to all subscribers"""
        
    def unsubscribe(self, event_type: EventType, handler: Callable) -> None:
        """Remove handler subscription"""
```

### Plugin System (Future Extension)

```python
class Plugin:
    """Base plugin interface"""
    
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        
    def initialize(self, app: VimGym) -> None:
        """Plugin initialization"""
        
    def register_commands(self) -> Dict[str, Callable]:
        """Register custom commands"""
        
    def register_hooks(self) -> Dict[EventType, Callable]:
        """Register event hooks"""
        
class PluginManager:
    """Plugin management system"""
    
    def load_plugin(self, plugin_path: Path) -> Plugin:
        """Load plugin from file"""
        
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable loaded plugin"""
        
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable active plugin"""
```

---

## 🎨 UI COMPONENT LIBRARY

### Basic Components

#### Headers a Titles
```python
def render_main_header() -> Panel:
    """Render main application header"""
    ascii_art = pyfiglet.figlet_format("VimGym", font="slant")
    return Panel(
        ascii_art,
        border_style="bright_blue",
        title="🏋️ Interactive Vim Training",
        subtitle="Master Vim Through Practice"
    )

def render_module_header(module: LearningModule, progress: float) -> Panel:
    """Render module-specific header with progress"""
    progress_bar = Progress.from_progress(progress)
    content = f"📚 {module.title}\n{progress_bar}"
    return Panel(content, border_style="green")
```

#### Progress Displays
```python
class ProgressBar:
    """Customizable progress bar component"""
    
    def __init__(self, total: int, completed: int, width: int = 30):
        self.total = total
        self.completed = completed
        self.width = width
        
    def render(self) -> str:
        """Render progress bar as string"""
        percentage = self.completed / self.total
        filled = int(percentage * self.width)
        bar = "█" * filled + "░" * (self.width - filled)
        return f"{bar} {percentage:.0%} ({self.completed}/{self.total})"

def render_module_grid(modules: List[LearningModule], progress: Progress) -> Table:
    """Render modules as grid with status icons"""
    table = Table(show_header=False, show_edge=False)
    
    for module in modules:
        status = get_module_status(module, progress)
        icon = STATUS_ICONS[status]
        completion = calculate_completion(module, progress)
        
        table.add_row(
            f"{icon} {module.title}",
            f"{completion:.0%}",
            status.capitalize()
        )
    
    return table
```

#### Menus a Navigation
```python
class Menu:
    """Interactive menu component"""
    
    def __init__(self, title: str, options: List[MenuOption]):
        self.title = title
        self.options = options
        self.selected_index = 0
        
    def render(self) -> Panel:
        """Render menu with current selection highlighted"""
        menu_content = []
        
        for i, option in enumerate(self.options):
            if i == self.selected_index:
                style = "bold reverse"
                prefix = "→ "
            else:
                style = "dim"
                prefix = "  "
                
            menu_content.append(
                f"{prefix}[{option.key}] {option.label}",
                style=style
            )
            
        return Panel(
            "\n".join(menu_content),
            title=self.title,
            border_style="blue"
        )
        
    def handle_key(self, key: str) -> Optional[MenuOption]:
        """Handle keyboard input and return selected option"""
        # Implementation for key handling
        pass

@dataclass
class MenuOption:
    key: str
    label: str  
    action: Callable
    enabled: bool = True
```

#### Simulator Display
```python
class SimulatorDisplay:
    """Vim simulator visual component"""
    
    def __init__(self, width: int = 80, height: int = 20):
        self.width = width
        self.height = height
        
    def render(self, simulator: VimSimulator) -> Panel:
        """Render current simulator state"""
        buffer_content = self._format_buffer(simulator.buffer)
        cursor_indicator = self._render_cursor(simulator.buffer.cursor_pos)
        mode_indicator = self._render_mode(simulator.buffer.mode)
        
        content = f"{buffer_content}\n\n{mode_indicator}"
        
        return Panel(
            content,
            title="🖥️ VIM SIMULATOR",
            border_style="cyan",
            height=self.height
        )
        
    def _format_buffer(self, buffer: VimBuffer) -> str:
        """Format buffer content with cursor"""
        lines = []
        
        for line_idx, line in enumerate(buffer.lines):
            if line_idx == buffer.cursor_pos[0]:
                # Insert cursor character
                cursor_col = buffer.cursor_pos[1]
                if cursor_col < len(line):
                    line = line[:cursor_col] + "█" + line[cursor_col+1:]
                else:
                    line += "█"
            lines.append(line)
            
        return "\n".join(lines)
        
    def _render_mode(self, mode: VimMode) -> str:
        """Render mode indicator with colors"""
        mode_colors = {
            VimMode.NORMAL: "purple",
            VimMode.INSERT: "green", 
            VimMode.VISUAL: "yellow",
            VimMode.COMMAND: "blue"
        }
        
        color = mode_colors.get(mode, "white")
        return f"Mode: [{color}]{mode.name}[/{color}]"
```

### Layout Managers

#### Screen Layouts
```python
class ScreenLayout:
    """Base class for screen layouts"""
    
    def __init__(self, console: Console):
        self.console = console
        
    def render(self, **kwargs) -> None:
        """Render complete screen layout"""
        raise NotImplementedError

class LessonLayout(ScreenLayout):
    """Layout for lesson screens"""
    
    def render(self, lesson: Lesson, simulator: VimSimulator, progress: float) -> None:
        """Render lesson with simulator and progress"""
        
        # Header section (15% of screen)
        header = render_lesson_header(lesson, progress)
        
        # Content section (60% of screen)  
        content_panel = self._render_lesson_content(lesson)
        simulator_panel = SimulatorDisplay().render(simulator)
        
        content_layout = Columns([content_panel, simulator_panel])
        
        # Footer section (25% of screen)
        footer = self._render_lesson_footer(lesson)
        
        # Combine all sections
        layout = Group(header, content_layout, footer)
        
        self.console.clear()
        self.console.print(layout)
        
    def _render_lesson_content(self, lesson: Lesson) -> Panel:
        """Render lesson instructional content"""
        content = Markdown(lesson.content.instructions)
        return Panel(content, title="📖 Instructions", border_style="blue")
        
    def _render_lesson_footer(self, lesson: Lesson) -> Panel:
        """Render lesson controls and hints"""
        controls = "[Space] Hint | [Tab] Next | [Esc] Menu | [?] Help"
        return Panel(controls, border_style="dim")
```

#### Responsive Design
```python
class ResponsiveLayout:
    """Adaptive layout based on terminal size"""
    
    def __init__(self, console: Console):
        self.console = console
        self.min_width = 80
        self.min_height = 24
        
    def get_layout_mode(self) -> LayoutMode:
        """Determine layout mode based on terminal size"""
        size = self.console.size
        
        if size.width < self.min_width or size.height < self.min_height:
            return LayoutMode.COMPACT
        elif size.width > 120:
            return LayoutMode.WIDE
        else:
            return LayoutMode.STANDARD
            
    def adapt_content(self, content: Any, mode: LayoutMode) -> Any:
        """Adapt content for different layout modes"""
        if mode == LayoutMode.COMPACT:
            return self._compress_content(content)
        elif mode == LayoutMode.WIDE:
            return self._expand_content(content)
        else:
            return content

class LayoutMode(Enum):
    COMPACT = "compact"
    STANDARD = "standard"  
    WIDE = "wide"
```

---

## 🔒 SECURITY A PRIVACY

### Data Protection

#### User Data Handling
- **Local Storage Only**: Všechna user data zůstávají lokálně
- **No Cloud Sync**: Žádná data nejsou posílána na external servery
- **Encryption**: Sensitive data (pokud nějaká) jsou encrypted at rest
- **Data Minimization**: Collect pouze nezbytná data pro functionality

#### Privacy Safeguards
```python
class PrivacyManager:
    """Handle user privacy and data protection"""
    
    def __init__(self):
        self.data_retention_days = 365
        self.anonymization_enabled = True
        
    def anonymize_session_data(self, session_data: Dict) -> Dict:
        """Remove/hash personally identifiable information"""
        anonymized = session_data.copy()
        
        # Remove or hash PII
        if 'username' in anonymized:
            anonymized['username'] = self._hash_username(anonymized['username'])
            
        # Remove detailed keystroke data after aggregation
        if 'detailed_keystrokes' in anonymized:
            anonymized['aggregated_stats'] = self._aggregate_keystrokes(
                anonymized['detailed_keystrokes']
            )
            del anonymized['detailed_keystrokes']
            
        return anonymized
        
    def cleanup_old_data(self) -> None:
        """Remove data older than retention period"""
        cutoff_date = datetime.now() - timedelta(days=self.data_retention_days)
        # Implementation for cleanup
```

### Input Validation

#### Command Injection Prevention
```python
class InputValidator:
    """Validate and sanitize user input"""
    
    ALLOWED_VIM_COMMANDS = {
        'movement': ['h', 'j', 'k', 'l', 'w', 'b', 'e', '0', '$'],
        'editing': ['i', 'a', 'o', 'x', 'd', 'y', 'p'],
        'mode': ['v', 'V', 'ctrl+v'],
        'search': ['/', '?', 'n', 'N', '*', '#']
    }
    
    def validate_vim_command(self, command: str) -> ValidationResult:
        """Validate that command is safe Vim command"""
        # Strip any non-printable characters
        clean_command = ''.join(char for char in command if char.isprintable())
        
        # Check against whitelist
        if self._is_allowed_command(clean_command):
            return ValidationResult(valid=True, sanitized=clean_command)
        else:
            return ValidationResult(valid=False, reason="Command not allowed")
            
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe file operations"""
        # Remove path traversal attempts
        filename = os.path.basename(filename)
        
        # Remove special characters
        safe_chars = string.ascii_letters + string.digits + '.-_'
        sanitized = ''.join(c for c in filename if c in safe_chars)
        
        return sanitized[:255]  # Limit length

@dataclass
class ValidationResult:
    valid: bool
    sanitized: Optional[str] = None
    reason: Optional[str] = None
```

### Safe File Operations

#### Sandboxed Environment
```python
class SafeFileManager:
    """Secure file operations within sandbox"""
    
    def __init__(self, sandbox_path: Path):
        self.sandbox_path = sandbox_path.resolve()
        self.allowed_extensions = {'.txt', '.py', '.js', '.md', '.vim'}
        
    def is_safe_path(self, file_path: Path) -> bool:
        """Verify path is within sandbox"""
        try:
            resolved_path = (self.sandbox_path / file_path).resolve()
            return resolved_path.is_relative_to(self.sandbox_path)
        except (OSError, ValueError):
            return False
            
    def safe_read(self, file_path: str, max_size: int = 1024*1024) -> Optional[str]:
        """Safely read file with size limits"""
        path = Path(file_path)
        
        if not self.is_safe_path(path):
            raise SecurityError("Path outside sandbox")
            
        if path.suffix not in self.allowed_extensions:
            raise SecurityError("File type not allowed")
            
        full_path = self.sandbox_path / path
        
        if full_path.stat().st_size > max_size:
            raise SecurityError("File too large")
            
        return full_path.read_text(encoding='utf-8')
        
    def safe_write(self, file_path: str, content: str) -> bool:
        """Safely write file with validation"""
        # Similar validation as safe_read
        # Implementation with proper error handling
        pass

class SecurityError(Exception):
    """Security-related error"""
    pass
```

### Audit Logging

#### Security Event Logging
```python
class SecurityAuditor:
    """Log security-relevant events"""
    
    def __init__(self, log_path: Path):
        self.logger = self._setup_logger(log_path)
        
    def log_file_access(self, user_id: str, file_path: str, operation: str) -> None:
        """Log file access attempts"""
        self.logger.info(
            "FILE_ACCESS",
            extra={
                'user_id': user_id,
                'file_path': file_path,
                'operation': operation,
                'timestamp': datetime.now().isoformat()
            }
        )
        
    def log_invalid_input(self, user_id: str, invalid_input: str) -> None:
        """Log potentially malicious input"""
        self.logger.warning(
            "INVALID_INPUT",
            extra={
                'user_id': user_id,
                'input_hash': hashlib.sha256(invalid_input.encode()).hexdigest(),
                'timestamp': datetime.now().isoformat()
            }
        )
        
    def log_authentication_event(self, user_id: str, event_type: str) -> None:
        """Log user authentication events"""
        self.logger.info(
            "AUTH_EVENT",
            extra={
                'user_id': user_id,
                'event_type': event_type,
                'timestamp': datetime.now().isoformat()
            }
        )
```

---

## 🧪 TESTING STRATEGIE

### Unit Testing

#### Core Components
```python
# tests/test_core/test_user.py
import pytest
from vimgym.core.user import User, UserPreferences

class TestUser:
    def test_user_creation(self):
        """Test basic user creation"""
        user = User("testuser")
        assert user.username == "testuser"
        assert user.id is not None
        assert isinstance(user.preferences, UserPreferences)
        
    def test_user_serialization(self):
        """Test user data serialization/deserialization"""
        user = User("testuser")
        user_data = user.to_dict()
        
        loaded_user = User.from_dict(user_data)
        assert loaded_user.username == user.username
        assert loaded_user.id == user.id
        
    def test_progress_update(self):
        """Test progress tracking functionality"""
        user = User("testuser")
        user.update_progress("module_01", "lesson_01", 85)
        
        progress = user.get_module_progress("module_01")
        assert progress.lessons_completed == ["lesson_01"]
        assert progress.best_score == 85

# tests/test_simulator/test_vim_buffer.py
class TestVimBuffer:
    def test_cursor_movement(self):
        """Test cursor movement within bounds"""
        buffer = VimBuffer("Hello\nWorld")
        
        # Test horizontal movement
        assert buffer.move_cursor('right') == True
        assert buffer.cursor_pos == (0, 1)
        
        # Test vertical movement  
        assert buffer.move_cursor('down') == True
        assert buffer.cursor_pos == (1, 1)
        
        # Test bounds checking
        buffer.cursor_pos = (1, 4)  # End of "World"
        assert buffer.move_cursor('right') == False
        
    def test_text_insertion(self):
        """Test text insertion at cursor"""
        buffer = VimBuffer("Hello World")
        buffer.cursor_pos = (0, 5)  # After "Hello"
        
        buffer.insert_text(" Beautiful")
        assert buffer.get_line(0) == "Hello Beautiful World"
        
    def test_undo_redo(self):
        """Test undo/redo functionality"""
        buffer = VimBuffer("Original")
        buffer.save_state()
        
        buffer.insert_text(" Text")
        assert buffer.get_line(0) == "Original Text"
        
        buffer.undo()
        assert buffer.get_line(0) == "Original"
        
        buffer.redo()
        assert buffer.get_line(0) == "Original Text"
```

#### Module Testing
```python
# tests/test_modules/test_module_progression.py
class TestModuleProgression:
    def test_prerequisite_checking(self):
        """Test module prerequisite validation"""
        module2 = LearningModule("module_02", "Movement")
        module2.prerequisites = ["module_01"]
        
        # User hasn't completed module 1
        progress = Progress()
        assert module2.is_unlocked(progress) == False
        
        # User completed module 1
        progress.complete_module("module_01")
        assert module2.is_unlocked(progress) == True
        
    def test_lesson_sequencing(self):
        """Test lesson order enforcement"""
        module = LearningModule("test_module", "Test")
        lesson1 = Lesson("lesson_01", "First", LessonContent())
        lesson2 = Lesson("lesson_02", "Second", LessonContent())
        
        module.add_lesson(lesson1)
        module.add_lesson(lesson2)
        
        progress = Progress()
        
        # Should start with first lesson
        next_lesson = module.get_next_lesson(progress)
        assert next_lesson.id == "lesson_01"
        
        # Complete first lesson
        progress.complete_lesson("test_module", "lesson_01", 90)
        
        # Should now get second lesson
        next_lesson = module.get_next_lesson(progress)
        assert next_lesson.id == "lesson_02"
```

### Integration Testing

#### End-to-End Workflows
```python
# tests/test_integration/test_learning_flow.py
class TestLearningFlow:
    def test_complete_lesson_workflow(self):
        """Test complete lesson from start to finish"""
        app = VimGym()
        user = User("integration_test")
        app.set_current_user(user)
        
        # Start first module
        module = app.get_module("module_01")
        lesson = module.get_next_lesson(user.progress)
        
        # Start lesson
        session = lesson.start(app.simulator)
        assert session.status == SessionStatus.ACTIVE
        
        # Simulate user completing exercises
        for exercise in lesson.exercises:
            result = exercise.execute(app.simulator)
            session.record_exercise_result(exercise.id, result)
            
        # Complete lesson
        assessment = lesson.validate_completion(session)
        assert assessment.passed == True
        
        # Verify progress update
        user.update_progress("module_01", lesson.id, assessment.score)
        progress = user.get_lesson_progress("module_01", lesson.id)
        assert progress.completion_time > 0
        
    def test_achievement_unlocking(self):
        """Test achievement system integration"""
        app = VimGym()
        user = User("achievement_test")
        app.set_current_user(user)
        
        # Complete actions that should unlock achievement
        app.simulator.process_input("h" * 50)  # 50 left movements
        
        # Check if "Movement Master" achievement unlocked
        achievements = user.get_unlocked_achievements()
        movement_achievement = next(
            (a for a in achievements if a.id == "movement_master"), 
            None
        )
        assert movement_achievement is not None
```

#### Performance Testing
```python
# tests/test_performance/test_simulator_performance.py
import time
import pytest

class TestSimulatorPerformance:
    def test_command_processing_speed(self):
        """Test simulator can handle rapid input"""
        simulator = VimSimulator()
        commands = ["h", "j", "k", "l"] * 1000  # 4000 commands
        
        start_time = time.time()
        for command in commands:
            simulator.process_input(command)
        end_time = time.time()
        
        # Should process 4000 commands in under 1 second
        assert (end_time - start_time) < 1.0
        
    def test_memory_usage_stability(self):
        """Test memory doesn't grow excessively"""
        import psutil
        process = psutil.Process()
        
        simulator = VimSimulator()
        initial_memory = process.memory_info().rss
        
        # Simulate long session
        for _ in range(10000):
            simulator.process_input("i")
            simulator.process_input("hello")
            simulator.process_input("escape")
            simulator.process_input("u")  # undo
            
        final_memory = process.memory_info().rss
        memory_growth = final_memory - initial_memory
        
        # Memory growth should be reasonable (< 50MB)
        assert memory_growth < 50 * 1024 * 1024

    @pytest.mark.parametrize("buffer_size", [100, 1000, 10000])
    def test_large_buffer_performance(self, buffer_size):
        """Test performance with large text buffers"""
        large_text = "Line of text\n" * buffer_size
        simulator = VimSimulator()
        simulator.buffer.set_content(large_text)
        
        start_time = time.time()
        
        # Perform operations on large buffer
        simulator.process_input("G")    # Go to end
        simulator.process_input("gg")   # Go to beginning
        simulator.process_input("/text") # Search
        
        end_time = time.time()
        
        # Operations should complete in reasonable time
        assert (end_time - start_time) < 0.5
```

### Automated Testing Pipeline

#### CI/CD Configuration
```yaml
# .github/workflows/test.yml
name: VimGym Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
        
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
        
    - name: Run unit tests
      run: |
        pytest tests/test_core tests/test_simulator tests/test_modules -v
        
    - name: Run integration tests  
      run: |
        pytest tests/test_integration -v
        
    - name: Run performance tests
      run: |
        pytest tests/test_performance -v --benchmark-only
        
    - name: Generate coverage report
      run: |
        pytest --cov=vimgym --cov-report=xml
        
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

#### Test Data Management
```python
# tests/conftest.py
import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
def temp_data_dir():
    """Create temporary directory for test data"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture  
def sample_user():
    """Create sample user for testing"""
    user = User("test_user")
    # Pre-populate with some progress
    user.update_progress("module_01", "lesson_01", 85)
    user.update_progress("module_01", "lesson_02", 92)
    return user

@pytest.fixture
def configured_simulator():
    """Create configured simulator for testing"""
    simulator = VimSimulator()
    simulator.buffer.set_content("Hello World\nThis is a test\nVim is awesome")
    return simulator

# tests/test_data/sample_lessons.py
SAMPLE_LESSON_CONTENT = {
    "lesson_01": {
        "title": "Basic Movement",
        "instructions": "Learn to move with hjkl keys",
        "exercises": [
            {
                "id": "exercise_01",
                "description": "Move right 3 times",
                "expected_commands": ["l", "l", "l"],
                "validation": "cursor_at_position"
            }
        ]
    }
}
```

---

## 📦 DEPLOYMENT A DISTRIBUCE

### Package Structure

#### PyPI Package Setup
```python
# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="vimgym",
    version="1.0.0",
    author="VimGym Team",
    author_email="info@vimgym.dev",
    description="Interactive Vim training in your terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vimgym/vimgym",
    project_urls={
        "Bug Tracker": "https://github.com/vimgym/vimgym/issues",
        "Documentation": "https://vimgym.dev/docs",
        "Source Code": "https://github.com/vimgym/vimgym",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals",
        "Topic :: Text Editors",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "vimgym=vimgym.main:main",
            "vimgym-admin=vimgym.admin:main",
        ],
    },
    include_package_data=True,
    package_data={
        "vimgym": [
            "data/lessons/*.yaml",
            "data/challenges/*.yaml", 
            "data/achievements/*.yaml",
            "data/templates/*",
        ],
    },
    zip_safe=False,
)
```

#### Installation Scripts
```bash
#!/bin/bash
# install.sh - One-click installation script

set -e

echo "🏋️ Installing VimGym - Interactive Vim Training"
echo "================================================"

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8+ required, found $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Install via pip
echo "📦 Installing VimGym..."
pip3 install --user vimgym

# Verify installation
if command -v vimgym &> /dev/null; then
    echo "✅ VimGym installed successfully!"
    echo ""
    echo "🚀 Quick start:"
    echo "   vimgym          # Start training"
    echo "   vimgym --help   # Show help"
    echo ""
    echo "📚 Documentation: https://vimgym.dev/docs"
else
    echo "❌ Installation failed. Please check errors above."
    exit 1
fi
```

### Cross-Platform Distribution

#### Windows Support
```python
# vimgym/platform/windows.py
import os
import sys
from pathlib import Path

class WindowsAdapter:
    """Windows-specific adaptations"""
    
    @staticmethod
    def get_config_dir() -> Path:
        """Get Windows config directory"""
        appdata = os.environ.get('APPDATA')
        if appdata:
            return Path(appdata) / 'VimGym'
        else:
            return Path.home() / 'AppData' / 'Roaming' / 'VimGym'
            
    @staticmethod  
    def setup_terminal() -> None:
        """Configure Windows terminal for optimal display"""
        # Enable ANSI color support on Windows 10+
        if sys.platform == "win32":
            import colorama
            colorama.init()
            
        # Set UTF-8 encoding
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
            
    @staticmethod
    def check_dependencies() -> List[str]:
        """Check Windows-specific dependencies"""
        missing = []
        
        # Check if Windows Terminal or ConEmu available
        if not WindowsAdapter._has_modern_terminal():
            missing.append("Modern terminal (Windows Terminal recommended)")
            
        return missing
        
    @staticmethod
    def _has_modern_terminal() -> bool:
        """Check if running in modern terminal"""
        return (
            'WT_SESSION' in os.environ or  # Windows Terminal
            'ConEmuPID' in os.environ or   # ConEmu
            'TERM_PROGRAM' in os.environ   # Other modern terminals
        )
```

#### macOS Support
```python
# vimgym/platform/macos.py
import subprocess
from pathlib import Path

class MacOSAdapter:
    """macOS-specific adaptations"""
    
    @staticmethod
    def get_config_dir() -> Path:
        """Get macOS config directory"""
        return Path.home() / 'Library' / 'Application Support' / 'VimGym'
        
    @staticmethod
    def setup_terminal() -> None:
        """Configure macOS terminal"""
        # macOS terminals generally have good Unicode/color support
        pass
        
    @staticmethod
    def install_via_homebrew() -> bool:
        """Install via Homebrew if available"""
        try:
            subprocess.run(['brew', 'install', 'vimgym'], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
```

#### Linux Distribution
```python
# vimgym/platform/linux.py
import subprocess
import shutil
from pathlib import Path

class LinuxAdapter:
    """Linux-specific adaptations"""
    
    @staticmethod
    def get_config_dir() -> Path:
        """Get Linux config directory following XDG spec"""
        xdg_config = os.environ.get('XDG_CONFIG_HOME')
        if xdg_config:
            return Path(xdg_config) / 'vimgym'
        else:
            return Path.home() / '.config' / 'vimgym'
            
    @staticmethod
    def detect_package_manager() -> Optional[str]:
        """Detect available package manager"""
        managers = ['apt', 'yum', 'dnf', 'pacman', 'zypper']
        
        for manager in managers:
            if shutil.which(manager):
                return manager
                
        return None
        
    @staticmethod
    def install_via_package_manager(manager: str) -> bool:
        """Install via detected package manager"""
        commands = {
            'apt': ['sudo', 'apt', 'install', 'python3-pip'],
            'yum': ['sudo', 'yum', 'install', 'python3-pip'],
            'dnf': ['sudo', 'dnf', 'install', 'python3-pip'],
            'pacman': ['sudo', 'pacman', '-S', 'python-pip'],
            'zypper': ['sudo', 'zypper', 'install', 'python3-pip']
        }
        
        if manager in commands:
            try:
                subprocess.run(commands[manager], check=True)
                return True
            except subprocess.CalledProcessError:
                return False
                
        return False
```

### Docker Support

#### Dockerfile
```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm-256color

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash vimuser

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install VimGym
RUN pip install -e .

# Create data directory with proper permissions
RUN mkdir -p /home/vimuser/.config/vimgym && \
    chown -R vimuser:vimuser /home/vimuser/.config

# Switch to non-root user
USER vimuser

# Set up environment
ENV HOME=/home/vimuser
ENV XDG_CONFIG_HOME=/home/vimuser/.config

# Default command
CMD ["vimgym"]
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  vimgym:
    build: .
    stdin_open: true
    tty: true
    volumes:
      - vimgym_data:/home/vimuser/.config/vimgym
    environment:
      - TERM=xterm-256color
      - COLORTERM=truecolor
    networks:
      - vimgym_network

  vimgym-dev:
    build: 
      context: .
      dockerfile: Dockerfile.dev
    stdin_open: true
    tty: true
    volumes:
      - .:/app
      - vimgym_dev_data:/home/vimuser/.config/vimgym
    environment:
      - TERM=xterm-256color
      - COLORTERM=truecolor
      - VIMGYM_DEV_MODE=1

volumes:
  vimgym_data:
  vimgym_dev_data:

networks:
  vimgym_network:
    driver: bridge
```

### Release Automation

#### GitHub Actions Release
```yaml
# .github/workflows/release.yml
name: Release VimGym

on:
  push:
    tags:
      - 'v*'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    - name: Run tests
      run: pytest
      
  build-and-publish:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
        
    - name: Install build dependencies
      run: |
        pip install build twine
        
    - name: Build package
      run: python -m build
      
    - name: Check package
      run: twine check dist/*
      
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
      
    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: VimGym ${{ github.ref }}
        draft: false
        prerelease: false
```

#### Version Management
```python
# vimgym/_version.py
"""Version management for VimGym"""

__version__ = "1.0.0"

def get_version() -> str:
    """Get current version string"""
    return __version__

def get_version_info() -> tuple:
    """Get version as tuple for comparison"""
    return tuple(map(int, __version__.split('.')))

def check_for_updates() -> Optional[str]:
    """Check if newer version is available"""
    try:
        import requests
        response = requests.get("https://pypi.org/pypi/vimgym/json", timeout=5)
        data = response.json()
        latest_version = data['info']['version']
        
        if get_version_info() < tuple(map(int, latest_version.split('.'))):
            return latest_version
    except:
        pass  # Fail silently
        
    return None
```

---

Dokument pokračuje dalšími sekcemi včetně údržby, metriky úspěchu, budoucích rozšíření a kompletní reference API. Celkový obsah by měl pokrýt více než 50 stránek detailní dokumentace o každém aspektu VimGym aplikace.