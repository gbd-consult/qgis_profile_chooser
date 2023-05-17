#!/usr/bin/env python

from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QCompleter,
    QMessageBox,
    QDialogButtonBox,
    QComboBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from pathlib import Path
import subprocess
import sys
import platform


def choose_qgis(dirs):
    combobox = QComboBox()
    combobox.addItems(dirs)
    buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    dialog = QDialog()
    layout = QVBoxLayout()
    layout.addWidget(combobox)
    layout.addWidget(buttonbox)
    dialog.setLayout(layout)
    dialog.setWindowTitle("Choose QGIS Install:")
    buttonbox.accepted.connect(dialog.accept)
    dialog.exec_()

    return combobox.currentText()


def start_qgis():
    if platform.system() == "Windows":
        font_name = "Segoe UI"
    elif platform.system() == "Darwin":
        font_name = "San Francisco"
    else:
        font_name = "Ubuntu"

    app = QApplication(sys.argv)
    app.setFont(QFont(font_name, 15))

    if platform.system() == "Windows":
        profile_path = (
            Path.home() / Path("AppData/Roaming/QGIS/QGIS3/profiles")
        )
        qgis_dirs = {
            path.name: path
            for path in Path("c:/Program Files").iterdir()
            if path.is_dir()
            and path.stem.startswith("QGIS")
        }
        if len(qgis_dirs) > 1:
            qgis_dir = qgis_dirs[choose_qgis(qgis_dirs.keys())]
        elif len(qgis_dirs) == 1:
            qgis_dir = qgis_dirs[qgis_dirs.keys()[0]]
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
    elif platform.system() == "Darwin":
        profile_path = (
            Path.home() /
            Path("~/Library/Application Support/QGIS/QGIS3/profiles")
        )
        qgis_path = "qgis"
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
