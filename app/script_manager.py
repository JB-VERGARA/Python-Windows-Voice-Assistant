import json
from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QListWidget,
    QHBoxLayout,
    QVBoxLayout,
)


COMMANDS_FILE = Path("commands/commands.json")


class ScriptManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Script Manager")
        self.setFixedSize(500, 400)

        self.command_list = QListWidget()

        self.command_list.itemClicked.connect(
            self.load_selected_command
        )

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText(
            "Example: open calculator"
        )

        self.script_input = QLineEdit()
        self.script_input.setPlaceholderText(
            "Select a Python script"
        )
        self.alias_input = QLineEdit()
        self.alias_input.setPlaceholderText(
            "Example: launch chrome, start chrome"
        )

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_script)

        add_button = QPushButton("Add Command")
        add_button.clicked.connect(self.save_script)

        edit_button = QPushButton("Save Changes")
        edit_button.clicked.connect(self.edit_script)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_script)

        form_layout = QFormLayout()

        form_layout.addRow(
            "Command:",
            self.command_input
        )

        form_layout.addRow(
            "Script:",
            self.script_input
        )

        form_layout.addRow(
            "Aliases:",
            self.alias_input
        )

        form_layout.addRow(
            "",
            browse_button
        )

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)  

        layout = QVBoxLayout()

        layout.addWidget(self.command_list)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.load_commands()

    def load_commands(self):
        self.command_list.clear()

        try:
            with open(
                COMMANDS_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                commands = json.load(file)

            for command in commands:
                self.command_list.addItem(command)

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )

    def browse_script(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Python Script",
            "scripts",
            "Python Files (*.py)"
        )

        if file_path:
            path = Path(file_path)

            try:
                relative_path = path.relative_to(
                    Path.cwd()
                )

                self.script_input.setText(
                    str(relative_path)
                )

            except ValueError:
                self.script_input.setText(
                    file_path
                )

    def save_script(self):
        command = self.command_input.text().strip().lower()
        script = self.script_input.text().strip()

        aliases = [
            alias.strip().lower()
            for alias in self.alias_input.text().split(",")
            if alias.strip()
        ]

        if not command:
            QMessageBox.warning(
                self,
                "Missing Command",
                "Please enter a command."
            )
            return

        if not script:
            QMessageBox.warning(
                self,
                "Missing Script",
                "Please select a script."
            )
            return

        try:
            with open(
                COMMANDS_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                commands = json.load(file)

            commands[command] = {
                "script": script,
                "aliases": aliases
            }

            with open(
                COMMANDS_FILE,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    commands,
                    file,
                    indent=4
                )

            self.command_input.clear()
            self.script_input.clear()
            self.alias_input.clear()

            self.load_commands()

            QMessageBox.information(
                self,
                "Success",
                f"Added command:\n{command}"
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )
    def load_selected_command(self):
        selected_item = self.command_list.currentItem()

        if not selected_item:
            return

        command = selected_item.text()

        try:
            with open(
                COMMANDS_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                commands = json.load(file)

            entry = commands.get(command)

            if isinstance(entry, dict):
                script = entry.get("script", "")
                aliases = entry.get("aliases", [])

            else:
                script = entry
                aliases = []

            self.command_input.setText(command)
            self.script_input.setText(script)
            self.alias_input.setText(
                ", ".join(aliases)
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )


    def edit_script(self):
        selected_item = self.command_list.currentItem()

        if not selected_item:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a command to edit."
            )
            return

        old_command = selected_item.text()

        new_command = self.command_input.text().strip().lower()
        new_script = self.script_input.text().strip()

        new_aliases = [
            alias.strip().lower()
            for alias in self.alias_input.text().split(",")
            if alias.strip()
        ]

        if not new_command:
            QMessageBox.warning(
                self,
                "Missing Command",
                "Please enter a command."
            )
            return

        if not new_script:
            QMessageBox.warning(
                self,
                "Missing Script",
                "Please select a script."
            )
            return

        try:
            with open(
                COMMANDS_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                commands = json.load(file)

            del commands[old_command]

            commands[new_command] = {
                "script": new_script,
                "aliases": new_aliases
            }

            with open(
                COMMANDS_FILE,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    commands,
                    file,
                    indent=4
                )

            self.load_commands()

            self.command_input.clear()
            self.script_input.clear()
            self.alias_input.clear()

            QMessageBox.information(
                self,
                "Success",
                f"Updated command:\n{new_command}"
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )

    def delete_script(self):
        selected_item = self.command_list.currentItem()

        if not selected_item:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a command to delete."
            )
            return

        command = selected_item.text()

        confirmation = QMessageBox.question(
            self,
            "Delete Command",
            f"Delete command:\n{command}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation != QMessageBox.Yes:
            return

        try:
            with open(
                COMMANDS_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                commands = json.load(file)

            del commands[command]

            with open(
                COMMANDS_FILE,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    commands,
                    file,
                    indent=4
                )

            self.load_commands()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )