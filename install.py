#!/usr/bin/env python
from pathlib import Path

with open("qgis_starter.desktop", "r") as desktop_file:
    content = desktop_file.read()

content = content.replace("!REPLACE", str(Path.cwd()))

desktop_file_path = Path.home() / Path(
    ".local/share/applications/start_qgis.desktop")

with open(desktop_file_path, "w") as desktop_file:
    desktop_file.write(content)


print(f"Created shortcut at {desktop_file_path}")
