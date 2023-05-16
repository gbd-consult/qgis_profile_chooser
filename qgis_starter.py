#!/usr/bin/env python

from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLineEdit, QCompleter, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from pathlib import Path
import subprocess
import os


def choose_qgis(dirs):
    completer = QCompleter(dirs, None)
    completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
    completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
    completer.setCaseSensitivity(Qt.CaseInsensitive)
    line_edit = QLineEdit()
    line_edit.setCompleter(completer)
    dialog = QDialog()
    layout = QVBoxLayout()
    layout.addWidget(line_edit)
    dialog.setLayout(layout)
    dialog.setWindowTitle("Choose QGIS Install:")
    line_edit.returnPressed.connect(dialog.accept)
    dialog.exec_()

    return line_edit.text()


def start_qgis():
    if os.name == "nt":
        font_name = "Segoe UI"
    else:
        font_name = "Ubuntu"

    app = QApplication()
    app.setFont(QFont(font_name, 15))

    if os.name == "nt":
        profile_path = (
            Path.home() / Path("AppData/Roaming/QGIS/QGIS3/profiles")
        )
        qgis_dirs = [
            path for path in Path("c:/Program Files").iterdir()
            if path.is_dir()
            and path.stem.startswith("QGIS")
        ]
        if len(qgis_dirs) > 1:
            qgis_dir = choose_qgis(qgis_dirs)
        elif len(qgis_dirs) == 1:
            qgis_dir = qgis_dirs[0]
        else:
            QMessageBox.critical(None, "Error", "QGIS not found")
            return
        if (qgis_dir / Path("bin/qgis.bat")).exists():
            qgis_path = qgis_dir / Path("bin/qgis.bat")
        elif (qgis_dir / Path("bin/qgis-ltr.bat")).exists():
            qgis_path = qgis_dir / Path("bin/qgis-ltr.bat")
        else:
            QMessageBox.critical(None, "Error", "QGIS bat not found")
            return
    else:
        profile_path = Path.home() / Path(".local/share/QGIS/QGIS3/profiles")
        qgis_path = "qgis"

    profiles = [
        path.name
        for path in profile_path.iterdir()
        if path.is_dir()
    ]
    profiles.sort(key=lambda x: x.lower())

    completer = QCompleter(profiles, None)
    completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
    completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
    completer.setCaseSensitivity(Qt.CaseInsensitive)
    line_edit = QLineEdit()
    line_edit.setCompleter(completer)
    dialog = QDialog()
    layout = QVBoxLayout()
    layout.addWidget(line_edit)
    dialog.setLayout(layout)
    dialog.setWindowTitle("Choose QGIS Profile:")
    line_edit.returnPressed.connect(dialog.accept)
    dialog.exec_()

    profile = line_edit.text()

    if profile and profile not in profiles:
        answer = QMessageBox.question(
            None,
            "Create new profile",
            f"Profile {profile} does not exist. Do you want to create it?"
        )
        if answer == QMessageBox.No:
            return

    subprocess.run([qgis_path, "--profile", profile])


if __name__ == '__main__':
    start_qgis()
