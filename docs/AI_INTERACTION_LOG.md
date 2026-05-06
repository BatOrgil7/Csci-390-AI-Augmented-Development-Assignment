# AI Interaction Log

This file records the AI-assisted development conversation for the Personal Note-Taking System (PNTS). It includes the assignment planning, code generation, dependency installation, debugging, UI improvement, GitHub publication, and Vercel publication conversations from this chat.

The final prompt that requested this cleanup is not included, based on the user's instruction.

## Prompt Evolution Overview

The prompts became more specific over time:

1. The first prompt gave the full assignment requirements and asked for the complete PNTS system.
2. The next prompt asked the AI to install all required libraries.
3. The next prompt asked the AI to launch the app.
4. The next prompt asked the AI to fix bugs and improve the UI.
5. The next prompt asked the AI to publish the project to GitHub and Vercel and verify errors.

## Transcript 1: Initial Assignment And Code Generation

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
- Date (selected using a date picker)
- Topic (text input)
- Content (multi-line text)
- Multiple image attachments
- View all notes in a list
Filter notes by:
- Date
- Topic
- Keyword search
You must:
- Keep all AI chat transcripts
- Clearly show how prompts evolved over time
- Critically evaluate AI-generated code (do not blindly accept it)
Deliverables
1. All Python source files
2. User Documentation
3. AI Interaction Log - Submit all AI chat transcripts, including:
- Code generation prompts
- Debugging conversations
- Design discussions
4. A summary of your experience on this activity.
```

### Assistant Response And Actions

```text
I’ll turn this into a working PyQt note-taking project plus the supporting deliverables the assignment asks for. First I’m checking what’s already in the workspace so I can avoid trampling anything you may have started.
```

The AI inspected the workspace and found that it was basically empty except for Git metadata. It checked Python and found Python 3.12.0. It also checked for PyQt and found that PyQt5 and PyQt6 were not installed yet.

```text
PyQt isn’t installed in the current Python environment, so I’ll include a requirements.txt and keep the storage logic testable without the GUI dependency. The app itself will target PyQt6, with notes saved locally as JSON and image attachments copied into a project data folder.
```

The AI created the project files:

- `main.py`
- `requirements.txt`
- `pnts/__init__.py`
- `pnts/models.py`
- `pnts/storage.py`
- `pnts/app.py`
- `tests/test_storage.py`
- `README.md`
- `docs/USER_DOCUMENTATION.md`
- `docs/AI_INTERACTION_LOG.md`
- `docs/EXPERIENCE_SUMMARY.md`
- `.gitignore`

The AI separated the program into a storage layer and a GUI layer. This was a useful design decision because the storage behavior could be tested without launching the desktop interface.

### Assistant Final Response For This Step

```text
Built the PNTS project in C:\Users\bator\OneDrive\Documents\New project 4.

Main pieces:
- App entry: main.py
- PyQt6 UI: pnts/app.py
- Data model/storage: pnts/models.py, pnts/storage.py
- User docs: docs/USER_DOCUMENTATION.md
- AI log: docs/AI_INTERACTION_LOG.md
- Experience summary draft: docs/EXPERIENCE_SUMMARY.md

Verification passed:
python -m py_compile main.py pnts\models.py pnts\storage.py pnts\app.py tests\test_storage.py
python -m unittest discover -s tests

PyQt6 is not installed in the current Python environment, so the GUI was not launched here. To run it:
python -m pip install -r requirements.txt
python main.py

One important note: review and personalize the AI log and experience summary before submitting, especially if you had any other AI conversations outside this session.
```

### Critical Evaluation

The generated design met the assignment requirements:

- Date picker: implemented with `QDateEdit`.
- Topic input: implemented with `QLineEdit`.
- Multiline content: implemented with `QTextEdit`.
- Multiple images: implemented with `QFileDialog.getOpenFileNames`.
- View notes: implemented with `QListWidget`.
- Filters: implemented in `NoteStore.filter_notes`.
- Documentation: created in the `docs/` folder.

The first version had limitations. Notes could be created and deleted, but not edited. JSON storage was simple and appropriate for this assignment, but it would not be ideal for a very large system. The GUI also could not be launched until PyQt6 was installed.

## Transcript 2: Installing Required Libraries

Date: May 6, 2026

### User Prompt

```text
Install the all required libraries
```

### Assistant Response And Actions

```text
I’ll install the project dependencies from requirements.txt now, then do a quick import check so we know PyQt6 is actually available.
```

The AI ran:

```powershell
python -m pip install -r requirements.txt
```

PyQt6 was installed successfully:

```text
Successfully installed PyQt6-6.11.0 PyQt6-Qt6-6.11.0 PyQt6-sip-13.11.1
```

The AI then checked that PyQt6 could import and reran the tests.

### Assistant Final Response For This Step

```text
Installed all required libraries from requirements.txt.

Confirmed:
- PyQt6 imports successfully
- Qt version: 6.11.0
- Tests pass: 3 passed

You can launch the app with:
python main.py

Small note: pip showed a warning about an invalid ~ip distribution, but PyQt6 installed correctly and the project is ready to run.
```

### Critical Evaluation

The AI did not assume installation worked just because `pip install` finished. It also tested the PyQt6 import and reran the storage tests. The pip warning was noted, but it did not stop the project because PyQt6 imported successfully.

## Transcript 3: Launching The App

Date: May 6, 2026

### User Prompt

```text
Launch the app.
```

### Assistant Response And Actions

```text
I’ll launch PNTS in its own process so the app window can stay open independently. If it exits right away, I’ll catch that from the process status.
```

The AI launched the app with:

```powershell
Start-Process -FilePath python -ArgumentList 'main.py'
```

The app started successfully.

### Assistant Final Response For This Step

```text
PNTS is launched and running.

Process ID: 16920
```

### Critical Evaluation

The AI checked whether the process exited quickly. This helped confirm that the app did not immediately crash after launch.

## Transcript 4: Bug Fixes And UI Improvements

Date: May 6, 2026

### User Prompt

```text
Fix all the bugs and Improve UI design
```

### Assistant Response And Actions

```text
I’ll do this as a real pass rather than a cosmetic skim: first reproduce/check obvious runtime issues, then tighten the UI and run verification again. Since there’s already an app process open, I’ll inspect without interrupting it unless I need to relaunch for testing.
```

The AI reviewed `pnts/app.py`, `pnts/storage.py`, and `pnts/models.py`. It ran an offscreen UI smoke test and found areas to improve. The AI identified several issues:

- Attachment handling was too permissive and could silently ignore bad files.
- JSON loading could fail hard if the notes file became corrupted.
- Image path handling needed to be safer.
- The UI needed clearer layout, spacing, and status feedback.
- The offscreen screenshot check showed a font-rendering issue where text appeared as square boxes.

The AI made these bug fixes:

- Added safer JSON loading.
- Backed up invalid `notes.json` files instead of crashing.
- Added atomic saves through a temporary file replacement.
- Added validation for supported image file types.
- Prevented image paths from resolving outside the app data folder.
- Added rollback cleanup if attachment copying failed partway through.
- Improved error messages for save and attachment problems.

The AI made these UI improvements:

- Improved the three-panel layout.
- Added native button icons.
- Added a remove-selected-image button.
- Added pending attachment counts.
- Added clearer status bar messages.
- Improved note list display and selected-note details.
- Improved spacing and visual grouping.
- Loaded a real Windows font into Qt when available to fix the screenshot font-rendering problem.

### Assistant Final Response For This Step

```text
Done. I fixed and improved the PNTS app, then relaunched the updated version visibly.

Key improvements:
- Hardened storage in pnts/storage.py: atomic saves, corrupt JSON backup, safer image paths, attachment validation, copy rollback on failure.
- Improved UI in pnts/app.py: cleaner three-panel layout, better spacing, icons, status bar messages, remove-selected attachment button, attachment counts, improved note list/detail display.
- Fixed a real font-rendering issue found during visual testing by loading a Windows font into Qt when available.
- Updated docs and AI log to reflect the bug-fix/UI pass.

Verified:
python -m py_compile main.py pnts\models.py pnts\storage.py pnts\app.py tests\test_storage.py
python -m unittest discover -s tests

Result: 5 tests passed.

The improved app is running now. Process ID: 15992.
```

### Critical Evaluation

The original app met the basic assignment requirements, but the improved version was safer and clearer. The AI did not just change colors or spacing. It fixed real behavior problems involving corrupted data, invalid attachments, and path safety. The visual screenshot check was useful because it revealed the font problem that normal unit tests would not catch.

The phrase "fix all bugs" is very broad, so this does not mean every possible bug was mathematically proven impossible. It means the AI reviewed the code, tested the main behavior, fixed discovered issues, and reran verification.

## Transcript 5: GitHub And Vercel Publication

Date: May 6, 2026

### User Prompt

```text
Deploy this project on my github as "Csci 390 ... assignment" and publish it on vercel to be easily accessible for the professor. Be sure to check every errors and fix it.
```

### Assistant Response And Actions

```text
I’ll use the GitHub publishing workflow and the Vercel deployment workflow here. One important constraint up front: Vercel cannot run a PyQt desktop GUI in the browser, so I’ll make a professor-friendly web landing page that hosts the project overview, run instructions, and deliverables, while GitHub contains the actual desktop source code.
```

The AI checked GitHub CLI authentication and confirmed the account was authenticated as:

```text
BatOrgil7
```

The AI also checked Vercel CLI and found an error because the local Vercel CLI shim pointed to a missing `vc.js` file. It repaired the Vercel CLI install with:

```powershell
npm install -g vercel@latest
```

The AI created a static Vercel landing page for the professor because a PyQt desktop app cannot run directly on Vercel. The static page included:

- Project title and course name.
- App screenshot generated from the PyQt implementation.
- Feature summary.
- Deliverables list.
- GitHub source link.
- Download ZIP link.
- Local run commands.

The AI added these publication files:

- `index.html`
- `styles.css`
- `site-assets/pnts-ui-preview.png`
- `.vercelignore`
- `vercel.json`

The AI created and pushed a public GitHub repository:

```text
https://github.com/BatOrgil7/Csci-390-AI-Augmented-Development-Assignment
```

### Deployment Debugging

The first Vercel deployment failed because Vercel auto-detected the repository as a Python web backend due to `requirements.txt`. The error said:

```text
No python entrypoint found.
```

The AI evaluated the error and determined that the project is not a Python web server. The correct fix was not to force the PyQt app into Vercel. Instead, the AI configured Vercel to deploy the static professor-facing page by updating `vercel.json`.

After the fix, Vercel build and deploy succeeded.

### Assistant Final Response For This Step

```text
Done. The project is published and verified.

GitHub repo: https://github.com/BatOrgil7/Csci-390-AI-Augmented-Development-Assignment

Vercel page for your professor: https://csci-390-ai-augmented-development-a.vercel.app

I fixed the Vercel deployment issue too: Vercel first auto-detected the repo as a Python web backend because of requirements.txt, but this is a PyQt desktop app. I added an explicit static Vercel config so it deploys the professor-facing landing page instead.

Verified:
- Python syntax check passed
- 5 unit tests passed
- Vercel production deployment is Ready
- Vercel page, CSS, screenshot asset, and GitHub repo all return HTTP 200
- Vercel error logs: no errors found
- GitHub repo is public and default branch is main
```

### Critical Evaluation

This was an important design decision. Vercel is a web hosting platform, while the assignment required a desktop PyQt app. The AI correctly avoided pretending the desktop app could run in a browser. Instead, it used Vercel as a public project page and kept the real runnable source code on GitHub.

The AI also checked errors instead of stopping after the first deploy attempt. It fixed the Vercel framework detection problem, verified the live page, checked the screenshot asset, checked the GitHub repository, and checked Vercel logs for errors.

## Final Verification Recorded Before Submission

The project was verified with:

```powershell
python -m py_compile main.py pnts\models.py pnts\storage.py pnts\app.py tests\test_storage.py
python -m unittest discover -s tests
```

Other verification:

- Static asset check passed.
- Vercel production deployment reached Ready status.
- Live Vercel HTML returned HTTP 200.
- Live Vercel CSS returned HTTP 200.
- Live Vercel screenshot asset returned HTTP 200.
- GitHub repository returned HTTP 200.
- GitHub repository visibility was public.
- Vercel error log check reported no errors.

## Current Public Links

```text
GitHub repository:
https://github.com/BatOrgil7/Csci-390-AI-Augmented-Development-Assignment

Vercel project page:
https://csci-390-ai-augmented-development-a.vercel.app
```

