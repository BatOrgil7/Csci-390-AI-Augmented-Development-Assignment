# AI Interaction Log

This log records the AI-assisted development work for PNTS. Review it before submission and append any additional AI conversations you had outside this project folder.

## Transcript 1: Initial Build Request

Date: May 6, 2026

### User Prompt

```text
CSci 390: Special Topics in CS
Topic: AI Augmented Development.
Exercise 6: Final Activity
Due Date: Thursday, May 7, 2026 by 3 PM
Directions: In this assignment, you will design and implement a desktop Personal Note-
Taking System (PNTS) using Python and PyQt. The application allows users to create,
organize, and view notes by date and topic, with support for multiple images per note.
Make sure to critically evaluate all AI-generated output and demonstrate understanding
of the system you build.
System Description
You will build a Personal Note-Taking System (PNTS) with the following capabilities:
Core Features
Create a note with:
• Date (selected using a date picker)
• Topic (text input)
• Content (multi-line text)
• Multiple image attachments
• View all notes in a list
Filter notes by:
• Date
• Topic
• Keyword search
You must:
• Keep all AI chat transcripts
• Clearly show how prompts evolved over time
• Critically evaluate AI-generated code (do not blindly accept it)
Deliverables
1. All Python source files
2. User Documentation
3. AI Interaction Log - Submit all AI chat transcripts, including:
• Code generation prompts
• Debugging conversations
• Design discussions
4. A summary of your experience on this activity.
```

### AI Response Summary

The AI interpreted the assignment as a request to create a complete PNTS project. It inspected the workspace, found that the folder was empty except for Git metadata, checked the Python version, and checked whether PyQt was installed. Python 3.12.0 was available, but PyQt5 and PyQt6 were not installed.

### Design Decisions Produced With AI

- Use PyQt6 because it is a current PyQt version and satisfies the PyQt requirement.
- Store notes in a local JSON file instead of a database because the assignment scope is small.
- Copy image attachments into `data/images/` so notes do not depend on the original image location.
- Separate storage/model logic from the GUI so filtering and persistence can be tested without launching the desktop app.
- Include a `requirements.txt` file because PyQt was missing from the current environment.

### Prompt Evolution

The initial prompt was broad and assignment-oriented. During implementation, the task became more specific:

1. Build a PyQt desktop note app with date, topic, content, and multiple images.
2. Add local persistence using JSON.
3. Add filters for date, topic, and keyword search.
4. Add documentation and an AI log because those are required deliverables.
5. Add tests for the non-GUI storage behavior.

## Critical Evaluation Of AI-Generated Code

The AI-generated design was reviewed against the assignment requirements:

- Date picker requirement: Satisfied with `QDateEdit` using calendar popup.
- Topic input requirement: Satisfied with `QLineEdit`.
- Multiline content requirement: Satisfied with `QTextEdit`.
- Multiple image attachments requirement: Satisfied with `QFileDialog.getOpenFileNames` and a list of copied attachment paths.
- View all notes requirement: Satisfied with `QListWidget`.
- Date, topic, and keyword filtering requirement: Satisfied in `NoteStore.filter_notes` and connected to UI controls.

The design also has limitations:

- Notes can be created and deleted, but not edited after saving.
- JSON storage is simple and readable, but it is not ideal for very large note collections.
- Keyword search is a simple substring search, not a ranked search system.
- The GUI could not be fully launched during development until PyQt6 is installed.

## Debugging And Verification Notes

- The environment was checked with `python --version`.
- PyQt availability was checked with Python import discovery.
- Non-GUI tests were added for persistence, filtering, and multiple attachment copying/deletion.
- Syntax checks passed with `python -m py_compile main.py pnts\models.py pnts\storage.py pnts\app.py tests\test_storage.py`.
- Tests passed with `python -m unittest discover -s tests`.
- The GUI was not launched in this environment because PyQt6 was not installed. The project includes `requirements.txt` and `main.py` prints a clear install instruction if PyQt6 is missing.

## Transcript 2: Bug Fix And UI Improvement Request

Date: May 6, 2026

### User Prompt

```text
Fix all the bugs and Improve UI design
```

### AI Response Summary

The AI reviewed the current PyQt and storage code, ran an offscreen UI smoke test, and then improved both reliability and interface design. PyQt6 had already been installed by this point, so the GUI code could be imported and tested.

### Changes Made

- Added safer JSON loading. Invalid `notes.json` files are backed up instead of crashing the app.
- Added atomic note saving through a temporary file replacement.
- Added image attachment validation for supported image extensions.
- Prevented stored image paths from resolving outside the app data directory.
- Added rollback cleanup if image copying fails partway through.
- Added pending attachment count, remove-selected-image support, and clearer attachment status.
- Improved the layout, spacing, native icons, status bar messages, selected-note display, and list styling.
- Fixed a font rendering problem found during an offscreen screenshot check by loading a real Windows font into Qt when available.

### Critical Evaluation

The original version met the assignment requirements, but it trusted the storage file and attachment paths too much. The improved version is safer because it handles corrupted JSON, rejects unsupported attachments, and avoids path traversal problems. The UI is also easier to scan because creation, filtering, note list, and note details are visually separated.

The phrase "fix all bugs" is broad, so the AI focused on bugs that could be discovered from code review and local tests. It did not prove that no bugs exist. Remaining possible improvements include edit-note support, drag-and-drop images, and packaged application builds.

### Verification

- Syntax check passed with `python -m py_compile main.py pnts\models.py pnts\storage.py pnts\app.py tests\test_storage.py`.
- Unit tests passed with `python -m unittest discover -s tests`.
- Offscreen UI smoke testing passed.
- A rendered UI preview was inspected to catch layout and font-rendering issues.

## Additional Transcript Space

Add any other AI conversations here, especially if you ask for bug fixes, explanations, or design changes after this point.
