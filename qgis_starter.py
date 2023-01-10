#!/usr/bin/env python

from qgis.PyQt.QtWidgets import QInputDialog, QApplication
from pathlib import Path
import subprocess


def start_qgis():
    _ = QApplication([])
    profile_path = Path.home() / Path(".local/share/QGIS/QGIS3/profiles")
    profiles = [
        path.name
        for path in profile_path.iterdir()
        if path.is_dir()
    ]
    profile, entry = QInputDialog.getItem(
        None,
        "Profilauswahl",
        "Profil zum starten auswählen",
        profiles,
        editable=False
    )
    if entry:
        subprocess.run(["qgis", "--profile", profile])


if __name__ == '__main__':
    start_qgis()