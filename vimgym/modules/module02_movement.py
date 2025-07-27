"""
Module 2: Movement & Navigation
Master efficient movement and navigation in Vim.
"""

from .base import LearningModule, Lesson, LessonContent, Exercise


class Module02Movement(LearningModule):
    """Module 2: Advanced movement and navigation."""
    
    def __init__(self):
        super().__init__(
            module_id="module_02",
            title="Movement & Navigation",
            description="Master efficient movement and navigation techniques in Vim"
        )
        self.estimated_duration = 60  # minutes
        self.prerequisites = ["module_01"]  # Requires Module 1 completion
    
    def initialize_content(self) -> None:
        """Initialize all lessons for this module."""
        self.add_lesson(self._create_lesson_01())
        self.add_lesson(self._create_lesson_02())
        self.add_lesson(self._create_lesson_03())
        self.add_lesson(self._create_lesson_04())
    
    def _create_lesson_01(self) -> Lesson:
        """Lesson 2.1: Efficient Line Movement"""
        content = LessonContent(
            title="Efficient Line Movement",
            description="Navigate within lines like a pro",
            learning_objectives=[
                "Master line-based movement commands",
                "Understand the difference between 0, ^, $, and g_",
                "Navigate efficiently within code lines",
                "Build speed in horizontal navigation"
            ],
            introduction="""
# Efficient Line Movement

Moving efficiently within a line is crucial for fast editing. 
Vim provides several commands that are much faster than using hjkl repeatedly.

## Line Movement Commands:
- `0` - Beginning of line (column 0)
- `^` - First non-whitespace character
- `$` - End of line
- `g_` - Last non-whitespace character

## When to Use Which:
- Use `^` instead of `0` for indented code
- Use `g_` instead of `$` to avoid trailing spaces
- Use `0` and `$` for absolute positioning
            """,
            instructions="""
Practice navigating within lines using these efficient movement commands. 
Notice how much faster they are than using 'l' and 'h' repeatedly.

**Code Context:**
You'll be working with typical code that has indentation and trailing spaces.
            """,
            exercises=[
                Exercise(
                    id="beginning_of_line",
                    title="Beginning of Line",
                    description="Move to the absolute beginning of line",
                    instructions="Use '0' to move to column 0",
                    expected_commands=["0"],
                    initial_text="    def hello_world():",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 0)},
                    hints=[
                        "Press '0' (zero) to go to column 0",
                        "This moves to the very beginning, before indentation",
                        "Useful for absolute positioning"
                    ]
                ),
                Exercise(
                    id="first_nonwhite",
                    title="First Non-whitespace",
                    description="Move to the first actual character",
                    instructions="Use '^' to move to the first non-whitespace character",
                    expected_commands=["^"],
                    initial_text="    def hello_world():",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 4)},
                    hints=[
                        "Press '^' to move to first non-whitespace",
                        "This skips the indentation spaces",
                        "More useful than '0' for code editing"
                    ]
                ),
                Exercise(
                    id="end_of_line",
                    title="End of Line",
                    description="Move to the end of the line",
                    instructions="Use '$' to move to the end of line",
                    expected_commands=["$"],
                    initial_text="    print('Hello, World!')",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 25)},
                    hints=[
                        "Press '$' to move to end of line",
                        "This goes to the last character",
                        "Think of '$' as 'end' in regex"
                    ]
                ),
                Exercise(
                    id="last_nonwhite",
                    title="Last Non-whitespace",
                    description="Move to the last actual character",
                    instructions="Use 'g_' to move to the last non-whitespace character",
                    expected_commands=["g", "_"],
                    initial_text="    return True    ",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 15)},
                    hints=[
                        "Press 'g' then '_' (g_)",
                        "This skips trailing whitespace",
                        "Useful when lines have trailing spaces"
                    ]
                ),
                Exercise(
                    id="line_navigation_combo",
                    title="Line Navigation Combination",
                    description="Practice combining line movements",
                    instructions="Navigate: start → first char → end → beginning",
                    expected_commands=["^", "$", "0"],
                    initial_text="        if condition == True:",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 0)},
                    hints=[
                        "Start with '^' to go to first character",
                        "Then '$' to go to end",
                        "Finally '0' to go to beginning"
                    ]
                )
            ],
            summary="""
Great! You've mastered line movement:

✅ `0` - Beginning of line (absolute)
✅ `^` - First non-whitespace character  
✅ `$` - End of line
✅ `g_` - Last non-whitespace character

These commands save countless keystrokes compared to hjkl!
            """,
            tips=[
                "Use '^' more often than '0' when coding",
                "Use 'g_' to avoid trailing whitespace issues",
                "Combine these with other commands for powerful editing",
                "Practice until these become automatic"
            ]
        )
        
        return Lesson("lesson_02_01", content)
    
    def _create_lesson_02(self) -> Lesson:
        """Lesson 2.2: Word Movement"""
        content = LessonContent(
            title="Word Movement",
            description="Navigate by words for efficient text traversal",
            learning_objectives=[
                "Master word-based movement commands",
                "Understand the difference between word and WORD",
                "Navigate efficiently through code and text",
                "Use word movement for faster editing"
            ],
            introduction="""
# Word Movement

Moving by words is much faster than character-by-character movement. 
Vim distinguishes between 'word' and 'WORD' for different contexts.

## Word Movement Commands:
- `w` - Next word beginning
- `b` - Previous word beginning  
- `e` - End of current/next word
- `W` - Next WORD beginning (whitespace-separated)
- `B` - Previous WORD beginning
- `E` - End of current/next WORD

## Word vs WORD:
- **word**: Separated by punctuation or whitespace
- **WORD**: Separated only by whitespace

Examples:
- `hello.world` = 3 words (`hello`, `.`, `world`)
- `hello.world` = 1 WORD (`hello.world`)
            """,
            instructions="""
Practice word movement commands on different types of text. 
Pay attention to how 'word' and 'WORD' behave differently.

**Test Cases:**
- Code with punctuation
- Filenames and paths
- Regular sentences
            """,
            exercises=[
                Exercise(
                    id="word_forward",
                    title="Move Forward by Word",
                    description="Navigate forward using word movement",
                    instructions="Use 'w' to move to the beginning of 'function'",
                    expected_commands=["w", "w", "w"],
                    initial_text="def my_function(param):",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 7)},
                    hints=[
                        "Press 'w' to move to next word beginning",
                        "Need to press it 3 times: my → function → (",
                        "Words are separated by underscores and punctuation"
                    ]
                ),
                Exercise(
                    id="word_backward",
                    title="Move Backward by Word",
                    description="Navigate backward using word movement",
                    instructions="Use 'b' to move back to 'my'",
                    expected_commands=["b", "b"],
                    initial_text="def my_function(param):",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 4)},
                    hints=[
                        "Press 'b' to move to previous word beginning",
                        "Need to press it twice from 'function'",
                        "b moves backward through words"
                    ]
                ),
                Exercise(
                    id="word_end",
                    title="Move to Word End",
                    description="Navigate to word endings",
                    instructions="Use 'e' to move to the end of 'function'",
                    expected_commands=["e", "e", "e"],
                    initial_text="def my_function(param):",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 14)},
                    hints=[
                        "Press 'e' to move to end of current/next word",
                        "Need to press it 3 times to reach end of 'function'",
                        "e goes to the last character of words"
                    ]
                ),
                Exercise(
                    id="WORD_movement",
                    title="WORD Movement",
                    description="Navigate using WORD (whitespace-separated)",
                    instructions="Use 'W' to move to 'config.json'",
                    expected_commands=["W"],
                    initial_text="filename=/path/to/config.json settings",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 20)},
                    hints=[
                        "Press 'W' (capital) to move by WORD",
                        "WORD treats punctuation as part of the word",
                        "Only one 'W' needed to jump to 'config.json'"
                    ]
                ),
                Exercise(
                    id="mixed_navigation",
                    title="Mixed Word Navigation",
                    description="Combine different word movements",
                    instructions="Navigate to the word 'return' efficiently",
                    expected_commands=["W", "W", "w"],
                    initial_text="if user.is_authenticated() and user.has_permission(): return True",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 57)},
                    hints=[
                        "Use 'W' to skip over method calls quickly",
                        "Then use 'w' for fine-grained movement",
                        "Sequence: W, W, w gets to 'return'"
                    ]
                )
            ],
            summary="""
Excellent word navigation! You've learned:

✅ `w` - Next word beginning
✅ `b` - Previous word beginning
✅ `e` - Word end  
✅ `W` - Next WORD (whitespace-separated)
✅ `B` - Previous WORD
✅ `E` - WORD end

Word movement is essential for efficient Vim usage!
            """,
            tips=[
                "Use W/B/E for paths and URLs (fewer stops)",
                "Use w/b/e for code with lots of punctuation",
                "Combine with numbers: 3w moves 3 words forward",
                "Practice on different types of text to see the difference"
            ],
            common_mistakes=[
                "Confusing w/W behavior - practice with punctuation",
                "Using hjkl when word movement would be faster",
                "Not using 'e' for moving to word endings"
            ]
        )
        
        return Lesson("lesson_02_02", content)
    
    def _create_lesson_03(self) -> Lesson:
        """Lesson 2.3: File Navigation"""
        content = LessonContent(
            title="File Navigation",
            description="Navigate efficiently through large files",
            learning_objectives=[
                "Master file-level navigation commands",
                "Learn to jump to specific lines quickly",
                "Navigate large files efficiently",
                "Use page scrolling commands effectively"
            ],
            introduction="""
# File Navigation

When working with large files, you need efficient ways to move around quickly. 
Vim provides powerful commands for file-level navigation.

## File Navigation Commands:
- `gg` - Go to first line
- `G` - Go to last line  
- `[number]G` - Go to specific line number
- `Ctrl+f` - Page forward (down)
- `Ctrl+b` - Page backward (up)
- `Ctrl+d` - Half page down
- `Ctrl+u` - Half page up

## Line Numbers:
- `:set number` - Show line numbers
- `:set relativenumber` - Show relative line numbers
            """,
            instructions="""
Practice navigating through a multi-line file using file navigation commands.
These commands are essential for working with large codebases.

**File Context:**
You'll be working with a simulated file with multiple lines and sections.
            """,
            exercises=[
                Exercise(
                    id="go_to_first",
                    title="Go to First Line",
                    description="Navigate to the beginning of the file",
                    instructions="Use 'gg' to go to the first line",
                    expected_commands=["g", "g"],
                    initial_text="Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nLine 8\nLine 9\nLine 10",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 0)},
                    hints=[
                        "Press 'g' twice (gg)",
                        "This moves to the very first line of the file",
                        "Useful when you're lost in a large file"
                    ]
                ),
                Exercise(
                    id="go_to_last",
                    title="Go to Last Line",
                    description="Navigate to the end of the file",
                    instructions="Use 'G' to go to the last line",
                    expected_commands=["G"],
                    initial_text="Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nLine 8\nLine 9\nLine 10",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (9, 0)},
                    hints=[
                        "Press 'G' (capital G)",
                        "This jumps to the last line of the file",
                        "Quick way to get to the end"
                    ]
                ),
                Exercise(
                    id="go_to_line",
                    title="Go to Specific Line",
                    description="Navigate to a specific line number",
                    instructions="Use '5G' to go to line 5",
                    expected_commands=["5", "G"],
                    initial_text="Line 1\nLine 2\nLine 3\nLine 4\nLine 5 - Target\nLine 6\nLine 7\nLine 8\nLine 9\nLine 10",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (4, 0)},
                    hints=[
                        "Type '5' then 'G'",
                        "This goes to line number 5",
                        "Very useful when you know the line number"
                    ]
                ),
                Exercise(
                    id="half_page_down",
                    title="Half Page Down",
                    description="Scroll down half a page",
                    instructions="Use 'Ctrl+d' to scroll down half a page",
                    expected_commands=["<C-d>"],
                    initial_text="Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nLine 8\nLine 9\nLine 10\nLine 11\nLine 12",
                    validation_type="cursor_position", 
                    validation_params={"expected_position": (6, 0)},
                    hints=[
                        "Hold Ctrl and press 'd'",
                        "This scrolls down half a page",
                        "Faster than multiple 'j' presses"
                    ]
                ),
                Exercise(
                    id="navigation_combo",
                    title="Navigation Combination",
                    description="Practice combining navigation commands",
                    instructions="Go to first line, then line 7, then last line",
                    expected_commands=["g", "g", "7", "G", "G"],
                    initial_text="Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nLine 8\nLine 9\nLine 10",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (9, 0)},
                    hints=[
                        "Start with 'gg' to go to first line",
                        "Then '7G' to go to line 7", 
                        "Finally 'G' to go to last line"
                    ]
                )
            ],
            summary="""
Perfect file navigation! You've mastered:

✅ `gg` - Go to first line
✅ `G` - Go to last line
✅ `[number]G` - Go to specific line  
✅ `Ctrl+d` - Half page down
✅ `Ctrl+u` - Half page up

These commands make large files manageable!
            """,
            tips=[
                "Use line numbers (:set number) to see where you are",
                "Combine with search for powerful navigation",
                "Ctrl+d/u are smoother than page up/down",
                "Practice on large files to feel the benefit"
            ]
        )
        
        return Lesson("lesson_02_03", content)
    
    def _create_lesson_04(self) -> Lesson:
        """Lesson 2.4: Search-Based Navigation"""
        content = LessonContent(
            title="Search-Based Navigation",
            description="Use search for lightning-fast navigation",
            learning_objectives=[
                "Master forward and backward search",
                "Use search navigation efficiently",
                "Navigate with word-under-cursor search",
                "Combine search with other movements"
            ],
            introduction="""
# Search-Based Navigation

Search is one of the fastest ways to navigate in Vim. Instead of counting 
lines or characters, you can jump directly to what you're looking for.

## Search Commands:
- `/pattern` - Search forward for pattern
- `?pattern` - Search backward for pattern
- `n` - Next match (same direction)
- `N` - Previous match (opposite direction)
- `*` - Search forward for word under cursor
- `#` - Search backward for word under cursor

## Search Tips:
- Search is case-sensitive by default
- Use `/<Enter>` to repeat last search
- Escape cancels search input
            """,
            instructions="""
Practice using search for navigation. Search is incredibly powerful 
for jumping to specific locations quickly.

**Search Context:**
You'll search for function names, variables, and keywords in code-like text.
            """,
            exercises=[
                Exercise(
                    id="forward_search",
                    title="Forward Search",
                    description="Search forward for a specific word",
                    instructions="Search for 'function' using '/function'",
                    expected_commands=["/", "f", "u", "n", "c", "t", "i", "o", "n", "<Enter>"],
                    initial_text="def my_function():\n    print('hello')\n    return function_result\n\ndef another_function():\n    pass",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 7)},
                    hints=[
                        "Press '/' to start forward search",
                        "Type 'function' and press Enter",
                        "Cursor will jump to first match"
                    ]
                ),
                Exercise(
                    id="next_match",
                    title="Next Search Match",
                    description="Navigate to the next search result",
                    instructions="Use 'n' to go to the next 'function' match",
                    expected_commands=["n"],
                    initial_text="def my_function():\n    print('hello')\n    return function_result\n\ndef another_function():\n    pass",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (2, 11)},
                    hints=[
                        "Press 'n' to go to next match",
                        "This continues the previous search",
                        "Much faster than searching again"
                    ]
                ),
                Exercise(
                    id="backward_search",
                    title="Backward Search",
                    description="Search backward for a pattern",
                    instructions="Search backward for 'def' using '?def'",
                    expected_commands=["?", "d", "e", "f", "<Enter>"],
                    initial_text="def my_function():\n    print('hello')\n    return function_result\n\ndef another_function():\n    pass",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (3, 0)},
                    hints=[
                        "Press '?' to start backward search",
                        "Type 'def' and press Enter",
                        "Searches upward from cursor position"
                    ]
                ),
                Exercise(
                    id="word_under_cursor",
                    title="Search Word Under Cursor",
                    description="Search for the word under cursor",
                    instructions="Place cursor on 'variable' and use '*' to find next occurrence",
                    expected_commands=["*"],
                    initial_text="variable = 10\nprint(variable)\nif variable > 5:\n    variable += 1",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (1, 6)},
                    hints=[
                        "Make sure cursor is on the word 'variable'",
                        "Press '*' to search forward for this word",
                        "Automatically searches for word boundaries"
                    ]
                ),
                Exercise(
                    id="search_navigation_combo",
                    title="Search Navigation Combination",
                    description="Combine search with other navigation",
                    instructions="Search for 'return', then go to next match, then previous",
                    expected_commands=["/", "r", "e", "t", "u", "r", "n", "<Enter>", "n", "N"],
                    initial_text="def func1():\n    return True\n\ndef func2():\n    return False\n\ndef func3():\n    return None",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (1, 4)},
                    hints=[
                        "Search for 'return' with /return",
                        "Use 'n' to go to next match",
                        "Use 'N' to go back to previous match"
                    ]
                )
            ],
            summary="""
Excellent search navigation! You've learned:

✅ `/pattern` - Search forward
✅ `?pattern` - Search backward
✅ `n` - Next match
✅ `N` - Previous match
✅ `*` - Search word under cursor
✅ `#` - Search word under cursor backward

Search is your fastest navigation tool!
            """,
            tips=[
                "Use * and # for quick variable/function finding",
                "Combine search with word movement for precision",
                "Use n/N to navigate through multiple matches",
                "Search is often faster than counting lines"
            ],
            common_mistakes=[
                "Forgetting to press Enter after typing search pattern",
                "Not using * for word-under-cursor (very handy!)",
                "Using case-sensitive search when case-insensitive would work better"
            ]
        )
        
        return Lesson("lesson_02_04", content)