from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import QDate, QSize, Qt
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QStyle,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QDateEdit,
)

from .models import Note
from .storage import InvalidAttachmentError, NoteStore, SUPPORTED_IMAGE_EXTENSIONS


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WINDOWS_FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/segoeui.ttf"),
    Path("C:/Windows/Fonts/arial.ttf"),
]


def configure_application_font(app: QApplication) -> None:
    for font_path in WINDOWS_FONT_CANDIDATES:
        if not font_path.exists():
            continue

        font_id = QFontDatabase.addApplicationFont(str(font_path))
        if font_id == -1:
            continue

        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            app.setFont(QFont(families[0], 10))
            return


class MainWindow(QMainWindow):
    def __init__(self, store: NoteStore | None = None) -> None:
        super().__init__()
        app = QApplication.instance()
        if app is not None:
            configure_application_font(app)
        self.store = store or NoteStore(PROJECT_ROOT / "data")
        self.pending_attachments: list[str] = []
        self.displayed_notes: list[Note] = []

        self.setWindowTitle("Personal Note-Taking System")
        self.resize(1240, 780)
        self.setMinimumSize(980, 640)
        self._build_ui()
        self._connect_events()
        self.refresh_notes()
        if self.store.load_error:
            self.statusBar().showMessage(f"Started with a fresh note list. {self.store.load_error}", 9000)

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("appRoot")
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(14)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)
        splitter.addWidget(self._build_form_panel())
        splitter.addWidget(self._build_notes_panel())
        splitter.addWidget(self._build_detail_panel())
        splitter.setSizes([370, 345, 525])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        splitter.setCollapsible(2, False)
        root_layout.addWidget(splitter)

        self.setCentralWidget(central)
        self.statusBar().showMessage("Ready")
        self.setStyleSheet(
            """
            QWidget {
                font-size: 10.5pt;
                color: #243041;
            }
            QMainWindow, QWidget#appRoot {
                background: #eef2f6;
            }
            QWidget#sidePanel, QWidget#listPanel, QWidget#detailPanel {
                background: transparent;
            }
            QGroupBox {
                background: #ffffff;
                border: 1px solid #d4dce8;
                border-radius: 8px;
                margin-top: 16px;
                padding: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
                font-weight: 600;
                color: #1d2939;
            }
            QFrame#detailCard {
                background: #ffffff;
                border: 1px solid #d4dce8;
                border-radius: 8px;
            }
            QLineEdit, QTextEdit, QListWidget, QDateEdit {
                background: #ffffff;
                border: 1px solid #c3ccd9;
                border-radius: 6px;
                padding: 8px;
                selection-background-color: #2457a7;
                selection-color: #ffffff;
            }
            QLineEdit:focus, QTextEdit:focus, QListWidget:focus, QDateEdit:focus {
                border: 1px solid #2457a7;
            }
            QListWidget {
                alternate-background-color: #f8fafc;
                outline: 0;
            }
            QListWidget::item {
                border: 1px solid transparent;
                border-radius: 6px;
                margin: 4px;
                padding: 8px;
            }
            QListWidget::item:selected {
                background: #e7eefb;
                border: 1px solid #9fb8e8;
                color: #13294b;
            }
            QPushButton {
                background: #2457a7;
                color: white;
                border: 0;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: 600;
                min-height: 28px;
            }
            QPushButton:hover {
                background: #1e4a8f;
            }
            QPushButton:disabled {
                background: #d9e0ea;
                color: #7b8798;
            }
            QPushButton#secondaryButton {
                background: #e9edf4;
                color: #1f2933;
            }
            QPushButton#secondaryButton:hover {
                background: #dbe3ee;
            }
            QPushButton#dangerButton {
                background: #b42318;
            }
            QPushButton#dangerButton:hover {
                background: #971f15;
            }
            QLabel#titleLabel {
                font-size: 17pt;
                font-weight: 700;
                color: #101828;
            }
            QLabel#panelTitle {
                font-size: 14pt;
                font-weight: 700;
                color: #101828;
            }
            QLabel#mutedLabel {
                color: #637083;
            }
            QLabel#fieldLabel {
                color: #344054;
                font-weight: 600;
            }
            QLabel#sectionLabel {
                color: #344054;
                font-weight: 700;
            }
            QScrollArea {
                border: 1px solid #d4dce8;
                border-radius: 8px;
                background: #f8fafc;
            }
            QStatusBar {
                background: #eef2f6;
                color: #526071;
            }
            """
        )

    def _build_form_panel(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("sidePanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        title = QLabel("PNTS")
        title.setObjectName("titleLabel")
        subtitle = QLabel("Personal notes organized by date, topic, and context.")
        subtitle.setObjectName("mutedLabel")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self._build_create_group())
        layout.addWidget(self._build_filter_group())
        layout.addStretch()
        return panel

    def _build_create_group(self) -> QGroupBox:
        group = QGroupBox("New Note")
        layout = QGridLayout(group)
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)
        layout.setColumnStretch(1, 1)

        self.note_date_edit = QDateEdit()
        self.note_date_edit.setCalendarPopup(True)
        self.note_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.note_date_edit.setDate(QDate.currentDate())

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Example: AI augmented development")

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Write the note content here...")
        self.content_input.setMinimumHeight(150)

        self.attachment_list = QListWidget()
        self.attachment_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.attachment_list.setMinimumHeight(82)

        self.add_images_button = QPushButton("Add Images")
        self.add_images_button.setToolTip("Attach one or more image files")
        self.remove_image_button = QPushButton("Remove")
        self.remove_image_button.setObjectName("secondaryButton")
        self.remove_image_button.setToolTip("Remove the selected pending image")
        self.clear_images_button = QPushButton("Clear")
        self.clear_images_button.setObjectName("secondaryButton")
        self.clear_images_button.setToolTip("Clear all pending images")
        self.save_button = QPushButton("Save Note")
        self.save_button.setToolTip("Save this note")
        self.attachment_count_label = QLabel("No images selected")
        self.attachment_count_label.setObjectName("mutedLabel")
        self._apply_button_icons()

        image_buttons = QHBoxLayout()
        image_buttons.setSpacing(8)
        image_buttons.addWidget(self.add_images_button)
        image_buttons.addWidget(self.remove_image_button)
        image_buttons.addWidget(self.clear_images_button)

        date_label = self._field_label("Date")
        topic_label = self._field_label("Topic")
        content_label = self._field_label("Content")
        images_label = self._field_label("Images")

        layout.addWidget(date_label, 0, 0)
        layout.addWidget(self.note_date_edit, 0, 1)
        layout.addWidget(topic_label, 1, 0)
        layout.addWidget(self.topic_input, 1, 1)
        layout.addWidget(content_label, 2, 0, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.content_input, 2, 1)
        layout.addWidget(images_label, 3, 0, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.attachment_list, 3, 1)
        layout.addWidget(self.attachment_count_label, 4, 1)
        layout.addLayout(image_buttons, 5, 1)
        layout.addWidget(self.save_button, 6, 1)
        self._refresh_attachment_list()
        return group

    def _build_filter_group(self) -> QGroupBox:
        group = QGroupBox("Filter Notes")
        layout = QGridLayout(group)
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)
        layout.setColumnStretch(1, 1)

        self.use_date_filter = QCheckBox("Use date")
        self.filter_date_edit = QDateEdit()
        self.filter_date_edit.setCalendarPopup(True)
        self.filter_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.filter_date_edit.setDate(QDate.currentDate())
        self.filter_date_edit.setEnabled(False)

        self.topic_filter_input = QLineEdit()
        self.topic_filter_input.setPlaceholderText("Topic contains...")

        self.keyword_filter_input = QLineEdit()
        self.keyword_filter_input.setPlaceholderText("Keyword in topic or content...")

        self.clear_filters_button = QPushButton("Clear Filters")
        self.clear_filters_button.setObjectName("secondaryButton")
        self.clear_filters_button.setToolTip("Reset date, topic, and keyword filters")
        self.clear_filters_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton))

        layout.addWidget(self.use_date_filter, 0, 0)
        layout.addWidget(self.filter_date_edit, 0, 1)
        layout.addWidget(self._field_label("Topic"), 1, 0)
        layout.addWidget(self.topic_filter_input, 1, 1)
        layout.addWidget(self._field_label("Keyword"), 2, 0)
        layout.addWidget(self.keyword_filter_input, 2, 1)
        layout.addWidget(self.clear_filters_button, 3, 1)
        return group

    def _field_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("fieldLabel")
        return label

    def _apply_button_icons(self) -> None:
        self.add_images_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))
        self.remove_image_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton))
        self.clear_images_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_LineEditClearButton))
        self.save_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))

    def _build_notes_panel(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("listPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        heading = QLabel("Notes")
        heading.setObjectName("panelTitle")
        self.note_count_label = QLabel()
        self.note_count_label.setObjectName("mutedLabel")

        self.notes_list = QListWidget()
        self.notes_list.setAlternatingRowColors(True)
        self.notes_list.setWordWrap(True)
        self.notes_list.setSpacing(2)
        self.notes_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.notes_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        layout.addWidget(heading)
        layout.addWidget(self.note_count_label)
        layout.addWidget(self.notes_list)
        return panel

    def _build_detail_panel(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("detailPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        heading_row = QHBoxLayout()
        detail_heading = QLabel("Selected Note")
        detail_heading.setObjectName("panelTitle")
        heading_row.addWidget(detail_heading)
        heading_row.addStretch()

        self.delete_button = QPushButton("Delete")
        self.delete_button.setObjectName("dangerButton")
        self.delete_button.setToolTip("Delete the selected note")
        self.delete_button.setEnabled(False)
        self.delete_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
        heading_row.addWidget(self.delete_button)

        self.detail_card = QFrame()
        self.detail_card.setObjectName("detailCard")
        self.detail_card.setFrameShape(QFrame.Shape.StyledPanel)
        card_layout = QVBoxLayout(self.detail_card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)

        self.detail_topic_label = QLabel("No note selected")
        self.detail_topic_label.setObjectName("titleLabel")
        self.detail_topic_label.setWordWrap(True)

        self.detail_date_label = QLabel("")
        self.detail_date_label.setObjectName("mutedLabel")

        self.detail_content = QTextEdit()
        self.detail_content.setReadOnly(True)
        self.detail_content.setMinimumHeight(180)

        self.image_scroll = QScrollArea()
        self.image_scroll.setWidgetResizable(True)
        self.image_scroll.setMinimumHeight(220)
        self.image_container = QWidget()
        self.image_layout = QVBoxLayout(self.image_container)
        self.image_layout.setContentsMargins(12, 12, 12, 12)
        self.image_layout.setSpacing(8)
        self.image_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.image_scroll.setWidget(self.image_container)

        card_layout.addWidget(self.detail_topic_label)
        card_layout.addWidget(self.detail_date_label)
        content_label = QLabel("Content")
        content_label.setObjectName("sectionLabel")
        card_layout.addWidget(content_label)
        card_layout.addWidget(self.detail_content)
        images_label = QLabel("Attached Images")
        images_label.setObjectName("sectionLabel")
        card_layout.addWidget(images_label)
        card_layout.addWidget(self.image_scroll)

        layout.addLayout(heading_row)
        layout.addWidget(self.detail_card)
        return panel

    def _connect_events(self) -> None:
        self.add_images_button.clicked.connect(self.choose_images)
        self.remove_image_button.clicked.connect(self.remove_selected_attachment)
        self.clear_images_button.clicked.connect(self.clear_pending_attachments)
        self.save_button.clicked.connect(self.save_note)
        self.clear_filters_button.clicked.connect(self.clear_filters)
        self.use_date_filter.stateChanged.connect(self.toggle_date_filter)
        self.filter_date_edit.dateChanged.connect(lambda: self.refresh_notes())
        self.topic_filter_input.textChanged.connect(lambda: self.refresh_notes())
        self.keyword_filter_input.textChanged.connect(lambda: self.refresh_notes())
        self.notes_list.currentItemChanged.connect(self.display_selected_note)
        self.delete_button.clicked.connect(self.delete_selected_note)

    def choose_images(self) -> None:
        supported_types = " ".join(f"*{extension}" for extension in sorted(SUPPORTED_IMAGE_EXTENSIONS))
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Image Attachments",
            "",
            f"Image Files ({supported_types});;All Files (*)",
        )
        added_count = 0
        for file_path in files:
            if file_path not in self.pending_attachments:
                self.pending_attachments.append(file_path)
                added_count += 1
        self._refresh_attachment_list()
        if added_count:
            self.statusBar().showMessage(f"Added {added_count} pending image{'s' if added_count != 1 else ''}.", 4000)

    def remove_selected_attachment(self) -> None:
        current_row = self.attachment_list.currentRow()
        if current_row < 0:
            return

        removed_path = self.pending_attachments.pop(current_row)
        self._refresh_attachment_list()
        self.statusBar().showMessage(f"Removed {Path(removed_path).name} from pending images.", 4000)

    def clear_pending_attachments(self) -> None:
        had_attachments = bool(self.pending_attachments)
        self.pending_attachments.clear()
        self._refresh_attachment_list()
        if had_attachments:
            self.statusBar().showMessage("Pending images cleared.", 3000)

    def save_note(self) -> None:
        topic = self.topic_input.text().strip()
        content = self.content_input.toPlainText().strip()
        if not topic or not content:
            QMessageBox.warning(self, "Missing Information", "Enter both a topic and note content.")
            return

        try:
            note = self.store.add_note(
                note_date=self.note_date_edit.date().toPyDate(),
                topic=topic,
                content=content,
                attachment_paths=self.pending_attachments,
            )
        except InvalidAttachmentError as error:
            QMessageBox.warning(self, "Attachment Problem", str(error))
            return
        except OSError as error:
            QMessageBox.critical(self, "Save Failed", f"Could not save this note: {error}")
            return

        self.topic_input.clear()
        self.content_input.clear()
        self.clear_pending_attachments()
        self.refresh_notes(select_note_id=note.id)
        if any(displayed_note.id == note.id for displayed_note in self.displayed_notes):
            self.statusBar().showMessage(f'Saved "{note.topic}".', 5000)
        else:
            self.statusBar().showMessage(f'Saved "{note.topic}". It is hidden by the active filters.', 7000)

    def clear_filters(self) -> None:
        self.use_date_filter.setChecked(False)
        self.topic_filter_input.clear()
        self.keyword_filter_input.clear()
        self.refresh_notes()
        self.statusBar().showMessage("Filters cleared.", 3000)

    def toggle_date_filter(self) -> None:
        enabled = self.use_date_filter.isChecked()
        self.filter_date_edit.setEnabled(enabled)
        self.refresh_notes()

    def refresh_notes(self, select_note_id: str | None = None) -> None:
        if select_note_id is None:
            current_item = self.notes_list.currentItem()
            if current_item is not None:
                select_note_id = current_item.data(Qt.ItemDataRole.UserRole)

        filter_date = self.filter_date_edit.date().toPyDate() if self.use_date_filter.isChecked() else None
        self.displayed_notes = self.store.filter_notes(
            note_date=filter_date,
            topic=self.topic_filter_input.text(),
            keyword=self.keyword_filter_input.text(),
        )

        self.notes_list.blockSignals(True)
        self.notes_list.clear()
        selected_row = -1

        for index, note in enumerate(self.displayed_notes):
            preview = " ".join(note.content.split())
            if len(preview) > 86:
                preview = f"{preview[:83]}..."
            image_text = f"{len(note.image_paths)} image{'s' if len(note.image_paths) != 1 else ''}"
            item = QListWidgetItem(f"{note.date} | {note.topic}\n{image_text} | {preview}")
            item.setData(Qt.ItemDataRole.UserRole, note.id)
            item.setToolTip(f"{note.topic}\n{note.date}")
            item.setSizeHint(QSize(260, 66))
            self.notes_list.addItem(item)
            if select_note_id and note.id == select_note_id:
                selected_row = index

        self.notes_list.blockSignals(False)
        count = len(self.displayed_notes)
        self.note_count_label.setText(f"{count} note{'s' if count != 1 else ''} shown")

        if selected_row >= 0:
            self.notes_list.setCurrentRow(selected_row)
        elif self.displayed_notes:
            self.notes_list.setCurrentRow(0)
        else:
            self._show_empty_detail()

    def display_selected_note(self, current: QListWidgetItem | None, _previous: QListWidgetItem | None) -> None:
        if current is None:
            self._show_empty_detail()
            return

        note_id = current.data(Qt.ItemDataRole.UserRole)
        note = self.store.get_note(note_id)
        if note is None:
            self._show_empty_detail()
            return

        self.detail_topic_label.setText(note.topic)
        image_text = f"{len(note.image_paths)} image{'s' if len(note.image_paths) != 1 else ''}"
        self.detail_date_label.setText(f"Date: {note.date} | {image_text}")
        self.detail_content.setPlainText(note.content)
        self.delete_button.setEnabled(True)
        self._render_images(note)

    def delete_selected_note(self) -> None:
        current = self.notes_list.currentItem()
        if current is None:
            return

        note_id = current.data(Qt.ItemDataRole.UserRole)
        note = self.store.get_note(note_id)
        if note is None:
            return

        answer = QMessageBox.question(
            self,
            "Delete Note",
            f'Delete the note "{note.topic}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        self.store.delete_note(note_id)
        self.refresh_notes()
        self.statusBar().showMessage(f'Deleted "{note.topic}".', 5000)

    def _refresh_attachment_list(self) -> None:
        self.attachment_list.clear()
        for path in self.pending_attachments:
            self.attachment_list.addItem(Path(path).name)

        count = len(self.pending_attachments)
        self.attachment_count_label.setText(
            f"{count} pending image{'s' if count != 1 else ''}" if count else "No images selected"
        )
        self.remove_image_button.setEnabled(count > 0)
        self.clear_images_button.setEnabled(count > 0)

    def _render_images(self, note: Note) -> None:
        self._clear_image_layout()

        if not note.image_paths:
            no_images = QLabel("No images attached.")
            no_images.setObjectName("mutedLabel")
            self.image_layout.addWidget(no_images)
            return

        for relative_path in note.image_paths:
            try:
                image_path = self.store.resolve_image_path(relative_path)
            except ValueError:
                image_path = Path(relative_path)
            label = QLabel()
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            label.setWordWrap(True)

            pixmap = QPixmap(str(image_path))
            if pixmap.isNull():
                label.setText(f"Could not load image: {image_path.name}")
            else:
                max_width = max(260, self.image_scroll.viewport().width() - 36)
                target_width = min(max_width, pixmap.width())
                scaled = pixmap.scaledToWidth(target_width, Qt.TransformationMode.SmoothTransformation)
                label.setPixmap(scaled)

            caption = QLabel(image_path.name)
            caption.setObjectName("mutedLabel")
            caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.image_layout.addWidget(label)
            self.image_layout.addWidget(caption)

    def _clear_image_layout(self) -> None:
        while self.image_layout.count():
            item = self.image_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _show_empty_detail(self) -> None:
        self.detail_topic_label.setText("No note selected")
        self.detail_date_label.setText("")
        self.detail_content.clear()
        self.delete_button.setEnabled(False)
        self._clear_image_layout()
        empty = QLabel("Select a note from the list to view its images.")
        empty.setObjectName("mutedLabel")
        empty.setWordWrap(True)
        self.image_layout.addWidget(empty)


def run() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Personal Note-Taking System")
    configure_application_font(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
