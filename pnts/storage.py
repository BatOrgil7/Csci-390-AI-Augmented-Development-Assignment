from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path
from uuid import uuid4

from .models import Note, current_timestamp


SUPPORTED_IMAGE_EXTENSIONS = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".webp"}


class NoteStoreError(Exception):
    """Base exception for storage problems."""


class InvalidAttachmentError(NoteStoreError):
    """Raised when an attachment path is missing or not a supported image."""


class NoteStore:
    """JSON-backed note repository used by the desktop UI."""

    def __init__(self, data_dir: Path | str = "data") -> None:
        self.data_dir = Path(data_dir)
        self.image_dir = self.data_dir / "images"
        self.notes_file = self.data_dir / "notes.json"
        self.notes: list[Note] = []
        self.load_error: str | None = None
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.image_dir.mkdir(parents=True, exist_ok=True)
        self.load()

    def load(self) -> list[Note]:
        if not self.notes_file.exists():
            self.notes = []
            return self.notes

        try:
            with self.notes_file.open("r", encoding="utf-8") as file:
                raw_notes = json.load(file)
        except json.JSONDecodeError as error:
            self._backup_invalid_notes_file()
            self.notes = []
            self.load_error = f"Could not read notes file: {error}"
            return self.notes

        if not isinstance(raw_notes, list):
            self._backup_invalid_notes_file()
            self.notes = []
            self.load_error = "Notes file must contain a list of notes."
            return self.notes

        try:
            self.notes = [Note.from_dict(item) for item in raw_notes]
        except (KeyError, TypeError, ValueError) as error:
            self._backup_invalid_notes_file()
            self.notes = []
            self.load_error = f"Could not load saved notes: {error}"
            return self.notes

        self.load_error = None
        self.notes.sort(key=lambda note: (note.date, note.created_at), reverse=True)
        return self.notes

    def save(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        temporary_file = self.notes_file.with_suffix(".tmp")
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump([note.to_dict() for note in self.notes], file, indent=2)
        temporary_file.replace(self.notes_file)

    def add_note(
        self,
        note_date: date | str,
        topic: str,
        content: str,
        attachment_paths: list[Path | str] | None = None,
    ) -> Note:
        normalized_date = note_date.isoformat() if isinstance(note_date, date) else str(note_date)
        copied_images = self._copy_attachments(attachment_paths or [])
        note = Note(
            date=normalized_date,
            topic=topic.strip(),
            content=content.strip(),
            image_paths=copied_images,
        )
        self.notes.append(note)
        self.notes.sort(key=lambda item: (item.date, item.created_at), reverse=True)
        self.save()
        return note

    def delete_note(self, note_id: str) -> bool:
        note = self.get_note(note_id)
        if note is None:
            return False

        self.notes = [item for item in self.notes if item.id != note_id]
        self._delete_unreferenced_images(note.image_paths)
        self.save()
        return True

    def get_note(self, note_id: str) -> Note | None:
        return next((note for note in self.notes if note.id == note_id), None)

    def filter_notes(
        self,
        note_date: date | str | None = None,
        topic: str = "",
        keyword: str = "",
    ) -> list[Note]:
        normalized_date = None
        if note_date:
            normalized_date = note_date.isoformat() if isinstance(note_date, date) else str(note_date)

        topic_query = topic.strip().lower()
        keyword_query = keyword.strip().lower()

        results: list[Note] = []
        for note in self.notes:
            if normalized_date and note.date != normalized_date:
                continue
            if topic_query and topic_query not in note.topic.lower():
                continue
            if keyword_query:
                searchable_text = f"{note.topic}\n{note.content}".lower()
                if keyword_query not in searchable_text:
                    continue
            results.append(note)
        return results

    def resolve_image_path(self, relative_path: str) -> Path:
        base_path = self.data_dir.resolve()
        image_path = (self.data_dir / relative_path).resolve()
        if not image_path.is_relative_to(base_path):
            raise ValueError(f"Image path is outside the data directory: {relative_path}")
        return image_path

    def _copy_attachments(self, attachment_paths: list[Path | str]) -> list[str]:
        sources = [Path(source_path) for source_path in attachment_paths]
        for source in sources:
            if not source.exists() or not source.is_file():
                raise InvalidAttachmentError(f"Attachment does not exist: {source}")
            if source.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
                raise InvalidAttachmentError(f"Unsupported image type: {source.name}")

        copied_paths: list[str] = []
        try:
            for source in sources:
                suffix = source.suffix.lower()
                destination_name = f"{uuid4().hex}{suffix}"
                destination = self.image_dir / destination_name
                shutil.copy2(source, destination)
                copied_paths.append(Path("images", destination_name).as_posix())
        except OSError:
            for copied_path in copied_paths:
                try:
                    self.resolve_image_path(copied_path).unlink()
                except (FileNotFoundError, ValueError):
                    pass
            raise
        return copied_paths

    def _delete_unreferenced_images(self, image_paths: list[str]) -> None:
        still_used = {path for note in self.notes for path in note.image_paths}
        for relative_path in image_paths:
            if relative_path in still_used:
                continue

            try:
                image_path = self.resolve_image_path(relative_path)
            except ValueError:
                continue
            try:
                image_path.unlink()
            except FileNotFoundError:
                pass

    def _backup_invalid_notes_file(self) -> None:
        if not self.notes_file.exists():
            return

        safe_timestamp = current_timestamp().replace(":", "-")
        backup_file = self.notes_file.with_name(f"notes.invalid-{safe_timestamp}.json")
        self.notes_file.replace(backup_file)
