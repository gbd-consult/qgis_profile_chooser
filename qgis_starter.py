#!/usr/bin/env python

from qgis.PyQt.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLineEdit, QCompleter, QMessageBox)
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtCore import Qt
from pathlib import Path
import subprocess
import os


def start_qgis():
    app = QApplication([])
    font = QFont("Ubuntu", 15)
    app.setFont(font)

    if os.name == "nt":
        profile_path = (
            Path.home() / Path("AppData/Roaming/QGIS/QGIS3/profiles")
        )
        qgis_path = Path(os.environ.get("OSGEO4W_ROOT")) / Path("bin/qgis.bat")
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
