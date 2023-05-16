#!/usr/bin/env python

from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLineEdit, QCompleter, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from pathlib import Path
import subprocess
import os


def start_qgis():
    if os.name == "nt":
        profile_path = (
            Path.home() / Path("AppData/Roaming/QGIS/QGIS3/profiles")
        )
        qgis_dirs = [
            path for path in Path("c:/Program Files").iterdir()
            if path.is_dir()
            and path.stem.startwith("QGIS")
        ]
        QMessageBox.information(
            None, "hi", ",".join([q.name for q in qgis_dirs]))
        qgis_path = Path(os.environ.get("OSGEO4W_ROOT")) / Path("bin/qgis.bat")
        font = QFont("Segoe UI", 15)
    else:
        profile_path = Path.home() / Path(".local/share/QGIS/QGIS3/profiles")
        qgis_path = "qgis"
        font = QFont("Ubuntu", 15)

    app = QApplication([])
    app.setFont(font)

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
