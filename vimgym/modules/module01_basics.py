"""
Module 1: Vim Basics & Introduction
Learn the fundamental concepts of Vim and basic operations.
"""

from .base import LearningModule, Lesson, LessonContent, Exercise


class Module01Basics(LearningModule):
    """Module 1: Introduction to Vim basics."""
    
    def __init__(self):
        super().__init__(
            module_id="module_01",
            title="Vim Basics & Introduction",
            description="Learn the fundamental concepts of Vim and basic operations"
        )
        self.estimated_duration = 45  # minutes
        self.prerequisites = []  # No prerequisites for first module
    
    def initialize_content(self) -> None:
        """Initialize all lessons for this module."""
        self.add_lesson(self._create_lesson_01())
        self.add_lesson(self._create_lesson_02())
        self.add_lesson(self._create_lesson_03())
        self.add_lesson(self._create_lesson_04())
        self.add_lesson(self._create_lesson_05())
    
    def _create_lesson_01(self) -> Lesson:
        """Lesson 1.1: What is Vim and Why Use It?"""
        content = LessonContent(
            title="What is Vim and Why Use It?",
            description="Introduction to Vim philosophy and advantages",
            learning_objectives=[
                "Understand what Vim is and its history",
                "Learn the advantages of modal editing",
                "Compare Vim with other editors",
                "Get motivated to learn Vim"
            ],
            introduction="""
# Welcome to VimGym! 🏋️

Vim (Vi Improved) is a powerful text editor that has been helping developers 
write code efficiently for decades. Unlike traditional editors, Vim uses a 
"modal" approach where different modes serve different purposes.

## Why Learn Vim?

1. **Speed**: Once mastered, Vim allows incredibly fast text editing
2. **Ubiquity**: Vim is available on virtually every system
3. **Efficiency**: Minimal hand movement, maximum productivity
4. **Customization**: Extremely configurable and extensible
5. **Longevity**: Skills that last a career

Let's start your journey to Vim mastery!
            """,
            instructions="""
This is an introductory lesson with no hands-on exercises. 
Read through the content and proceed when ready.

**Key Concepts to Remember:**
- Vim is a modal editor (different modes for different tasks)
- Normal mode is for navigation and commands
- Insert mode is for typing text
- Efficiency comes from keeping hands on home row
            """,
            exercises=[
                Exercise(
                    id="intro_understanding",
                    title="Understanding Check",
                    description="Simple check that you've read the introduction",
                    instructions="Press any key to confirm you understand the Vim philosophy",
                    expected_commands=["k"],  # Any key will work, we'll be flexible
                    validation_type="commands",
                    hints=["Press any key to continue", "Try pressing 'k' or any other key"]
                )
            ],
            summary="""
You've completed the introduction! Key takeaways:

✅ Vim is a modal editor with different modes for different tasks
✅ The main advantage is efficiency through minimal hand movement  
✅ Vim skills are valuable and long-lasting
✅ The learning curve is steep but worth it

Next, we'll learn how to start and exit Vim safely.
            """,
            tips=[
                "Don't worry about memorizing everything - focus on understanding concepts",
                "Practice is key - you'll build muscle memory over time",
                "It's normal to feel slow at first - everyone goes through this"
            ]
        )
        
        return Lesson("lesson_01_01", content)
    
    def _create_lesson_02(self) -> Lesson:
        """Lesson 1.2: Starting and Exiting Vim"""
        content = LessonContent(
            title="Starting and Exiting Vim",
            description="Learn how to safely enter and exit Vim",
            learning_objectives=[
                "Know how to start Vim",
                "Master different ways to exit Vim",
                "Understand the difference between :q, :q!, and :wq",
                "Never get 'trapped' in Vim again"
            ],
            introduction="""
# Starting and Exiting Vim

One of the most important skills in Vim is knowing how to exit it! 
This lesson will teach you several ways to safely leave Vim.

## Common Exit Commands:
- `:q` - Quit (if no changes made)
- `:q!` - Force quit (discard changes)  
- `:wq` - Write and quit (save changes)
- `:x` - Write and quit (alternative)
- `ZZ` - Write and quit (from Normal mode)
            """,
            instructions="""
Practice the different exit commands. Each exercise will guide you through 
a specific exit scenario.

**Remember:** 
- All `:` commands require pressing Enter
- If you see "No write since last change", use `:q!` or `:wq`
            """,
            exercises=[
                Exercise(
                    id="basic_quit",
                    title="Basic Quit",
                    description="Practice quitting when no changes were made",
                    instructions="Type ':q' and press Enter to quit Vim",
                    expected_commands=[":", "q"],
                    validation_type="commands",
                    hints=[
                        "Type the colon (:) first",
                        "Then type 'q' for quit",
                        "Don't forget to press Enter!"
                    ]
                ),
                Exercise(
                    id="force_quit",
                    title="Force Quit", 
                    description="Practice force quitting to discard changes",
                    instructions="Type ':q!' and press Enter to force quit",
                    expected_commands=[":", "q", "!"],
                    validation_type="commands",
                    hints=[
                        "Type colon (:) first",
                        "Then 'q!' to force quit",
                        "The exclamation mark discards any changes"
                    ]
                ),
                Exercise(
                    id="save_and_quit",
                    title="Save and Quit",
                    description="Practice saving changes and quitting",
                    instructions="Type ':wq' and press Enter to save and quit",
                    expected_commands=[":", "w", "q"],
                    validation_type="commands", 
                    hints=[
                        "Type colon (:) first",
                        "Then 'wq' - w for write, q for quit",
                        "This saves any changes you made"
                    ]
                ),
                Exercise(
                    id="normal_mode_quit",
                    title="Normal Mode Quit",
                    description="Practice the ZZ command to save and quit",
                    instructions="Type 'ZZ' (capital Z twice) to save and quit",
                    expected_commands=["Z", "Z"],
                    validation_type="commands",
                    hints=[
                        "Press Shift+Z twice (capital ZZ)",
                        "This works from Normal mode without :",
                        "It's equivalent to :wq"
                    ]
                )
            ],
            summary="""
Excellent! You now know how to exit Vim safely. Remember:

✅ `:q` - Clean quit (no changes)
✅ `:q!` - Force quit (discard changes)  
✅ `:wq` - Save and quit
✅ `ZZ` - Save and quit (from Normal mode)

You'll never be trapped in Vim again!
            """,
            tips=[
                "When in doubt, try :q first - Vim will warn you if there are unsaved changes",
                "Use :q! only when you're sure you want to lose your changes",
                "ZZ is faster than :wq for save-and-quit"
            ],
            common_mistakes=[
                "Forgetting to press Enter after : commands",
                "Trying to use exit commands while in Insert mode",
                "Using :q when there are unsaved changes (use :wq or :q!)"
            ]
        )
        
        return Lesson("lesson_01_02", content)
    
    def _create_lesson_03(self) -> Lesson:
        """Lesson 1.3: Vim Modes - The Foundation"""
        content = LessonContent(
            title="Vim Modes - The Foundation",
            description="Understanding Vim's modal nature",
            learning_objectives=[
                "Understand what modal editing means",
                "Learn the four main Vim modes",
                "Practice switching between modes",
                "Recognize mode indicators"
            ],
            introduction="""
# Vim Modes - The Heart of Vim

Vim's power comes from its modal nature. Unlike other editors where 
every keystroke inserts text, Vim has different modes for different tasks.

## The Four Main Modes:

1. **Normal Mode** - Navigation and commands (default)
2. **Insert Mode** - Typing text  
3. **Visual Mode** - Selecting text
4. **Command Mode** - Ex commands (starting with :)

## Mode Transitions:
- `Esc` - Always returns to Normal mode
- `i` - Enter Insert mode
- `v` - Enter Visual mode
- `:` - Enter Command mode
            """,
            instructions="""
Practice switching between different modes. Pay attention to the 
mode indicator at the bottom of the screen.

**Key Points:**
- Normal mode is your "home base"
- Esc key always brings you back to Normal mode
- Each mode has different purposes and commands
            """,
            exercises=[
                Exercise(
                    id="normal_to_insert",
                    title="Normal to Insert Mode",
                    description="Practice entering Insert mode",
                    instructions="Press 'i' to enter Insert mode",
                    expected_commands=["i"],
                    validation_type="commands",
                    hints=[
                        "Simply press the 'i' key",
                        "Watch the mode indicator change to INSERT",
                        "Now you can type text normally"
                    ]
                ),
                Exercise(
                    id="insert_to_normal",
                    title="Insert to Normal Mode", 
                    description="Practice returning to Normal mode",
                    instructions="Press Escape to return to Normal mode",
                    expected_commands=["<Esc>"],
                    validation_type="commands",
                    hints=[
                        "Press the Escape key",
                        "This works from any mode to return to Normal",
                        "Escape is your 'safety' key in Vim"
                    ]
                ),
                Exercise(
                    id="visual_mode",
                    title="Enter Visual Mode",
                    description="Practice entering Visual mode for text selection",
                    instructions="Press 'v' to enter Visual mode",
                    expected_commands=["v"],
                    validation_type="commands",
                    hints=[
                        "Press the 'v' key from Normal mode",
                        "Visual mode lets you select text",
                        "The mode indicator will show VISUAL"
                    ]
                ),
                Exercise(
                    id="command_mode",
                    title="Enter Command Mode",
                    description="Practice entering Command mode",
                    instructions="Press ':' to enter Command mode",
                    expected_commands=[":"],
                    validation_type="commands", 
                    hints=[
                        "Press the colon (:) key",
                        "This opens the command line at the bottom",
                        "You can type ex commands here"
                    ]
                ),
                Exercise(
                    id="mode_cycle",
                    title="Mode Cycling Practice",
                    description="Cycle through different modes",
                    instructions="Go: Normal → Insert → Normal → Visual → Normal → Command → Normal",
                    expected_commands=["i", "<Esc>", "v", "<Esc>", ":", "<Esc>"],
                    validation_type="commands",
                    hints=[
                        "Start with 'i' for Insert mode",
                        "Use Escape to return to Normal mode between switches",
                        "Remember: i, Esc, v, Esc, :, Esc"
                    ]
                )
            ],
            summary="""
Great! You understand Vim's modal system:

✅ **Normal Mode** - Navigation and commands (your home base)
✅ **Insert Mode** - For typing text (press 'i')
✅ **Visual Mode** - For selecting text (press 'v') 
✅ **Command Mode** - For ex commands (press ':')
✅ **Escape** - Always returns to Normal mode

This modal system is what makes Vim so powerful and efficient!
            """,
            tips=[
                "Spend most of your time in Normal mode - it's the most powerful",
                "Use Insert mode only when you need to type new text",
                "Escape is your best friend - use it whenever you're unsure",
                "Watch the mode indicator to always know where you are"
            ]
        )
        
        return Lesson("lesson_01_03", content)
    
    def _create_lesson_04(self) -> Lesson:
        """Lesson 1.4: Basic Movement - hjkl"""
        content = LessonContent(
            title="Basic Movement - hjkl",
            description="Master the fundamental movement keys",
            learning_objectives=[
                "Learn the hjkl movement keys",
                "Understand why hjkl instead of arrow keys",
                "Build muscle memory for basic navigation",
                "Move efficiently without leaving home row"
            ],
            introduction="""
# Basic Movement - hjkl

In Vim, you navigate using the hjkl keys instead of arrow keys. 
This keeps your hands on the home row for maximum efficiency.

## The Movement Keys:
```
    k
    ↑
h ← + → l
    ↓  
    j
```

- `h` - Move left (←)
- `j` - Move down (↓)  
- `k` - Move up (↑)
- `l` - Move right (→)

## Why hjkl?
- Keeps hands on home row
- Faster than reaching for arrow keys
- Available on all keyboards
- Part of Vi tradition since 1976!
            """,
            instructions="""
Practice moving around the text using hjkl keys. Notice how much faster 
it is than moving your hand to the arrow keys.

**Tips:**
- Start slowly and focus on accuracy
- Use the mnemonic: j looks like down arrow, k is up
- Don't use arrow keys - build the hjkl habit!
            """,
            exercises=[
                Exercise(
                    id="move_right",
                    title="Move Right",
                    description="Practice moving right with 'l'",
                    instructions="Move right 3 positions using 'l'",
                    expected_commands=["l", "l", "l"],
                    initial_text="Hello World! This is practice text for movement.",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 3)},
                    hints=[
                        "Press 'l' to move right",
                        "Press it three times total",
                        "Think 'l' for 'light' or 'left-to-right'"
                    ]
                ),
                Exercise(
                    id="move_down",
                    title="Move Down",
                    description="Practice moving down with 'j'",
                    instructions="Move down 2 lines using 'j'",
                    expected_commands=["j", "j"],
                    initial_text="Line 1: Start here\nLine 2: Middle line\nLine 3: Target line\nLine 4: Bottom line",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (2, 0)},
                    hints=[
                        "Press 'j' to move down",
                        "Press it twice to reach line 3",
                        "Think 'j' looks like a down arrow"
                    ]
                ),
                Exercise(
                    id="move_up",
                    title="Move Up",
                    description="Practice moving up with 'k'",
                    instructions="Move up 1 line using 'k'",
                    expected_commands=["k"],
                    initial_text="Line 1: Target line\nLine 2: Start here\nLine 3: Bottom line",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 0)},
                    hints=[
                        "Press 'k' to move up",
                        "One press should get you to line 1",
                        "Think 'k' for 'up' (it's above j)"
                    ]
                ),
                Exercise(
                    id="move_left",
                    title="Move Left",
                    description="Practice moving left with 'h'",
                    instructions="Move left 4 positions using 'h'",
                    expected_commands=["h", "h", "h", "h"],
                    initial_text="    Start here and move left",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 0)},
                    hints=[
                        "Press 'h' to move left",
                        "Press it four times total",
                        "Think 'h' is on the left side of hjkl"
                    ]
                ),
                Exercise(
                    id="navigation_combo",
                    title="Navigation Combination",
                    description="Navigate to a specific position",
                    instructions="Navigate to the word 'target' using hjkl",
                    expected_commands=["j", "j", "l", "l", "l", "l", "l"],
                    initial_text="Start at the beginning\nSecond line here\nLook target is here\nFinal line",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (2, 5)},
                    hints=[
                        "First move down to line 3 (jj)",
                        "Then move right to the 't' in 'target' (lllll)",
                        "Combine: j, j, l, l, l, l, l"
                    ]
                )
            ],
            summary="""
Excellent navigation practice! You've learned:

✅ `h` - Move left (←)
✅ `j` - Move down (↓)  
✅ `k` - Move up (↑)
✅ `l` - Move right (→)
✅ How to combine movements for precise navigation

These keys will become second nature with practice!
            """,
            tips=[
                "Practice hjkl in your spare time - even outside of code",
                "Resist the urge to use arrow keys - build the muscle memory",
                "Start with individual movements, then combine them",
                "Speed comes naturally after accuracy"
            ],
            common_mistakes=[
                "Confusing j (down) and k (up) - remember j looks like a down arrow",
                "Using arrow keys out of habit - force yourself to use hjkl",
                "Going too fast initially - accuracy first, speed later"
            ]
        )
        
        return Lesson("lesson_01_04", content)
    
    def _create_lesson_05(self) -> Lesson:
        """Lesson 1.5: Basic Text Insertion"""
        content = LessonContent(
            title="Basic Text Insertion",
            description="Learn the fundamental ways to insert text in Vim",
            learning_objectives=[
                "Master different ways to enter Insert mode",
                "Understand the difference between i, a, o, and other commands",
                "Practice positioning cursor before inserting text",
                "Build efficiency in text insertion"
            ],
            introduction="""
# Basic Text Insertion

Vim offers several ways to enter Insert mode, each positioning your 
cursor differently. Choosing the right one saves time and keystrokes.

## Insert Mode Commands:
- `i` - Insert before cursor
- `a` - Insert after cursor (append)
- `o` - Insert on new line below (open)
- `O` - Insert on new line above  
- `I` - Insert at beginning of line
- `A` - Insert at end of line

## The Pattern:
- Lowercase (i, a, o) = Local positioning
- Uppercase (I, A, O) = Line-based positioning
            """,
            instructions="""
Practice the different insertion commands. Notice how each positions 
the cursor differently before entering Insert mode.

**Remember:**
- Use Escape to return to Normal mode after each exercise
- Choose the most efficient insertion command for the task
            """,
            exercises=[
                Exercise(
                    id="insert_before",
                    title="Insert Before Cursor",
                    description="Practice inserting before the cursor position",
                    instructions="Use 'i' to insert 'Hello ' before 'World'",
                    expected_commands=["i", "H", "e", "l", "l", "o", " ", "<Esc>"],
                    initial_text="World",
                    validation_type="text_content",
                    validation_params={"expected_text": "Hello World"},
                    hints=[
                        "Press 'i' to enter Insert mode before the cursor",
                        "Type 'Hello ' (with a space)",
                        "Press Escape when done"
                    ]
                ),
                Exercise(
                    id="append_after",
                    title="Append After Cursor",
                    description="Practice appending after the cursor position",
                    instructions="Use 'a' to append ' World' after 'Hello'",
                    expected_commands=["a", " ", "W", "o", "r", "l", "d", "<Esc>"],
                    initial_text="Hello",
                    validation_type="text_content",
                    validation_params={"expected_text": "Hello World"},
                    hints=[
                        "Press 'a' to enter Insert mode after the cursor",
                        "Type ' World' (with a space before)",
                        "Press Escape when done"
                    ]
                ),
                Exercise(
                    id="open_below",
                    title="Open Line Below",
                    description="Practice opening a new line below",
                    instructions="Use 'o' to open a new line and type 'Second line'",
                    expected_commands=["o", "S", "e", "c", "o", "n", "d", " ", "l", "i", "n", "e", "<Esc>"],
                    initial_text="First line",
                    validation_type="text_content",
                    validation_params={"expected_text": "First line\nSecond line"},
                    hints=[
                        "Press 'o' to open a new line below the current line",
                        "Type 'Second line'",
                        "Press Escape when done"
                    ]
                ),
                Exercise(
                    id="open_above",
                    title="Open Line Above",
                    description="Practice opening a new line above",
                    instructions="Use 'O' to open a line above and type 'First line'",
                    expected_commands=["O", "F", "i", "r", "s", "t", " ", "l", "i", "n", "e", "<Esc>"],
                    initial_text="Second line",
                    validation_type="text_content",
                    validation_params={"expected_text": "First line\nSecond line"},
                    hints=[
                        "Press 'O' (capital O) to open a new line above",
                        "Type 'First line'",
                        "Press Escape when done"
                    ]
                ),
                Exercise(
                    id="insert_beginning",
                    title="Insert at Line Beginning",
                    description="Practice inserting at the beginning of a line",
                    instructions="Use 'I' to insert 'Start: ' at the beginning",
                    expected_commands=["I", "S", "t", "a", "r", "t", ":", " ", "<Esc>"],
                    initial_text="    some text here",
                    validation_type="text_content",
                    validation_params={"expected_text": "Start:     some text here"},
                    hints=[
                        "Press 'I' (capital I) to go to the beginning of the line",
                        "Type 'Start: '",
                        "Press Escape when done"
                    ]
                ),
                Exercise(
                    id="append_end",
                    title="Append at Line End",
                    description="Practice appending at the end of a line",
                    instructions="Use 'A' to append ' - End' at the line end",
                    expected_commands=["A", " ", "-", " ", "E", "n", "d", "<Esc>"],
                    initial_text="Some text",
                    validation_type="text_content",
                    validation_params={"expected_text": "Some text - End"},
                    hints=[
                        "Press 'A' (capital A) to go to the end of the line",
                        "Type ' - End'",
                        "Press Escape when done"
                    ]
                )
            ],
            summary="""
Perfect! You've mastered text insertion in Vim:

✅ `i` - Insert before cursor
✅ `a` - Append after cursor  
✅ `o` - Open new line below
✅ `O` - Open new line above
✅ `I` - Insert at line beginning
✅ `A` - Append at line end

Choose the most efficient command for each situation!
            """,
            tips=[
                "Use 'A' instead of moving to end and pressing 'a'",
                "Use 'o' or 'O' instead of navigating to line end/beginning",
                "Capital letters (I, A, O) work at line level",
                "Always return to Normal mode when done inserting"
            ],
            common_mistakes=[
                "Forgetting to press Escape after inserting text",
                "Using 'i' when 'a' would be more efficient",
                "Not utilizing 'o' and 'O' for new lines",
                "Moving cursor manually instead of using I/A"
            ]
        )
        
        return Lesson("lesson_01_05", content)