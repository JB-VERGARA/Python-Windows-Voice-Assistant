from pathlib import Path

from PySide6.QtWidgets import QApplication, QMessageBox


folder = Path.home() / "Desktop" / "Bryan Test Folder"

app = QApplication([])

reply = QMessageBox.question(
    None,
    "Create Folder",
    f"Are you sure you want to create:\n\n{folder}",
    QMessageBox.StandardButton.Yes
    | QMessageBox.StandardButton.No
)

if reply == QMessageBox.StandardButton.Yes:
    folder.mkdir(exist_ok=True)

    QMessageBox.information(
        None,
        "Folder Created",
        f"Folder created successfully:\n\n{folder}"
    )

else:
    QMessageBox.information(
        None,
        "Cancelled",
        "Folder creation cancelled."
    )