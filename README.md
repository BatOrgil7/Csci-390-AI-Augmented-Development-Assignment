# Personal Note-Taking System

This project implements a desktop Personal Note-Taking System (PNTS) for CSci 390 Exercise 6. It is written in Python with PyQt6.

## Features

- Create notes with a date, topic, multiline content, and multiple image attachments.
- Add, remove, or clear pending image attachments before saving.
- View all saved notes in a list.
- Filter notes by selected date, topic text, and keyword search.
- View selected note details and attached images.
- Delete notes when they are no longer needed.
- Store notes locally in JSON and copy validated image attachments into a local data folder.

## Run the App

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start PNTS:

```powershell
python main.py
```

The app stores runtime data in `data/notes.json` and `data/images/`. That folder is ignored by Git so personal notes and images are not accidentally submitted as source code.

## Project Structure

- `main.py`: Application entry point.
- `pnts/app.py`: PyQt6 user interface.
- `pnts/models.py`: Note data model.
- `pnts/storage.py`: JSON storage, filtering, image validation/copying, and delete cleanup.
- `tests/test_storage.py`: Non-GUI tests for persistence, filtering, attachment handling, and invalid JSON recovery.
- `docs/USER_DOCUMENTATION.md`: User documentation.
- `docs/AI_INTERACTION_LOG.md`: AI transcript and critical evaluation notes.
- `docs/EXPERIENCE_SUMMARY.md`: Experience summary draft.

## Test Non-GUI Logic

```powershell
python -m unittest discover -s tests
```
