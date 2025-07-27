"""
Module 3: Text Editing - Advanced text manipulation in Vim.
"""

from .base import LearningModule, Lesson, LessonContent, Exercise


class Module03TextEditing(LearningModule):
    """Module 3: Text Editing and Manipulation."""
    
    def __init__(self):
        super().__init__(
            module_id="module_03",
            title="Text Editing & Manipulation",
            description="Master text editing, copying, pasting, and advanced manipulation techniques",
            prerequisites=["module_01", "module_02"],
            estimated_duration=45
        )
        
        # Create lessons
        self.lessons = [
            self._create_lesson_01_basic_editing(),
            self._create_lesson_02_copy_paste(),
            self._create_lesson_03_delete_operations(),
            self._create_lesson_04_change_operations(),
            self._create_lesson_05_advanced_editing()
        ]
    
    def _create_lesson_01_basic_editing(self) -> Lesson:
        """Lesson 1: Basic Text Editing."""
        content = LessonContent(
            title="Basic Text Editing",
            description="Learn fundamental text editing operations in Vim",
            learning_objectives=[
                "Insert text at cursor position and end of line",
                "Insert new lines above and below cursor",
                "Replace single characters and entire lines",
                "Master different ways to enter Insert mode"
            ],
            introduction="""
# Basic Text Editing

Now that you can move around in Vim, it's time to learn how to actually edit text! 
This is where Vim's modal nature really shines.

## Key Concepts:
- **Insert modes**: Different ways to enter Insert mode for different situations
- **Replace operations**: Quick character and line replacements  
- **Line creation**: Adding new lines efficiently
- **Mode awareness**: Understanding when you're in Insert vs Normal mode

## Why This Matters:
These are the building blocks of all text editing in Vim. Once you master these basics,
you'll be able to edit text faster than in any other editor!
            """.strip(),
            instructions="""
Practice these fundamental editing commands:

**Important Notes:**
- Always return to Normal mode (Escape) after editing
- Watch the mode indicator to know which mode you're in
- These commands work from Normal mode only
            """.strip(),
            exercises=[
                Exercise(
                    id="module_03_lesson_01_exercise_01",
                    title="Insert at Cursor",
                    description="Practice inserting text at the cursor position",
                    instructions="Use 'i' to enter Insert mode at the cursor, type 'Hello', then press Escape to return to Normal mode",
                    expected_commands=["i", "Hello", "Escape"],
                    initial_text="Welcome to Vim!",
                    validation_type="text_content",
                    validation_params={"expected_text": "HelloWelcome to Vim!"},
                    hints=[
                        "Press 'i' to enter Insert mode at the cursor position",
                        "Type 'Hello' while in Insert mode",
                        "Press Escape to return to Normal mode"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_01_exercise_02", 
                    title="Append at End of Line",
                    description="Learn to append text at the end of the current line",
                    instructions="Use 'A' to move to end of line and enter Insert mode, type ' - edited', then Escape",
                    expected_commands=["A", " - edited", "Escape"],
                    initial_text="This line needs editing",
                    validation_type="text_content", 
                    validation_params={"expected_text": "This line needs editing - edited"},
                    hints=[
                        "Press 'A' (uppercase) to jump to end of line and enter Insert mode",
                        "Type ' - edited' (with the space at the beginning)",
                        "Press Escape when done"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_01_exercise_03",
                    title="Insert New Line Below",
                    description="Create a new line below the cursor and enter Insert mode",
                    instructions="Use 'o' to create a new line below, type 'New line!', then Escape",
                    expected_commands=["o", "New line!", "Escape"],
                    initial_text="First line\nSecond line",
                    validation_type="text_content",
                    validation_params={"expected_text": "First line\nNew line!\nSecond line"},
                    hints=[
                        "Press 'o' (lowercase) to create a new line below and enter Insert mode",
                        "Type 'New line!' on the new line",
                        "Press Escape to return to Normal mode"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_01_exercise_04",
                    title="Insert New Line Above", 
                    description="Create a new line above the cursor and enter Insert mode",
                    instructions="Move to second line, use 'O' to create a line above, type 'Inserted above', then Escape",
                    expected_commands=["j", "O", "Inserted above", "Escape"],
                    initial_text="First line\nSecond line",
                    validation_type="text_content",
                    validation_params={"expected_text": "First line\nInserted above\nSecond line"},
                    hints=[
                        "First move down to the second line with 'j'",
                        "Press 'O' (uppercase) to create a new line above and enter Insert mode",
                        "Type 'Inserted above' on the new line",
                        "Press Escape when done"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_01_exercise_05",
                    title="Replace Single Character",
                    description="Replace a single character without entering Insert mode",
                    instructions="Move to the 'X' character and use 'r' to replace it with 'Y'",
                    expected_commands=["f", "X", "r", "Y"],
                    initial_text="Find the X character and replace it",
                    validation_type="text_content",
                    validation_params={"expected_text": "Find the Y character and replace it"},
                    hints=[
                        "Use 'f' followed by 'X' to find the X character",
                        "Press 'r' to enter replace mode for one character",
                        "Type 'Y' to replace the X with Y"
                    ]
                )
            ],
            summary="""
Excellent work on basic text editing! You've learned:

✅ Insert mode variations: i, I, a, A, o, O
✅ Single character replacement with 'r'
✅ Creating new lines above and below
✅ Mode awareness and transitions

These are the fundamental building blocks of text editing in Vim. 
Next we'll learn about copying and pasting text efficiently.
            """.strip(),
            tips=[
                "Remember: 'i' = insert here, 'a' = insert after, 'A' = insert at end of line",
                "'o' creates new line below, 'O' creates new line above",
                "'r' replaces one character without entering Insert mode",
                "Always watch the mode indicator to know where you are"
            ],
            common_mistakes=[
                "Forgetting to press Escape to return to Normal mode",
                "Confusing uppercase and lowercase commands (O vs o, A vs a)",
                "Trying to use editing commands while in Insert mode"
            ]
        )
        
        return Lesson("module_03_lesson_01", content)
    
    def _create_lesson_02_copy_paste(self) -> Lesson:
        """Lesson 2: Copy and Paste Operations."""
        content = LessonContent(
            title="Copy and Paste Operations",
            description="Master Vim's powerful copy (yank) and paste system",
            learning_objectives=[
                "Copy (yank) text with 'y' command combinations",
                "Paste text before and after cursor with 'p' and 'P'",
                "Work with Vim's clipboard registers",
                "Copy entire lines and word selections"
            ],
            introduction="""
# Copy and Paste in Vim

Vim's copy-paste system is incredibly powerful and different from other editors.
In Vim, copying is called "yanking" and uses the 'y' command.

## Key Concepts:
- **Yanking**: Copying text with 'y' + motion commands
- **Putting**: Pasting text with 'p' and 'P'
- **Line operations**: Special commands for entire lines
- **Visual selection**: Selecting text before copying

## Why This Matters:
Vim's copy-paste system works seamlessly with movement commands, making it
incredibly efficient once you understand the patterns.
            """.strip(),
            instructions="""
Learn these copy-paste commands:

**Important Notes:**
- 'y' + motion copies that text range
- 'p' pastes after cursor, 'P' pastes before cursor  
- 'yy' copies the entire current line
- Copied text stays available until you copy something else
            """.strip(),
            exercises=[
                Exercise(
                    id="module_03_lesson_02_exercise_01",
                    title="Copy Current Line",
                    description="Copy an entire line using the yy command",
                    instructions="Move to the first line and use 'yy' to copy it, then 'p' to paste below",
                    expected_commands=["yy", "p"],
                    initial_text="Line to copy\nOther line",
                    validation_type="text_content",
                    validation_params={"expected_text": "Line to copy\nLine to copy\nOther line"},
                    hints=[
                        "Make sure you're on the first line",
                        "Press 'yy' to yank (copy) the entire line",
                        "Press 'p' to paste the line below the cursor"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_02_exercise_02",
                    title="Copy Word and Paste",
                    description="Copy a word and paste it elsewhere",
                    instructions="Move to word 'important', copy it with 'yw', move to end and paste with 'p'",
                    expected_commands=["f", "i", "yw", "A", " ", "p"],
                    initial_text="This is important text",
                    validation_type="text_content",
                    validation_params={"expected_text": "This is important text important"},
                    hints=[
                        "Use 'f' followed by 'i' to find the word 'important'",
                        "Press 'yw' to yank (copy) the word",
                        "Press 'A' to go to end of line and enter Insert mode",
                        "Add a space, then Escape and paste with 'p'"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_02_exercise_03",
                    title="Paste Before Cursor",
                    description="Learn to paste before the cursor position",
                    instructions="Copy the first word with 'yw', move to 'text', and paste before it with 'P'",
                    expected_commands=["yw", "f", "t", "P"],
                    initial_text="Hello world text here",
                    validation_type="text_content",
                    validation_params={"expected_text": "Hello world Hellotext here"},
                    hints=[
                        "Start by copying 'Hello' with 'yw'",
                        "Use 'f' followed by 't' to find the word 'text'",
                        "Press 'P' (uppercase) to paste before the cursor"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_02_exercise_04",
                    title="Copy to End of Line",
                    description="Copy from cursor to end of line",
                    instructions="Move to word 'from', copy to end with 'y$', go to next line and paste with 'p'",
                    expected_commands=["f", "f", "y$", "j", "p"],
                    initial_text="Copy from here to end\nPaste on this line",
                    validation_type="text_content",
                    validation_params={"expected_text": "Copy from here to end\nPaste on this linefrom here to end"},
                    hints=[
                        "Use 'f' twice to find the word 'from'",
                        "Press 'y$' to copy from cursor to end of line",
                        "Press 'j' to go to next line, then 'p' to paste"
                    ]
                )
            ],
            summary="""
Great job mastering copy and paste! You now know:

✅ Line copying with 'yy'
✅ Word copying with 'yw'
✅ Copy to end of line with 'y$'
✅ Paste after cursor with 'p' and before with 'P'

These operations combine with all movement commands for maximum efficiency.
Next we'll explore different ways to delete text.
            """.strip(),
            tips=[
                "'y' works with any movement command: yw, y$, yj, etc.",
                "'p' pastes after cursor/line, 'P' pastes before",
                "Think of 'yy' as 'yank yank' - yank the whole line",
                "Copied text persists until you copy something else"
            ],
            common_mistakes=[
                "Confusing 'p' and 'P' - remember 'p' = after, 'P' = before",
                "Forgetting that 'y' needs a movement command (except 'yy')",
                "Not realizing copied text is overwritten by new copies"
            ]
        )
        
        return Lesson("module_03_lesson_02", content)
    
    def _create_lesson_03_delete_operations(self) -> Lesson:
        """Lesson 3: Delete Operations."""
        content = LessonContent(
            title="Delete Operations",
            description="Learn efficient ways to delete text in Vim",
            learning_objectives=[
                "Delete characters, words, and lines efficiently",
                "Use delete commands that also copy (cut) text",
                "Combine delete with movement commands",
                "Understand the difference between delete and change"
            ],
            introduction="""
# Delete Operations in Vim

Vim provides many ways to delete text efficiently. What's powerful is that
most delete operations also copy the deleted text, so you can paste it elsewhere.

## Key Concepts:
- **Character deletion**: x, X for single characters
- **Word deletion**: dw, db for word-based deletion
- **Line deletion**: dd for entire lines
- **Cut and paste**: Deleted text is automatically copied

## Why This Matters:
Vim's delete commands are actually "cut" operations - they delete and copy
simultaneously, making text manipulation incredibly efficient.
            """.strip(),
            instructions="""
Master these deletion commands:

**Important Notes:**
- 'd' + motion deletes that range and copies it
- 'x' deletes character under cursor
- 'dd' deletes entire line
- Deleted text can be pasted with 'p'
            """.strip(),
            exercises=[
                Exercise(
                    id="module_03_lesson_03_exercise_01", 
                    title="Delete Single Character",
                    description="Delete individual characters using x",
                    instructions="Move to the 'X' character and delete it with 'x'",
                    expected_commands=["f", "X", "x"],
                    initial_text="Remove the X from this line",
                    validation_type="text_content",
                    validation_params={"expected_text": "Remove the  from this line"},
                    hints=[
                        "Use 'f' followed by 'X' to find the X character",
                        "Press 'x' to delete the character under the cursor"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_03_exercise_02",
                    title="Delete Entire Line",
                    description="Delete a complete line using dd",
                    instructions="Move to the second line and delete it with 'dd'",
                    expected_commands=["j", "dd"],
                    initial_text="Keep this line\nDelete this line\nKeep this line too",
                    validation_type="text_content",
                    validation_params={"expected_text": "Keep this line\nKeep this line too"},
                    hints=[
                        "Press 'j' to move to the second line",
                        "Press 'dd' to delete the entire line"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_03_exercise_03",
                    title="Delete Word Forward",
                    description="Delete from cursor to end of word",
                    instructions="Move to 'unnecessary' and delete the word with 'dw'",
                    expected_commands=["f", "u", "dw"],
                    initial_text="This unnecessary word should be removed",
                    validation_type="text_content",
                    validation_params={"expected_text": "This word should be removed"},
                    hints=[
                        "Use 'f' followed by 'u' to find the word 'unnecessary'",
                        "Press 'dw' to delete from cursor to end of word"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_03_exercise_04",
                    title="Delete to End of Line",
                    description="Delete from cursor to end of line",
                    instructions="Move to 'delete' and remove everything after it with 'D'",
                    expected_commands=["f", "d", "D"],
                    initial_text="Keep this but delete everything after this point",
                    validation_type="text_content",
                    validation_params={"expected_text": "Keep this but "},
                    hints=[
                        "Use 'f' followed by 'd' to find the word 'delete'",
                        "Press 'D' (uppercase) to delete from cursor to end of line"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_03_exercise_05",
                    title="Delete and Paste",
                    description="Delete text and paste it elsewhere",
                    instructions="Delete the word 'middle' with 'dw', move to end of line with 'A', and paste with ' p'",
                    expected_commands=["f", "m", "dw", "A", " ", "p"],
                    initial_text="Move the middle word to end",
                    validation_type="text_content",
                    validation_params={"expected_text": "Move the word to end middle"},
                    hints=[
                        "Find 'middle' with 'f' followed by 'm'",
                        "Delete it with 'dw'", 
                        "Go to end with 'A', add space, Escape, then paste with 'p'"
                    ]
                )
            ],
            summary="""
Excellent work with delete operations! You've mastered:

✅ Single character deletion with 'x'
✅ Line deletion with 'dd'  
✅ Word deletion with 'dw'
✅ Delete to end of line with 'D'
✅ Cut and paste workflow with delete + paste

Delete operations in Vim are incredibly powerful because they double as cut operations.
Next we'll learn about change operations.
            """.strip(),
            tips=[
                "'d' works with any movement: dw, d$, dj, db, etc.",
                "'x' = delete character, 'X' = delete character before cursor",
                "'D' is shorthand for 'd$' (delete to end of line)",
                "Deleted text is automatically copied and can be pasted"
            ],
            common_mistakes=[
                "Forgetting that deleted text is copied and can be pasted",
                "Using 'x' when 'dw' would be more efficient",
                "Not realizing 'D' deletes to end of line, not just one character"
            ]
        )
        
        return Lesson("module_03_lesson_03", content)
    
    def _create_lesson_04_change_operations(self) -> Lesson:
        """Lesson 4: Change Operations."""
        content = LessonContent(
            title="Change Operations", 
            description="Master the change command for efficient text replacement",
            learning_objectives=[
                "Use change command to delete and enter Insert mode",
                "Change words, lines, and text ranges efficiently",
                "Understand when to use change vs delete + insert",
                "Combine change with movement commands"
            ],
            introduction="""
# Change Operations

The change command 'c' is one of Vim's most powerful features. It combines
deletion and insertion into one smooth operation.

## Key Concepts:
- **Change = Delete + Insert**: 'c' deletes text and enters Insert mode
- **Efficiency**: Change eliminates the separate delete + insert steps
- **Range-based**: Works with any movement command
- **Line changes**: 'cc' changes entire lines

## Why This Matters:
Change operations are often the fastest way to replace text, as they combine
multiple operations into one fluid motion.
            """.strip(),
            instructions="""
Practice these change commands:

**Important Notes:**
- 'c' + motion deletes that range and enters Insert mode
- 'cc' changes the entire line
- 'C' changes from cursor to end of line
- After changing, press Escape to return to Normal mode
            """.strip(),
            exercises=[
                Exercise(
                    id="module_03_lesson_04_exercise_01",
                    title="Change Word",
                    description="Change a word using the cw command",
                    instructions="Move to 'old' and change it to 'new' using 'cw new' then Escape",
                    expected_commands=["f", "o", "cw", "new", "Escape"],
                    initial_text="Replace the old word with something else",
                    validation_type="text_content",
                    validation_params={"expected_text": "Replace the new word with something else"},
                    hints=[
                        "Use 'f' followed by 'o' to find the word 'old'",
                        "Press 'cw' to change the word (delete it and enter Insert mode)",
                        "Type 'new', then press Escape"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_04_exercise_02",
                    title="Change Entire Line", 
                    description="Replace an entire line using cc",
                    instructions="Move to the second line and change it to 'New line content' using 'cc'",
                    expected_commands=["j", "cc", "New line content", "Escape"],
                    initial_text="Keep this line\nReplace this entire line\nKeep this line too",
                    validation_type="text_content",
                    validation_params={"expected_text": "Keep this line\nNew line content\nKeep this line too"},
                    hints=[
                        "Press 'j' to move to the second line",
                        "Press 'cc' to change the entire line",
                        "Type 'New line content', then press Escape"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_04_exercise_03",
                    title="Change to End of Line",
                    description="Change from cursor to end of line",
                    instructions="Move to 'change' and replace everything after with 'modified text' using 'C'",
                    expected_commands=["f", "c", "C", "modified text", "Escape"],
                    initial_text="Keep this but change everything after this point",
                    validation_type="text_content",
                    validation_params={"expected_text": "Keep this but modified text"},
                    hints=[
                        "Use 'f' followed by 'c' to find 'change'",
                        "Press 'C' to change from cursor to end of line",
                        "Type 'modified text', then press Escape"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_04_exercise_04",
                    title="Change Inside Word",
                    description="Change text inside quotes or brackets",
                    instructions="Change the text inside quotes to 'hello' using 'ci\"hello'",
                    expected_commands=["ci\"", "hello", "Escape"],
                    initial_text="The word \"world\" should be changed",
                    validation_type="text_content",
                    validation_params={"expected_text": "The word \"hello\" should be changed"},
                    hints=[
                        "Position cursor somewhere on the quoted word 'world'",
                        "Press 'ci\"' to change inside the quotes",
                        "Type 'hello', then press Escape"
                    ]
                )
            ],
            summary="""
Outstanding work with change operations! You've learned:

✅ Word changing with 'cw'
✅ Line changing with 'cc'
✅ Change to end of line with 'C'
✅ Change inside text objects with 'ci'

Change operations are incredibly efficient because they combine delete and insert.
Next we'll explore some advanced editing techniques.
            """.strip(),
            tips=[
                "'c' + movement is usually faster than delete + insert separately",
                "'cc' preserves indentation when changing lines",
                "'C' is shorthand for 'c$' (change to end of line)",
                "Text objects like '\"', '(', '[' work great with 'ci' and 'ca'"
            ],
            common_mistakes=[
                "Forgetting to press Escape after typing replacement text",
                "Using 'dw' + 'i' instead of the more efficient 'cw'",
                "Not knowing about text objects like 'ci\"' for quoted text"
            ]
        )
        
        return Lesson("module_03_lesson_04", content)
    
    def _create_lesson_05_advanced_editing(self) -> Lesson:
        """Lesson 5: Advanced Editing Techniques."""
        content = LessonContent(
            title="Advanced Editing Techniques",
            description="Learn powerful editing techniques for complex text manipulation",
            learning_objectives=[
                "Use visual mode for precise text selection",
                "Master undo and redo operations",
                "Repeat last command with the dot operator",
                "Combine multiple editing operations efficiently"
            ],
            introduction="""
# Advanced Editing Techniques

Now that you know the basics, let's explore some advanced techniques that will
make you incredibly efficient at text editing.

## Key Concepts:
- **Visual mode**: Select text precisely before operating on it
- **Undo/Redo**: Navigate through your editing history
- **Dot operator**: Repeat your last change instantly
- **Command combinations**: Chain operations for complex edits

## Why This Matters:
These advanced techniques separate Vim beginners from power users. They allow
you to perform complex text manipulations with just a few keystrokes.
            """.strip(),
            instructions="""
Master these advanced editing techniques:

**Important Notes:**
- 'v' enters visual mode for character selection
- 'V' enters visual line mode
- 'u' undos last change, Ctrl+r redos
- '.' repeats the last change command
            """.strip(),
            exercises=[
                Exercise(
                    id="module_03_lesson_05_exercise_01",
                    title="Visual Mode Selection",
                    description="Use visual mode to select and delete text",
                    instructions="Use 'v' to enter visual mode, select 'unnecessary text', then delete with 'd'",
                    expected_commands=["f", "u", "v", "e", "e", "d"],
                    initial_text="Remove this unnecessary text from the line",
                    validation_type="text_content",
                    validation_params={"expected_text": "Remove this from the line"},
                    hints=[
                        "Find 'unnecessary' with 'f' followed by 'u'",
                        "Press 'v' to enter visual mode",
                        "Use 'e' to select to end of words",
                        "Press 'd' to delete the selected text"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_05_exercise_02",
                    title="Undo Operation",
                    description="Practice undoing changes",
                    instructions="Delete the word 'test' with 'dw', then undo the deletion with 'u'",
                    expected_commands=["f", "t", "dw", "u"],
                    initial_text="Don't delete this test word permanently",
                    validation_type="text_content",
                    validation_params={"expected_text": "Don't delete this test word permanently"},
                    hints=[
                        "Find 'test' with 'f' followed by 't'",
                        "Delete the word with 'dw'",
                        "Press 'u' to undo the deletion"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_05_exercise_03",
                    title="Repeat Last Command",
                    description="Use the dot operator to repeat commands",
                    instructions="Delete 'first' with 'dw', move to 'second', then repeat with '.'",
                    expected_commands=["dw", "w", "w", "."],
                    initial_text="first word second word third word",
                    validation_type="text_content",
                    validation_params={"expected_text": "word word third word"},
                    hints=[
                        "Start by deleting 'first' with 'dw'",
                        "Move to 'second' with 'w' commands",
                        "Press '.' to repeat the last deletion"
                    ]
                ),
                Exercise(
                    id="module_03_lesson_05_exercise_04",
                    title="Visual Line Mode",
                    description="Select entire lines with visual line mode",
                    instructions="Use 'V' to select the middle line, then delete it with 'd'",
                    expected_commands=["j", "V", "d"],
                    initial_text="First line\nDelete this line\nThird line",
                    validation_type="text_content",
                    validation_params={"expected_text": "First line\nThird line"},
                    hints=[
                        "Move to the middle line with 'j'",
                        "Press 'V' (uppercase) to enter visual line mode",
                        "Press 'd' to delete the selected line"
                    ]
                )
            ],
            summary="""
Congratulations! You've mastered advanced editing techniques:

✅ Visual mode selection with 'v' and 'V'
✅ Undo operations with 'u'
✅ Command repetition with '.'
✅ Complex text manipulation workflows

You now have all the tools needed for efficient text editing in Vim!
Next module will cover search and replace operations.
            """.strip(),
            tips=[
                "Visual mode is great for precise selections that are hard to express with motions",
                "The dot operator '.' is one of Vim's most powerful features",
                "'u' undos, Ctrl+r redos - navigate through your change history",
                "Combine visual mode with any operation: d, y, c, etc."
            ],
            common_mistakes=[
                "Overusing visual mode when a motion command would be more efficient",
                "Not utilizing the dot operator for repetitive tasks",
                "Forgetting that 'V' selects entire lines vs 'v' for characters"
            ]
        )
        
        return Lesson("module_03_lesson_05", content)