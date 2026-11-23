"""Точка входу та головне вікно журналу навчальних сесій."""

import argparse
import sys
from dataclasses import replace
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QStyle,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from dialogs import SettingsDialog
from journal import MAX_GOAL, MIN_GOAL, JournalSettings, export_journal
from widgets import JournalPanel, SessionForm


class MainWindow(QMainWindow):
    def __init__(self, stylesheet: str, *, styled: bool = True) -> None:
        super().__init__()
        self.settings = JournalSettings()
        self._stylesheet = stylesheet
        self.setWindowTitle(self.settings.title)
        self.setMinimumSize(860, 535)
        self.resize(1040, 630)

        self.form = SessionForm()
        self.journal = JournalPanel(self.settings)
        panels = QHBoxLayout()
        panels.setSpacing(16)
        panels.addWidget(self.form, 5)
        panels.addWidget(self.journal, 6)
        central = QWidget()
        central.setObjectName("workspace")
        layout = QVBoxLayout(central)
        layout.setContentsMargins(17, 16, 17, 16)
        layout.addLayout(panels)
        self.setCentralWidget(central)

        self.count_label = QLabel("Записів: 0 · Завершено: 0 хв")
        self.statusBar().addPermanentWidget(self.count_label)
        self.statusBar().showMessage("Готово")

        # Зв'язки між компонентами належать вікну, яке ними керує.
        self.form.draft_changed.connect(self.journal.show_draft)
        self.form.session_submitted.connect(self.journal.append_session)
        self.journal.totals_changed.connect(self._show_totals)
        self.form.reset_button.clicked.connect(self._show_reset_status)
        self.form.publish_draft()

        self._create_actions(styled)

    def _create_actions(self, styled: bool) -> None:
        self.new_action = QAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon), "Нова сесія", self
        )
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.triggered.connect(self._reset_form)

        self.export_action = QAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton),
            "Експорт JSON…",
            self,
        )
        self.export_action.setShortcut(QKeySequence.StandardKey.Save)
        self.export_action.triggered.connect(self._export)

        self.goal_action = QAction("Ціль на день…", self)
        self.goal_action.setShortcut(QKeySequence("Ctrl+G"))
        self.goal_action.triggered.connect(self._change_goal)

        self.settings_action = QAction("Параметри журналу…", self)
        self.settings_action.setShortcut(QKeySequence("Ctrl+,"))
        self.settings_action.triggered.connect(self._edit_settings)

        self.style_action = QAction("Оформлення QSS", self)
        self.style_action.setCheckable(True)
        self.style_action.setChecked(styled)
        self.style_action.toggled.connect(self._apply_style)

        self.file_menu = self.menuBar().addMenu("Файл")
        self.file_menu.addActions([self.new_action, self.export_action])
        self.tools_menu = self.menuBar().addMenu("Інструменти")
        self.tools_menu.addActions([self.goal_action, self.settings_action])
        self.tools_menu.addSeparator()
        self.tools_menu.addAction(self.style_action)

        self.toolbar = QToolBar("Швидкі дії", self)
        self.toolbar.setMovable(False)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolbar.addActions([self.new_action, self.export_action])
        self.addToolBar(self.toolbar)

        QApplication.instance().setStyleSheet(self._stylesheet if styled else "")

    @pyqtSlot(int, int)
    def _show_totals(self, session_count: int, completed_minutes: int) -> None:
        self.count_label.setText(f"Записів: {session_count} · Завершено: {completed_minutes} хв")
        self.statusBar().showMessage("Сесію додано до журналу.", 5000)

    @pyqtSlot()
    def _show_reset_status(self) -> None:
        self.statusBar().showMessage("Поля форми скинуто.", 5000)

    @pyqtSlot()
    def _reset_form(self) -> None:
        self.form.reset()
        self._show_reset_status()

    @pyqtSlot()
    def _export(self) -> None:
        dialog = QFileDialog(self, "Експорт журналу")
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setNameFilter("JSON (*.json)")
        dialog.setDefaultSuffix("json")
        dialog.selectFile("навчальний_журнал.json")
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        path = dialog.selectedFiles()[0]
        try:
            export_journal(path, self.settings, self.journal.sessions)
        except OSError as error:
            QMessageBox.warning(self, "Помилка експорту", f"Не вдалося записати файл.\n{error}")
            self.statusBar().showMessage("Експорт не виконано.", 5000)
            return

        self.statusBar().showMessage(f"Збережено {Path(path).name}", 5000)

    @pyqtSlot()
    def _change_goal(self) -> None:
        minutes, accepted = QInputDialog.getInt(
            self, "Ціль на день", "Хвилин навчання", self.settings.goal, MIN_GOAL, MAX_GOAL
        )
        if accepted:
            self._apply_settings(replace(self.settings, goal=minutes))
            self.statusBar().showMessage(f"Ціль на день змінено на {minutes} хв.", 5000)

    @pyqtSlot()
    def _edit_settings(self) -> None:
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._apply_settings(dialog.settings)
            self.statusBar().showMessage("Параметри журналу оновлено.", 5000)

    def _apply_settings(self, settings: JournalSettings) -> None:
        self.settings = settings
        self.setWindowTitle(settings.title)
        self.journal.apply_settings(settings)

    @pyqtSlot(bool)
    def _apply_style(self, enabled: bool) -> None:
        QApplication.instance().setStyleSheet(self._stylesheet if enabled else "")
        message = "Оформлення QSS увімкнено." if enabled else "Стандартний вигляд Qt."
        self.statusBar().showMessage(message, 5000)


def main() -> int:
    parser = argparse.ArgumentParser(description="Журнал навчальних сесій")
    parser.add_argument("--plain", action="store_true", help="запустити зі стандартним виглядом Qt")
    args = parser.parse_args()
    app = QApplication([sys.argv[0]])
    app.setStyle("Fusion")
    stylesheet = Path(__file__).with_name("style.qss").read_text(encoding="utf-8")
    window = MainWindow(stylesheet, styled=not args.plain)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
