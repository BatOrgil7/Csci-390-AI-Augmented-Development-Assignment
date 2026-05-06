# User Documentation

## Application Name

Personal Note-Taking System (PNTS)

## Purpose

PNTS is a desktop application for creating and organizing personal notes by date and topic. Each note can include written content and multiple image attachments.

## Installation

1. Install Python 3.12 or another current Python 3 version.
2. Open a terminal in the project folder.
3. Install PyQt6:

```powershell
python -m pip install -r requirements.txt
```

4. Start the application:

```powershell
python main.py
```

## Creating a Note

1. Select a date using the date picker in the Create Note section.
2. Enter a topic.
3. Type note content in the multiline content box.
4. Select Add Images to attach one or more image files.
5. Select Remove to remove a selected pending image, or Clear to remove all pending images.
6. Select Save Note.

The note appears in the Notes list after saving. Attached image files are copied into the app's local `data/images/` folder so the note still has access to them later.

## Viewing Notes

All notes are shown in the Notes list. Select a note to view:

- Topic
- Date
- Content
- Attached images

If a note has several images, they appear vertically in the image viewer area.

## Filtering Notes

Use the Filter Notes section to narrow the notes list:

- Use date: When checked, only notes matching the selected date appear.
- Topic: Shows notes whose topic contains the typed text.
- Keyword: Searches both topic and note content.
- Clear Filters: Removes all active filters.

The filters can be combined. For example, a user can filter for notes on May 7, 2026 with topic text "Python" and keyword "PyQt".

## Deleting Notes

Select a note, then select Delete. The app asks for confirmation before deleting the note. Images used only by that note are also removed from local storage.

## Data Storage

PNTS stores note data locally:

- `data/notes.json`: Text data for saved notes.
- `data/images/`: Copied image attachments.

The `data/` folder is ignored by Git because it contains user-generated notes and images rather than source code.

If `notes.json` becomes unreadable, PNTS backs it up as `notes.invalid-[timestamp].json` and opens with a fresh note list instead of crashing.

## Troubleshooting

If the app does not start and reports that PyQt6 is missing, run:

```powershell
python -m pip install -r requirements.txt
```

If attached images do not display, confirm that the image files are valid `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, or `.webp` files.
