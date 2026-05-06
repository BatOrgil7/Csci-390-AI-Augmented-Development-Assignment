import tempfile
import unittest
from datetime import date
from pathlib import Path

from pnts.storage import InvalidAttachmentError, NoteStore


class NoteStoreTests(unittest.TestCase):
    def test_add_note_persists_and_loads(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = NoteStore(Path(temp_dir))

            created = store.add_note(date(2026, 5, 7), "AI Notes", "PyQt can use a QDateEdit.")
            reloaded = NoteStore(Path(temp_dir))

            self.assertIsNotNone(reloaded.get_note(created.id))
            self.assertEqual(reloaded.notes[0].topic, "AI Notes")
            self.assertEqual(reloaded.notes[0].date, "2026-05-07")

    def test_filter_notes_by_date_topic_and_keyword(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = NoteStore(Path(temp_dir))
            store.add_note("2026-05-07", "Python", "Desktop app using PyQt.")
            store.add_note("2026-05-08", "Biology", "Cell diagram notes.")
            store.add_note("2026-05-07", "Math", "Integrals and graph sketches.")

            results = store.filter_notes(note_date="2026-05-07", topic="py", keyword="desktop")

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].topic, "Python")

    def test_attachment_files_are_copied_and_removed_on_delete(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            source_one = base_path / "source-one.png"
            source_two = base_path / "source-two.jpg"
            source_one.write_bytes(b"fake image one")
            source_two.write_bytes(b"fake image two")

            store = NoteStore(base_path / "data")
            note = store.add_note(
                "2026-05-07",
                "Images",
                "Testing multiple image attachments.",
                [source_one, source_two],
            )

            copied_paths = [store.resolve_image_path(path) for path in note.image_paths]

            self.assertEqual(len(copied_paths), 2)
            self.assertTrue(all(path.exists() for path in copied_paths))
            self.assertTrue(all("/" in image_path for image_path in note.image_paths))

            store.delete_note(note.id)

            self.assertTrue(all(not path.exists() for path in copied_paths))

    def test_unsupported_attachment_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            source = base_path / "not-an-image.txt"
            source.write_text("plain text", encoding="utf-8")

            store = NoteStore(base_path / "data")

            with self.assertRaises(InvalidAttachmentError):
                store.add_note("2026-05-07", "Bad attachment", "This should fail.", [source])

            self.assertEqual(store.notes, [])

    def test_invalid_json_is_backed_up_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            data_path = base_path / "data"
            data_path.mkdir()
            notes_file = data_path / "notes.json"
            notes_file.write_text("{not valid json", encoding="utf-8")

            store = NoteStore(data_path)
            backups = list(data_path.glob("notes.invalid-*.json"))

            self.assertEqual(store.notes, [])
            self.assertIsNotNone(store.load_error)
            self.assertEqual(len(backups), 1)


if __name__ == "__main__":
    unittest.main()
