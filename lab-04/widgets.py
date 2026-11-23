"""Форма введення та панель, що показує записи й добову ціль."""

from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QProgressBar,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from journal import (
    MAX_DURATION,
    MIN_DURATION,
    SUBJECTS,
    JournalSettings,
    StudySession,
    validate_session,
)


class SessionForm(QWidget):
    """Збирає введення, перевіряє його та передає через сигнали."""

    draft_changed = pyqtSignal(str, str, int, bool)
    session_submitted = pyqtSignal(object)
    DEFAULT_MINUTES = 45
    DEFAULT_DIFFICULTY = 2

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("sessionForm")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self.topic = QLineEdit()
        self.topic.setPlaceholderText("Наприклад, сигнали та слоти Qt")
        self.topic.setToolTip("Введіть назву теми, яку вивчали.")
        self.topic.setMaxLength(80)

        self.subject = QComboBox()
        self.subject.addItems(SUBJECTS)
        self.subject.setToolTip("Категорія для запису в журналі.")

        self.duration = QSpinBox()
        self.duration.setRange(0, MAX_DURATION)
        self.duration.setValue(self.DEFAULT_MINUTES)
        self.duration.setSuffix(" хв")
        self.duration.setToolTip(f"Для запису потрібно від {MIN_DURATION} до {MAX_DURATION} хв.")

        self.difficulty = QSlider(Qt.Orientation.Horizontal)
        self.difficulty.setRange(1, 5)
        self.difficulty.setValue(self.DEFAULT_DIFFICULTY)
        self.difficulty.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.difficulty.setToolTip("Складність від 1 (легка) до 5 (висока).")
        self.level_label = QLabel(f"{self.DEFAULT_DIFFICULTY}/5")
        self.level_label.setMinimumWidth(32)
        level_layout = QHBoxLayout()
        level_layout.addWidget(self.difficulty, 1)
        level_layout.addWidget(self.level_label)

        self.completed = QCheckBox("Сесія завершена")
        self.completed.setChecked(True)
        self.completed.setToolTip("Тільки завершені сесії зараховуються до цілі.")

        fields = QFormLayout()
        fields.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        fields.setHorizontalSpacing(14)
        fields.setVerticalSpacing(11)
        fields.addRow("&Тема", self.topic)
        fields.addRow("&Категорія", self.subject)
        fields.addRow("Т&ривалість", self.duration)
        fields.addRow("Складність", level_layout)
        fields.addRow("", self.completed)

        self.add_button = QPushButton("Додати сесію")
        self.add_button.setObjectName("addSessionButton")
        self.add_button.setToolTip("Перевірити введення й додати сесію до журналу.")
        self.reset_button = QPushButton("Скинути")
        self.reset_button.setToolTip("Повернути поля форми до початкових значень.")
        actions = QHBoxLayout()
        actions.addWidget(self.add_button)
        actions.addWidget(self.reset_button)
        actions.addStretch(1)

        self.validation = QLabel()
        self.validation.setObjectName("validationMessage")
        self.validation.setWordWrap(True)
        self.validation.setMinimumHeight(32)
        self.validation.setTextFormat(Qt.TextFormat.PlainText)
        self.validation.setAccessibleName("Результат перевірки введення")

        heading = QLabel("Нова сесія")
        heading.setObjectName("panelHeading")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 17, 20, 16)
        layout.setSpacing(12)
        layout.addWidget(heading)
        layout.addLayout(fields)
        layout.addLayout(actions)
        layout.addWidget(self.validation)
        layout.addStretch(1)

        self.topic.textChanged.connect(self.publish_draft)
        self.subject.currentTextChanged.connect(self.publish_draft)
        self.duration.valueChanged.connect(self.publish_draft)
        self.completed.toggled.connect(self.publish_draft)
        self.difficulty.valueChanged.connect(lambda level: self.level_label.setText(f"{level}/5"))
        self.add_button.clicked.connect(self.submit)
        self.reset_button.clicked.connect(self.reset)

    @pyqtSlot()
    def publish_draft(self) -> None:
        self.validation.clear()
        self.draft_changed.emit(
            self.topic.text().strip(),
            self.subject.currentText(),
            self.duration.value(),
            self.completed.isChecked(),
        )

    @pyqtSlot()
    def submit(self) -> None:
        try:
            session = validate_session(
                self.topic.text(),
                self.subject.currentText(),
                self.duration.value(),
                self.difficulty.value(),
                self.completed.isChecked(),
            )
        except ValueError as error:
            self.validation.setText(str(error))
            return
        self.validation.clear()
        self.session_submitted.emit(session)

    @pyqtSlot()
    def reset(self) -> None:
        defaults = (
            (self.topic, self.topic.clear, ()),
            (self.subject, self.subject.setCurrentIndex, (0,)),
            (self.duration, self.duration.setValue, (self.DEFAULT_MINUTES,)),
            (self.difficulty, self.difficulty.setValue, (self.DEFAULT_DIFFICULTY,)),
            (self.completed, self.completed.setChecked, (True,)),
        )
        # Зміна п'яти полів має оновити попередній перегляд лише один раз.
        for widget, setter, args in defaults:
            previous = widget.blockSignals(True)
            try:
                setter(*args)
            finally:
                widget.blockSignals(previous)

        self.level_label.setText(f"{self.DEFAULT_DIFFICULTY}/5")
        self.topic.setFocus()
        self.publish_draft()


class JournalPanel(QWidget):
    """Показує чернетку, список зареєстрованих сесій та виконання цілі."""

    totals_changed = pyqtSignal(int, int)

    def __init__(
        self, settings: JournalSettings, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setObjectName("journalPanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self._sessions: list[StudySession] = []
        self._completed_minutes = 0
        self._goal = settings.goal

        self.heading = QLabel()
        self.heading.setObjectName("panelHeading")
        self.heading.setWordWrap(True)
        self.heading.setTextFormat(Qt.TextFormat.PlainText)

        self.progress = QProgressBar()
        self.progress.setToolTip("Сума хвилин завершених сесій відносно добової цілі.")
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.draft = QLabel()
        self.draft.setObjectName("draftPreview")
        self.draft.setWordWrap(True)
        self.draft.setMinimumHeight(62)
        self.draft.setTextFormat(Qt.TextFormat.PlainText)

        self.entries = QListWidget()
        self.entries.setAlternatingRowColors(True)
        self.entries.setWordWrap(True)
        self.entries.setMinimumHeight(110)
        self.entries.setAccessibleName("Список зареєстрованих сесій")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 17, 20, 16)
        layout.setSpacing(10)
        layout.addWidget(self.heading)
        layout.addWidget(self.progress)
        layout.addWidget(self.draft)
        layout.addWidget(QLabel("Записи"))
        layout.addWidget(self.entries, 1)
        self.apply_settings(settings)

    @property
    def sessions(self) -> tuple[StudySession, ...]:
        return tuple(self._sessions)

    def apply_settings(self, settings: JournalSettings) -> None:
        self.heading.setText(settings.title)
        self._goal = settings.goal
        self.progress.setRange(0, self._goal)
        self._refresh_progress()

    @pyqtSlot(str, str, int, bool)
    def show_draft(self, topic: str, subject: str, minutes: int, completed: bool) -> None:
        name = topic or "тему ще не введено"
        outcome = "буде зараховано до цілі" if completed else "заплановано"
        self.draft.setText(f"Чернетка: {name}\n{subject} · {minutes} хв · {outcome}")

    @pyqtSlot(object)
    def append_session(self, session: StudySession) -> None:
        self._sessions.append(session)
        status = "Завершено" if session.completed else "Заплановано"
        item = QListWidgetItem(
            f"{session.topic}\n{session.subject} · {session.minutes} хв · "
            f"складність {session.difficulty}/5 · {status}"
        )
        self.entries.addItem(item)
        self.entries.scrollToItem(item)
        if session.completed:
            self._completed_minutes += session.minutes
        self._refresh_progress()
        self.totals_changed.emit(len(self._sessions), self._completed_minutes)

    def _refresh_progress(self) -> None:
        self.progress.setValue(min(self._completed_minutes, self._goal))
        self.progress.setFormat(f"{self._completed_minutes} / {self._goal} хв")
