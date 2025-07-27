"""
Module 4: Search & Replace - Master Vim's powerful search and replace capabilities.
"""

from .base import LearningModule, Lesson, LessonContent, Exercise


class Module04SearchReplace(LearningModule):
    """Module 4: Search & Replace Operations."""
    
    def __init__(self):
        super().__init__(
            module_id="module_04",
            title="Search & Replace",
            description="Master Vim's powerful search and replace capabilities for efficient text manipulation"
        )
        self.prerequisites = ["module_01", "module_02", "module_03"]
        self.estimated_duration = 50
    
    def initialize_content(self) -> None:
        """Initialize all lessons for this module."""
        self.add_lesson(self._create_lesson_01())
        self.add_lesson(self._create_lesson_02())
        self.add_lesson(self._create_lesson_03())
        self.add_lesson(self._create_lesson_04())
        self.add_lesson(self._create_lesson_05())
    
    def _create_lesson_01(self) -> Lesson:
        """Lesson 4.1: Basic Search Operations"""
        content = LessonContent(
            title="Basic Search Operations",
            description="Learn fundamental search operations in Vim",
            learning_objectives=[
                "Master forward and backward search with / and ?",
                "Navigate search results with n and N",
                "Use search for quick navigation",
                "Understand search patterns and escaping"
            ],
            introduction="""
# Basic Search Operations

Search is one of Vim's most powerful navigation tools. Instead of manually 
navigating to text, you can jump directly to what you're looking for.

## Search Commands:
- `/pattern` - Search forward for pattern
- `?pattern` - Search backward for pattern  
- `n` - Next match (same direction)
- `N` - Previous match (opposite direction)
- `*` - Search forward for word under cursor
- `#` - Search backward for word under cursor

## Search Tips:
- Search wraps around the file (goes to beginning/end)
- Use `/<Enter>` to repeat last search
- Press Escape to cancel search input
- Search is case-sensitive by default
            """,
            instructions="""
Practice these fundamental search operations. Search is incredibly fast
for navigation once you master the basic patterns.

**Key Points:**
- Type the pattern after / or ? and press Enter
- Use n/N to move between matches
- * and # search for the word under cursor automatically
            """,
            exercises=[
                Exercise(
                    id="basic_forward_search",
                    title="Forward Search",
                    description="Search forward for a specific word",
                    instructions="Search for the word 'function' using '/function' then press Enter",
                    expected_commands=["/", "function", "<Enter>"],
                    initial_text="def my_function():\n    return calculate_function(x)\n\ndef another_function():\n    pass",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 7)},
                    hints=[
                        "Press '/' to start forward search",
                        "Type 'function' and press Enter",
                        "Cursor will jump to first match"
                    ]
                ),
                Exercise(
                    id="search_next_match",
                    title="Navigate to Next Match",
                    description="Move to the next search result",
                    instructions="Use 'n' to go to the next occurrence of 'function'",
                    expected_commands=["n"],
                    initial_text="def my_function():\n    return calculate_function(x)\n\ndef another_function():\n    pass",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (1, 19)},
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
                    instructions="Search backward for 'def' using '?def' then press Enter",
                    expected_commands=["?", "def", "<Enter>"],
                    initial_text="def my_function():\n    return calculate_function(x)\n\ndef another_function():\n    pass",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (2, 0)},
                    hints=[
                        "Press '?' to start backward search",
                        "Type 'def' and press Enter",
                        "Searches upward from cursor position"
                    ]
                ),
                Exercise(
                    id="word_under_cursor",
                    title="Search Word Under Cursor",
                    description="Search for the word under cursor automatically",
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
                    description="Combine search with navigation commands",
                    instructions="Search for 'return', go to next match with 'n', then previous with 'N'",
                    expected_commands=["/", "return", "<Enter>", "n", "N"],
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
Excellent! You've mastered basic search operations:

✅ Forward search with `/pattern`
✅ Backward search with `?pattern`
✅ Navigation with `n` and `N`
✅ Word-under-cursor search with `*` and `#`

Search is your fastest navigation tool in Vim!
            """,
            tips=[
                "Use * and # for quick variable/function finding",
                "Search is often faster than counting lines or words",
                "Combine search with editing commands for powerful workflows",
                "Practice typing search patterns quickly for maximum efficiency"
            ]
        )
        
        return Lesson("lesson_04_01", content)
    
    def _create_lesson_02(self) -> Lesson:
        """Lesson 4.2: Search Options and Modifiers"""
        content = LessonContent(
            title="Search Options and Modifiers",
            description="Control search behavior with options and modifiers",
            learning_objectives=[
                "Use case-insensitive search",
                "Control search wrapping behavior",
                "Use search with ranges and counts",
                "Master search highlighting and incremental search"
            ],
            introduction="""
# Search Options and Modifiers

Vim provides many options to customize search behavior. These make search
more flexible and powerful for different use cases.

## Search Modifiers:
- `\\c` - Case-insensitive search (in pattern)
- `\\C` - Case-sensitive search (in pattern)
- `:set ignorecase` - Default case-insensitive
- `:set smartcase` - Smart case matching
- `:set hlsearch` - Highlight search results
- `:set incsearch` - Incremental search

## Special Patterns:
- `^pattern` - Match at beginning of line
- `pattern$` - Match at end of line
- `\\<word\\>` - Match whole word only
- `.` - Match any character
- `*` - Match zero or more of previous character
            """,
            instructions="""
Learn to control search behavior with these modifiers and options.
These make search much more precise and useful.

**Important Notes:**
- \\c and \\C can be used anywhere in the pattern
- ^ and $ are anchors for line beginning/end
- \\< and \\> match word boundaries
            """,
            exercises=[
                Exercise(
                    id="case_insensitive_search",
                    title="Case-Insensitive Search", 
                    description="Search ignoring case differences",
                    instructions="Search for 'HELLO' case-insensitively using '/\\chello'",
                    expected_commands=["/", "\\c", "hello", "<Enter>"],
                    initial_text="Hello world\nHELLO there\nhello again",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 0)},
                    hints=[
                        "Type '/\\chello' to search case-insensitively",
                        "\\c makes the search ignore case",
                        "Will match Hello, HELLO, hello, etc."
                    ]
                ),
                Exercise(
                    id="line_beginning_search",
                    title="Search at Line Beginning",
                    description="Search for patterns at the start of lines",
                    instructions="Search for 'def' at the beginning of a line using '/^def'",
                    expected_commands=["/", "^", "def", "<Enter>"],
                    initial_text="    def helper():\n        pass\ndef main():\n    def nested():\n        pass",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (2, 0)},
                    hints=[
                        "Use '^' to match beginning of line",
                        "Type '/^def' to find 'def' at line start",
                        "Will skip indented 'def' statements"
                    ]
                ),
                Exercise(
                    id="line_end_search",
                    title="Search at Line End",
                    description="Search for patterns at the end of lines",
                    instructions="Search for lines ending with ':' using '/:$'",
                    expected_commands=["/", ":", "$", "<Enter>"],
                    initial_text="def function():\n    if condition:\n        return value\n    else:\n        return None",
                    validation_type="cursor_position", 
                    validation_params={"expected_position": (0, 14)},
                    hints=[
                        "Use '$' to match end of line",
                        "Type '/:$' to find ':' at line end",
                        "Useful for finding function definitions"
                    ]
                ),
                Exercise(
                    id="whole_word_search",
                    title="Whole Word Search",
                    description="Search for complete words only",
                    instructions="Search for whole word 'in' using '/\\<in\\>'",
                    expected_commands=["/", "\\<", "in", "\\>", "<Enter>"],
                    initial_text="print(string)\nif item in list:\n    begin = 0",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (1, 8)},
                    hints=[
                        "Use '\\<' and '\\>' for word boundaries",
                        "Type '/\\<in\\>' to find 'in' as whole word",
                        "Won't match 'in' inside 'print' or 'string'"
                    ]
                ),
                Exercise(
                    id="wildcard_search",
                    title="Wildcard Search",
                    description="Use wildcards in search patterns",
                    instructions="Search for 'f.n' (f + any char + n) using '/f.n'",
                    expected_commands=["/", "f", ".", "n", "<Enter>"],
                    initial_text="function name\nfun code\nfan out\nfen error",
                    validation_type="cursor_position",
                    validation_params={"expected_position": (0, 0)},
                    hints=[
                        "Use '.' to match any single character",
                        "Type '/f.n' to find f + any char + n",
                        "Will match 'fun', 'fan', 'fen', etc."
                    ]
                )
            ],
            summary="""
Great work with search modifiers! You now know:

✅ Case-insensitive search with `\\c`
✅ Line anchors with `^` and `$`
✅ Word boundaries with `\\<` and `\\>`
✅ Wildcard matching with `.`

These modifiers make search incredibly precise and powerful!
            """,
            tips=[
                "Use \\c when you're not sure about capitalization",
                "^ and $ are great for finding function definitions",
                "\\< \\> prevent partial word matches",
                "Learn regex basics to unlock search's full power"
            ]
        )
        
        return Lesson("lesson_04_02", content)
    
    def _create_lesson_03(self) -> Lesson:
        """Lesson 4.3: Basic Find and Replace"""
        content = LessonContent(
            title="Basic Find and Replace",
            description="Learn fundamental find and replace operations",
            learning_objectives=[
                "Use the substitute command (:s) for replacements",
                "Replace on current line vs entire file",
                "Use global and confirm flags",
                "Handle special characters in replacements"
            ],
            introduction="""
# Basic Find and Replace

The substitute command (:s) is Vim's find and replace tool. It's incredibly
powerful and flexible, allowing precise text transformations.

## Substitute Command Syntax:
```
:s/pattern/replacement/flags
```

## Common Patterns:
- `:s/old/new/` - Replace first occurrence on current line
- `:s/old/new/g` - Replace all occurrences on current line
- `:%s/old/new/g` - Replace all occurrences in entire file
- `:%s/old/new/gc` - Replace with confirmation

## Useful Flags:
- `g` - Global (all occurrences on line)
- `c` - Confirm each replacement
- `i` - Case-insensitive
- `n` - Show count without replacing
            """,
            instructions="""
Practice the substitute command for find and replace operations.
Start with simple replacements and work up to more complex patterns.

**Remember:**
- :s works on current line by default
- Use % to work on entire file
- Always test with a small scope first
            """,
            exercises=[
                Exercise(
                    id="simple_line_replace",
                    title="Replace on Current Line",
                    description="Replace text on the current line only",
                    instructions="Replace 'old' with 'new' on current line using ':s/old/new/'",
                    expected_commands=[":", "s", "/", "old", "/", "new", "/", "<Enter>"],
                    initial_text="This old text has old values",
                    validation_type="text_content",
                    validation_params={"expected_text": "This new text has old values"},
                    hints=[
                        "Type ':s/old/new/' and press Enter",
                        "This replaces only the first occurrence",
                        "Notice it doesn't replace the second 'old'"
                    ]
                ),
                Exercise(
                    id="global_line_replace",
                    title="Replace All on Line",
                    description="Replace all occurrences on current line",
                    instructions="Replace all 'test' with 'demo' using ':s/test/demo/g'",
                    expected_commands=[":", "s", "/", "test", "/", "demo", "/", "g", "<Enter>"],
                    initial_text="test function test_var test123",
                    validation_type="text_content",
                    validation_params={"expected_text": "demo function demo_var demo123"},
                    hints=[
                        "Type ':s/test/demo/g' and press Enter",
                        "The 'g' flag means 'global' - all on line",
                        "All instances of 'test' will be replaced"
                    ]
                ),
                Exercise(
                    id="file_wide_replace",
                    title="Replace in Entire File",
                    description="Replace text throughout the entire file",
                    instructions="Replace all 'var' with 'variable' in file using ':%s/var/variable/g'",
                    expected_commands=[":", "%", "s", "/", "var", "/", "variable", "/", "g", "<Enter>"],
                    initial_text="var x = 5\nvar y = var * 2\nprint(var)",
                    validation_type="text_content",
                    validation_params={"expected_text": "variable x = 5\nvariable y = variable * 2\nprint(variable)"},
                    hints=[
                        "Type ':%s/var/variable/g' and press Enter",
                        "% means entire file, g means all occurrences",
                        "This is the most common replace pattern"
                    ]
                ),
                Exercise(
                    id="confirm_replace",
                    title="Replace with Confirmation",
                    description="Replace text with confirmation prompt",
                    instructions="Replace 'temp' with 'temporary' with confirmation using ':%s/temp/temporary/gc', then confirm all",
                    expected_commands=[":", "%", "s", "/", "temp", "/", "temporary", "/", "g", "c", "<Enter>", "a"],
                    initial_text="temp file\ntemp variable\ntemp storage",
                    validation_type="text_content",
                    validation_params={"expected_text": "temporary file\ntemporary variable\ntemporary storage"},
                    hints=[
                        "Type ':%s/temp/temporary/gc' and press Enter",
                        "The 'c' flag asks for confirmation",
                        "Press 'a' to confirm all replacements"
                    ]
                ),
                Exercise(
                    id="range_replace",
                    title="Replace in Range",
                    description="Replace text in specific line range",
                    instructions="Replace 'old' with 'new' in lines 1-2 using ':1,2s/old/new/g'",
                    expected_commands=[":", "1", ",", "2", "s", "/", "old", "/", "new", "/", "g", "<Enter>"],
                    initial_text="old line 1\nold line 2\nold line 3",
                    validation_type="text_content",
                    validation_params={"expected_text": "new line 1\nnew line 2\nold line 3"},
                    hints=[
                        "Type ':1,2s/old/new/g' and press Enter",
                        "1,2 specifies the range (lines 1 to 2)",
                        "Line 3 should remain unchanged"
                    ]
                )
            ],
            summary="""
Excellent work with find and replace! You've learned:

✅ Basic substitute: `:s/old/new/`
✅ Global flag: `:s/old/new/g`
✅ File-wide replace: `:%s/old/new/g`
✅ Confirmation: `:%s/old/new/gc`
✅ Range replace: `:1,5s/old/new/g`

The substitute command is incredibly powerful for text transformation!
            """,
            tips=[
                "Always test replacements on a small scope first",
                "Use \\c in pattern for case-insensitive replace",
                "The 'n' flag shows how many matches without replacing",
                "Visual mode selection can be used as range for :s"
            ]
        )
        
        return Lesson("lesson_04_03", content)
    
    def _create_lesson_04(self) -> Lesson:
        """Lesson 4.4: Advanced Replace Patterns"""
        content = LessonContent(
            title="Advanced Replace Patterns",
            description="Master advanced replacement patterns and techniques",
            learning_objectives=[
                "Use regular expressions in replacements",
                "Capture groups and backreferences",
                "Replace with special characters",
                "Use replacement expressions and functions"
            ],
            introduction="""
# Advanced Replace Patterns

Vim's substitute command supports full regular expressions and advanced
replacement features that enable powerful text transformations.

## Regular Expression Features:
- `\\d` - Match digits
- `\\w` - Match word characters
- `\\s` - Match whitespace
- `.*` - Match any characters (greedy)
- `.*?` - Match any characters (non-greedy)
- `[abc]` - Match any of a, b, or c
- `[0-9]` - Match any digit

## Capture Groups and Backreferences:
- `\\(pattern\\)` - Capture group
- `\\1`, `\\2` - Reference captured groups in replacement
- `&` - Reference entire match

## Special Replacements:
- `\\r` - Newline in replacement
- `\\t` - Tab in replacement
- `\\U\\1` - Uppercase captured group
- `\\L\\1` - Lowercase captured group
            """,
            instructions="""
Learn advanced replacement patterns for complex text transformations.
These patterns unlock the full power of Vim's replace capabilities.

**Key Concepts:**
- Use \\( \\) to capture parts of the match
- Reference captures with \\1, \\2, etc. in replacement
- & refers to the entire matched text
            """,
            exercises=[
                Exercise(
                    id="capture_groups",
                    title="Using Capture Groups",
                    description="Capture and rearrange text using groups",
                    instructions="Swap first and last name using ':s/\\(\\w\\+\\) \\(\\w\\+\\)/\\2, \\1/'",
                    expected_commands=[":", "s", "/", "\\(", "\\w", "\\+", "\\)", " ", "\\(", "\\w", "\\+", "\\)", "/", "\\2", ",", " ", "\\1", "/", "<Enter>"],
                    initial_text="John Smith",
                    validation_type="text_content",
                    validation_params={"expected_text": "Smith, John"},
                    hints=[
                        "\\( \\) creates capture groups",
                        "\\w\\+ matches one or more word characters",
                        "\\1 and \\2 reference the captured groups"
                    ]
                ),
                Exercise(
                    id="digit_replacement",
                    title="Replace Digits",
                    description="Find and replace digit patterns",
                    instructions="Replace all digits with 'X' using ':s/\\d/X/g'",
                    expected_commands=[":", "s", "/", "\\d", "/", "X", "/", "g", "<Enter>"],
                    initial_text="Phone: 123-456-7890",
                    validation_type="text_content",
                    validation_params={"expected_text": "Phone: XXX-XXX-XXXX"},
                    hints=[
                        "\\d matches any single digit",
                        "Use g flag to replace all digits",
                        "Each digit becomes 'X'"
                    ]
                ),
                Exercise(
                    id="word_boundaries",
                    title="Word Boundary Replacement",
                    description="Replace whole words using word boundaries",
                    instructions="Replace whole word 'is' with 'was' using ':s/\\<is\\>/was/g'",
                    expected_commands=[":", "s", "/", "\\<", "is", "\\>", "/", "was", "/", "g", "<Enter>"],
                    initial_text="This is a test. is this working?",
                    validation_type="text_content",
                    validation_params={"expected_text": "This was a test. was this working?"},
                    hints=[
                        "\\< and \\> are word boundaries",
                        "This prevents matching 'is' inside 'This'",
                        "Only standalone 'is' words are replaced"
                    ]
                ),
                Exercise(
                    id="case_conversion",
                    title="Case Conversion in Replacement",
                    description="Convert case of captured text",
                    instructions="Uppercase first letter of each word using ':s/\\<\\(\\w\\)/\\U\\1/g'",
                    expected_commands=[":", "s", "/", "\\<", "\\(", "\\w", "\\)", "/", "\\U", "\\1", "/", "g", "<Enter>"],
                    initial_text="hello world vim editor",
                    validation_type="text_content",
                    validation_params={"expected_text": "Hello World Vim Editor"},
                    hints=[
                        "\\< matches word boundary",
                        "\\(\\w\\) captures first character of word",
                        "\\U\\1 converts captured character to uppercase"
                    ]
                ),
                Exercise(
                    id="multiple_spaces",
                    title="Replace Multiple Spaces",
                    description="Replace multiple spaces with single space",
                    instructions="Replace multiple spaces with single space using ':s/  \\+/ /g'",
                    expected_commands=[":", "s", "/", " ", " ", "\\+", "/", " ", "/", "g", "<Enter>"],
                    initial_text="Text  with    multiple     spaces",
                    validation_type="text_content",
                    validation_params={"expected_text": "Text with multiple spaces"},
                    hints=[
                        "\\+ means one or more of previous pattern",
                        "  \\+ matches two or more spaces",
                        "Replaces with single space"
                    ]
                )
            ],
            summary="""
Outstanding work with advanced patterns! You've mastered:

✅ Capture groups with `\\( \\)`
✅ Backreferences with `\\1`, `\\2`
✅ Character classes like `\\d`, `\\w`, `\\s`
✅ Word boundaries `\\<` and `\\>`
✅ Case conversion `\\U` and `\\L`

These patterns enable incredibly powerful text transformations!
            """,
            tips=[
                "Practice regex patterns outside Vim first if you're new to them",
                "Use very magic mode (\\v) for cleaner regex syntax",
                "Test complex patterns on small text samples first",
                "Learn common regex patterns for your specific use cases"
            ]
        )
        
        return Lesson("lesson_04_04", content)
    
    def _create_lesson_05(self) -> Lesson:
        """Lesson 4.5: Search and Replace Workflows"""
        content = LessonContent(
            title="Search and Replace Workflows",
            description="Learn efficient workflows combining search and replace",
            learning_objectives=[
                "Combine visual selection with substitute",
                "Use search history and repetition",
                "Build complex multi-step replacements",
                "Master search and replace best practices"
            ],
            introduction="""
# Search and Replace Workflows

Real-world text editing often requires combining multiple search and replace
operations into efficient workflows. This lesson teaches you how to chain
operations and work efficiently.

## Workflow Techniques:
- Visual selection + substitute
- Search history and repetition
- Multiple substitute commands
- Conditional replacements
- Search and manual edit combination

## Advanced Features:
- `:g/pattern/s/old/new/g` - Global command with substitute
- `*` then `:%s//new/g` - Use last search in substitute
- `q:` - Open command history
- `@:` - Repeat last command

## Best Practices:
- Test on small samples first
- Use confirmation for risky changes
- Save backup before major changes
- Build complex changes incrementally
            """,
            instructions="""
Practice efficient workflows that combine search, selection, and replace.
These patterns will make you incredibly efficient at text manipulation.

**Workflow Tips:**
- Start with simple operations and build complexity
- Use visual mode for precise control
- Leverage search history to avoid retyping
            """,
            exercises=[
                Exercise(
                    id="visual_substitute",
                    title="Visual Selection Substitute",
                    description="Use visual selection to limit substitute scope",
                    instructions="Select lines 1-2 with 'V', then replace 'old' with 'new' using ':s/old/new/g'",
                    expected_commands=["V", "j", ":", "s", "/", "old", "/", "new", "/", "g", "<Enter>"],
                    initial_text="old text line 1\nold text line 2\nold text line 3",
                    validation_type="text_content",
                    validation_params={"expected_text": "new text line 1\nnew text line 2\nold text line 3"},
                    hints=[
                        "Use 'V' to enter visual line mode",
                        "Move down with 'j' to select multiple lines",
                        "Type ':s/old/new/g' to replace in selection"
                    ]
                ),
                Exercise(
                    id="search_then_substitute",
                    title="Search Then Substitute",
                    description="Use search result in substitute command",
                    instructions="Search for 'function' with '/', then replace all with 'method' using ':%s//method/g'",
                    expected_commands=["/", "function", "<Enter>", ":", "%", "s", "/", "/", "method", "/", "g", "<Enter>"],
                    initial_text="def function():\n    call_function()\nclass function_handler:",
                    validation_type="text_content",
                    validation_params={"expected_text": "def method():\n    call_method()\nclass method_handler:"},
                    hints=[
                        "First search for 'function' with /function",
                        "Then use :%s//method/g (empty pattern uses last search)",
                        "This is faster than retyping the pattern"
                    ]
                ),
                Exercise(
                    id="global_command_substitute",
                    title="Global Command with Substitute",
                    description="Use global command to substitute on matching lines only",
                    instructions="Replace 'temp' with 'final' only on lines containing 'var' using ':g/var/s/temp/final/g'",
                    expected_commands=[":", "g", "/", "var", "/", "s", "/", "temp", "/", "final", "/", "g", "<Enter>"],
                    initial_text="var temp = 5\nconst temp = 6\nvar temp_name = 'test'\nlet temp = 7",
                    validation_type="text_content",
                    validation_params={"expected_text": "var final = 5\nconst temp = 6\nvar final_name = 'test'\nlet temp = 7"},
                    hints=[
                        "':g/var/' selects lines containing 'var'",
                        "'/s/temp/final/g' runs substitute on those lines",
                        "Only lines with 'var' will have 'temp' replaced"
                    ]
                ),
                Exercise(
                    id="incremental_replacement",
                    title="Incremental Replacement",
                    description="Build complex replacement through multiple steps",
                    instructions="First replace 'old_' with 'new_', then replace '_name' with '_title'",
                    expected_commands=[":", "%", "s", "/", "old_", "/", "new_", "/", "g", "<Enter>", ":", "%", "s", "/", "_name", "/", "_title", "/", "g", "<Enter>"],
                    initial_text="old_name = 'test'\nold_name_var = 1\nold_filename = 'data'",
                    validation_type="text_content",
                    validation_params={"expected_text": "new_title = 'test'\nnew_title_var = 1\nnew_filename = 'data'"},
                    hints=[
                        "First run :%s/old_/new_/g",
                        "Then run :%s/_name/_title/g",
                        "Complex changes are often easier in steps"
                    ]
                ),
                Exercise(
                    id="conditional_replacement",
                    title="Conditional Replacement with Confirmation",
                    description="Use confirmation to selectively replace text",
                    instructions="Replace 'test' with 'exam' using confirmation, accept first, reject second using ':%s/test/exam/gc' then 'y' then 'n'",
                    expected_commands=[":", "%", "s", "/", "test", "/", "exam", "/", "g", "c", "<Enter>", "y", "n"],
                    initial_text="test function\ntest_variable\ntest case",
                    validation_type="text_content",
                    validation_params={"expected_text": "exam function\ntest_variable\ntest case"},
                    hints=[
                        "Use :%s/test/exam/gc for confirmation",
                        "Press 'y' for yes on first match",
                        "Press 'n' for no on remaining matches"
                    ]
                )
            ],
            summary="""
Congratulations! You've mastered advanced search and replace workflows:

✅ Visual selection with substitute
✅ Search history and pattern reuse
✅ Global commands with substitute
✅ Incremental replacement strategies
✅ Conditional replacement with confirmation

You now have the tools for any text transformation task!
            """,
            tips=[
                "Save your work before complex replacements",
                "Use :earlier and :later to navigate through changes",
                "Learn the global command (:g) for powerful line-based operations",
                "Practice these workflows on real code to build muscle memory"
            ]
        )
        
        return Lesson("lesson_04_05", content)