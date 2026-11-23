"""Власне модальне вікно редагування параметрів журналу."""

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from journal import MAX_GOAL, MIN_GOAL, JournalSettings


class SettingsDialog(QDialog):
    def __init__(self, settings: JournalSettings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Параметри журналу")
        self.setModal(True)
        self.setMinimumWidth(410)
        self.settings = settings

        self.title_field = QLineEdit(settings.title)
        self.title_field.setMaxLength(40)
        self.title_field.setPlaceholderText("Назва журналу")
        self.goal_field = QSpinBox()
        self.goal_field.setRange(MIN_GOAL, MAX_GOAL)
        self.goal_field.setSuffix(" хв")
        self.goal_field.setValue(settings.goal)

        fields = QFormLayout()
        fields.addRow("Назва журналу", self.title_field)
        fields.addRow("Ціль на день", self.goal_field)

        self.error = QLabel()
        self.error.setObjectName("validationMessage")
        self.error.setWordWrap(True)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.button(QDialogButtonBox.StandardButton.Save).setText("Зберегти")
        self.buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Скасувати")
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.addLayout(fields)
        layout.addWidget(self.error)
        layout.addWidget(self.buttons)

    def accept(self) -> None:
        title = self.title_field.text().strip()
        if not title:
            self.error.setText("Введіть назву журналу.")
            return
        self.settings = JournalSettings(title, self.goal_field.value())
        super().accept()
